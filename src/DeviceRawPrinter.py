import Printer

class DeviceRawPrinter (Printer.Printer):
    """
    This is a printer implementation, which accesses a device
    over the filesystem. Everything passed to printData will be
    directly written to the device.
    """
    
    def __init__(self, config):
        self.config = config;
        # Check access rights and existance on startup!
        fileStream = open( self.config['device'], 'wb' );
        fileStream.close();
    
    def printData(self, data, contentType):
        if contentType != self.config['content-type']:
            print("Unknown content type: %s" % contentType)
            return False
        
        fileStream = open( self.config['device'], 'wb' );
        fileStream.write( data );
        fileStream.close();
        return True
