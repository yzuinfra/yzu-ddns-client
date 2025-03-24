class Zone:
    def __init__(self, id: int = -1, name: str = "", records: list = []):
        self.id = id
        self.name = name
        self.records = records

    def __repr__(self):
        return f"Zone(name={self.name}, records={self.records})"
    
    def __getitem__(self, index):
        return self.__dict__[index]