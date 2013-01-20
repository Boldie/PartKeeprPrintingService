class Printer:
    """
    This is an interface class, every printer should be inherit from.
    A printer is a kind of output and implements the way to pass the
    data to the printer.
    """
    
    def printData(self, data, contentType):
        """
        Send the data passed to method to the printer.
        Returns True if successfull, otherwise false.
        """
        return False
