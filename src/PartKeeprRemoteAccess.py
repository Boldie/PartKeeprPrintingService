import md5
import pprint
import requests
import json

class PartKeeprRemoteAccess:
    """
    This class is our proxy class to access the remote part keepr
    installation and will hels us to handle the connection and authentification.
    """
    
    def __init__(self, remoteBaseUrl ):
        """
        Construct remote proxy.
        
        @param remoteBaseUrl: The base url (to PartKeepr/frontend) of the remote installation.
        """
        self.remoteBaseUrl = remoteBaseUrl
        self.lastError = ""
    
    def auth(self, username, password):
        pwHash = md5.new()
        pwHash.update(password);
        
        self.session = requests.Session();
        r = self.session.get(self.remoteBaseUrl + 'rest.php/Auth/login'
                     , params={ 'username' : username, 'password' : pwHash.hexdigest() })
        
        if r.status_code == 200:
            rslt = r.json()
            if ('success' in rslt and rslt['success'] ):
                #pprint.pprint(self.cookies)
                self.session.headers.update({'session': r.cookies['PHPSESSID']})
                return
            else:
                raise Exception("Login failed: Status code: " + str( r.status_code ) )
        elif r.status_code == 400:
            rslt = r.json()
            if 'exception' in rslt and 'message' in rslt['exception']:
                err = rslt['exception']['message']
            else:
                err = 'Unknown'
            raise Exception("Login failed: " + err )
        else:
            raise Exception("Login failed: Status code: " + str( r.status_code ) )
    
    def getWaitingPrintJobs(self):
        r = self.session.get(self.remoteBaseUrl + 'rest.php/Printing.PrintingJob'
                             , params={ 'filter': 
                                      json.dumps([{'property':'done', 'value':'0'}])
                                      }
                             )
       
        if r.status_code == 200:
            rslt = r.json()
            if ('success' in rslt and rslt['success'] and 'response' in rslt and 'data' in rslt['response']):
                return rslt['response']['data'];
            else:
                raise Exception("Query returns: Not successfull");
        elif r.status_code == 400:
            rslt = r.json()
            if 'exception' in rslt and 'message' in rslt['exception']:
                err = rslt['exception']['message']
            else:
                err = 'Unknown'
            raise Exception("Query failed: " + err)
        else:
            raise Exception("Unknown status code: %i" % r.status_code)
        
    def retrieveDataForPrintingJob(self, job):
        r = self.session.get(self.remoteBaseUrl + 'file.php'
                             , params={'type' : 'Print', 'id' : job['data']})
       
        if r.status_code == 200:
            #pprint.pprint(r.headers);
            return { 'content' : r.content, 'headers': r.headers }
        else:
            raise Exception("Error while fetching binary file: %i" % r.status_code)
        
    def setJobDone(self, job):
        r = self.session.put(self.remoteBaseUrl + 'rest.php/Printing.PrintingJob'
                             , params={'id': job['id'], 'done': 'true' } )
       
        if r.status_code == 200:
            rslt = r.json()
            if ('success' in rslt and rslt['success'] ):
                return True;
            else:
                raise Exception("Query returns: Not successfull");
        elif r.status_code == 400:
            rslt = r.json()
            if 'exception' in rslt and 'message' in rslt['exception']:
                err = rslt['exception']['message']
            else:
                err = 'Unknown'
            raise Exception("Query failed: " + err)
        else:
            raise Exception("Unknown status code: %i" % r.status_code)

        
    def registerListener(self,eventName):
        r = self.session.put(self.remoteBaseUrl + 'rest.php/EventNotification/registerListener'
                             , params={'event':eventName} )

        if r.status_code == 200:
            rslt = r.json()
            if ('success' in rslt and rslt['success'] ):
                return
            else:
                raise Exception("Query returns: Not successfull");
        elif r.status_code == 400:
            rslt = r.json()
            if 'exception' in rslt and 'message' in rslt['exception']:
                err = rslt['exception']['message']
            else:
                err = 'Unknown'
            raise Exception("Query failed: " + err)
        else:
            raise Exception("Unknown status code: %i" % r.status_code)
        
    def isListenerNotified(self):
        r = self.session.put(self.remoteBaseUrl + 'rest.php/EventNotification/isNotified'
                             , params={'long':'1'} )
        
        if r.status_code == 200:
            rslt = r.json()
            if ('success' in rslt and rslt['success'] ):
                return rslt['response']['data']
            else:
                raise Exception('Query was not successfull!');
        elif r.status_code == 400:
            rslt = r.json()
            if 'exception' in rslt and 'message' in rslt['exception']:
                raise Exception(rslt['exception']['message'])
            else:
                raise Exception('Unknown error while sending request!')
        else:
            raise Exception("Unknown status code: %i" % r.status_code)
        