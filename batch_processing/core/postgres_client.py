from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData

class PostgresClient():
    def __init__(self, uri) -> None:
        self.client = create_engine(uri)
        self.db = self.client.connect()

    def create_table(self, table, cols):
        meta = MetaData()
        table = Table(table, meta, *cols)
        meta.create_all()    

    

    
