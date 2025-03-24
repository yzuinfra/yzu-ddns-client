class Record:
    def __init__(self, record_id: str = "", record_name: str = "", record_type: str = "A", record_content: str = None, record_ttl: int = 3600):
        self.record_id = record_id
        self.record_name = record_name
        self.record_type = record_type
        self.record_content = record_content
        self.record_ttl = record_ttl

    def __repr__(self):
        return f"Record(id={self.record_id}, name={self.record_name}, type={self.record_type}, content={self.record_content}, ttl={self.record_ttl})"