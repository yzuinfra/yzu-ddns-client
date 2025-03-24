class BaseProvider:
    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__.lower()
    
    def getZones(self):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def getRecords(self, zone):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def updateRecord(self, zone, record):
        raise NotImplementedError("This method should be overridden by subclasses.")