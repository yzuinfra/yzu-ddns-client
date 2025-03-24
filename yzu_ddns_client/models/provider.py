class BaseProvider:
    def __init__(self, config):
        self.config = config
        self.name = self.__class__.__name__.lower()
    
    def getZones(self):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def getRecords(self, zone_id):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def updateRecord(self, zone_id, record_id, fields={}):
        raise NotImplementedError("This method should be overridden by subclasses.")
    
    def successCodes(self) -> list:
        return [200, 204]