from __future__ import print_function

import pprint
import time
import sys
import ConfigParser
from PartKeeprRemoteAccess import PartKeeprRemoteAccess

print("Welcome to Printing Service for PartKeepr v0.1\n")

config = ConfigParser.SafeConfigParser()
config.read('PartKeeprPrintingService.ini')

# Initialize printer
printerModuleName = config.get('Printer','module')
printerModule = __import__( printerModuleName )
printerClass = getattr(printerModule, printerModuleName )  

printerCfg = {}
for name, value  in config.items( printerModuleName ):
    printerCfg[name] = value
    
printer = printerClass( printerCfg )

# Start initializing our remote side and connect
remoteProxy = PartKeeprRemoteAccess(config.get('PartKeepr','baseurl'));
if not remoteProxy.auth(config.get('PartKeepr','username'), config.get('PartKeepr','password')):
    print("Auth failed!\nError: " + remoteProxy.lastError + "\n");
    raise SystemExit

remoteProxy.registerListener('Printing.pendingJob')

print("Preparation done, waiting for jobs now.");

# This is a list of jobs to ignore due to errors.
ignoreJobs = {};

pollInterval = float( config.get('PartKeepr','pollInterval') )
try:
    while True:
        jobs = remoteProxy.getWaitingPrintJobs();
            
        if jobs is None:
            print("Error while fetching jobs: %s" % remoteProxy.lastError)
            time.sleep(5)
            continue
        
        if len(jobs) > 0:
            #print("New jobs available.")
            for job in jobs:
                if not job['done'] and not job['id'] in ignoreJobs:
                    print("Working on job #%i with timestamp %s ..." % ( job['id'], job['created']['date'] ))
                    print("Fetching ...")
                    rv = remoteProxy.retrieveDataForPrintingJob(job);
                    print("Printing ...")
                    if not printer.printData(rv['content'], rv['headers']['content-type']):
                        print("Printer plugin is unable to handle the content!")
                        ignoreJobs[ job['id'] ] = True;
                    else:
                        print("Signal job done.")
                        if remoteProxy.setJobDone(job):
                            print("Job finished successfully!");
                        else:
                            print("Error while setting job to done: %s" % remoteProxy.lastError)
                            
        # Waits for notifications from remote side. We will wait here and not on the top
        # to ensure a quick printing after starting the application.
        notifications = remoteProxy.isListenerNotified()
    
        #sys.stdout.write('.')
        #sys.stdout.flush()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting down!")
