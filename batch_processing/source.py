import signal
import sys
import time

# local import
import const
from model.change_event import ChangeEvent
from core.mongodb_watcher import Watcher

class SourceConnector():
    def __init__(self) -> None:
        # Graceful shutdown
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        self.kill_signal_received = False

        # Setup mongdb watcher
        self.watcher = Watcher(uri="mongodb://172.20.128.1:27011,172.20.128.2:27012,172.20.128.3:27013/?replicaSet=rs0&authSource=admin")
        self.change_stream = self.watcher.get_change_stream()

        # Event
        self.queue = []
        self.postgres_timeout = 3
        self.start_time = time.time()

    # Main function
    def pull_event(self):
        while not self.kill_signal_received:
            event = self.get_next_event()
            self.add_event(event)

            if self.is_time_to_push_events():
                self.send_event_to_postgres()
                self.reset()
    
    def get_next_event(self):
        return self.change_stream.try_next()

    def add_event(self, event):
        if event == const.NO_EVENT:
            print("No event")
        else:
            self.queue.append(ChangeEvent(**event))

    def reset(self):
        self.queue = []
        self.start_time = time.time()

    def is_time_to_push_events(self):
        if len(self.queue) == const.CONFIG_EVENT_BATCH_SIZE:
            return True
        elif time.time() - self.start_time > self.postgres_timeout:
            return True
        else:
            return False

    def send_event_to_postgres(self):
        if len(self.queue) > 0:
            print("Push to postgres")
        else:
            print("Empty event")

    def graceful_shutdown(self, *args): 
        self.kill_signal_received = True
        self.watcher.stop_change_stream()
        print("Push events to Postgres")
        print("Saving checkpoint")
        print("Shutdown")
        sys.exit(0)
        return

if __name__ == "__main__":
    SourceConnector().pull_event()