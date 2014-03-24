PartKeeprPrintingService
========================

This is a little service daemon which can be used to send printing jobs to your real printer. The service is connecting to a given Partkeeper installation and will check if there is something to print. For the moment this service supports printing to a device only if the rendering is implemented in the Partkeeper side. For many label printers there is a language, which can be sent directly to a printer. The service has been testes succesfully using a Zebra TLP 2824 Plus on a linux (Ubuntu) machine using the ZPL language.

The service will turn your linux box into a printer server for PartKeeper.

TODO: Print PDFs directly using ghostscript or something else.

Installation instructions
-------------------------

To use the service daemon, the following prequesites needs to be installed:
* python
* python requests (http://www.python-requests.org)

    apt-get install python-pip
    pip install requests


Configuration instructions
--------------------------

The first thing to do is to create a configuration file in the src directory. For the moment this file must reside in the directory the PartKeeprPrintingService.py is located. You can use the template file "PartKeeprPrintingService_tpl.ini" and rename it to "PartKeeprPrintingService.ini". Open the file using your favorite editor and adapt the PartKeeper section to fit to your installation. For the username and password it is best to create a new account with the name of your printer. You can select this acount after the service is running and logged in successfully from inside your PartKeeper installation as Printer Target after choosing to print anything.

Now you should find out your printer devicename. Attach your printer to your linux box (which will act as printerserver and which you are configuring now) and check the devicename using dmsg. This decivename must be entered in the "DeviceRawPrinter" section for the entry "device". If you have no printer, you can select any filename and check the basic things by viewing the using tail or cat :).


Starting the service
--------------------

Change to the src directory and run:

    ./PartKeeprPrintingService.py

Now the service should run.


Check if everything is working as expected
------------------------------------------

Finally you can check it using Partkeepr (See also https://wiki.partkeepr.org/wiki/Category:Printing). For a fast check do the follwong steps:

* View -> Printing and Labeling -> Edit Configuration
* Press "Add configuration" on the left pane
* Select "Zebra Label Renderer" for the Renderer and as Datatybe Part.
* Past the following stuff to Additional Configuration

    {
    "template" : "CT~~CD,~CC^~CT~\n^XA~TA000~JSN^LT0^MNW^MTT^PON^PMN^LH0,0^JMA^PR3,3~SD8^JUS^LRN^CI0^XZ\n^XA\n^MMT  \n^PW448\n^LL0256\n^LS0\n^CI28\n^FT20,49^A0N,31,31^FH\\^FD<<name>>^FS\n^FT20,150^A0N,23,24^TBN,390,90^FH\\^FD<<description>>^FS\n^FT20,227^A0N,34,33^FH\\^FD<<storageLocationName>>^FS\n^BY3,3,75^FT191,227^BCN,,N,N\n^FD>;<<barcodeId,%06d>>^FS\n^FT20,183^A0N,23,24^FH\\^FDStorage \\CI13 ^FS\n^FT257,250^A0N,23,24^FB72,1,0,C^FH\\^FD<<barcodeId,%06d>>^FS\n^PQ1,0,1,Y^XZ"
}

* Give it a name and do "Save Configuration"

Now you have prepared the configuration, which can be used for printing. Now you can print one, by right clicking on a part in the "Part List" and choose print. Select your new configuration and the user which you have added for the service before. 


