from pymongo import MongoClient

class Watcher(): 
    def __init__(self, uri) -> None:
        self.client = MongoClient(uri)
        self.change_stream = None
    
    def get_change_stream(self):
        self.change_stream = self.client.watch([], batch_size=1000)
        return self.change_stream

    def stop_change_stream(self):
        self.change_stream.close()