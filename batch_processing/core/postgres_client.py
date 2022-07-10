from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import Table

class PostgresClient():
    def __init__(self, uri) -> None:
        self.engine = create_engine(uri)
        
    def insert_many(self, table, columns, values):
        with Session(self.engine) as session:
            mapping = Table(table, *columns)
            session.bulk_insert_mappings(mapping, values)
            session.commit()
        
    

    
