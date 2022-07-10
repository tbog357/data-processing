import os
import sys
import time
import signal

# local import
import const
import helper
from core.logger import setup_logger
from core.mongodb_watcher import MongoDbWatcher
from core.postgres_client import PostgresClient
from model.change_event import ChangeEvent


class SourceConnector():
    def __init__(self) -> None:
        # Graceful shutdown
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        self.kill_signal_received = False

        # Setup mongdb watcher
        self.watcher = MongoDbWatcher(uri=os.environ.get(const.ENV_MONGODB_URI))
        self.change_stream = self.watcher.get_change_stream()
        
        # Postgres
        self.postgres_client = PostgresClient(uri=os.environ.get(const.ENV_POSTGRES_URI))

        # Event config
        self.queue = []
        self.postgres_timeout = 3
        self.start_time = time.time()

        # Logger
        self.logger = setup_logger(const.LOGGER_SOURCE_LOCATION, const.LOGGER_SOURCE)

    # Main function
    def run(self):
        while not self.kill_signal_received:
            event = self.get_next_event()
            self.add_event_to_queue(event)
            if self.is_time_to_push_event():
                self.push_event_to_postgres()
                self.reset_queue()
    
    # Sub-main functions
    def get_next_event(self):
        """ Get next change event from change stream """
        return self.change_stream.try_next()

    def add_event_to_queue(self, event):
        """ Add change event to queue """
        if event != const.NO_EVENT:
            self.queue.append(ChangeEvent(**event))

    def reset_queue(self):
        """ Reset queue """
        self.queue = []
        self.start_time = time.time()

    def is_time_to_push_event(self):
        """ Indicate time push change events to postgres """
        if len(self.queue) == const.CONFIG_EVENT_BATCH_SIZE:
            return True
        elif helper.time_since(self.start_time) > self.postgres_timeout:
            return True
        else:
            return False

    def push_event_to_postgres(self):
        """ Push all change events in queue to postgres """
        if len(self.queue) > 0:
            self.logger.info(f"Push {len(self.queue)} events to postgres")
        else:
            self.logger.info("Queue is empty")

    def graceful_shutdown(self, *args): 
        self.kill_signal_received = True
        # Close change stream and wait for it fully closed
        self.watcher.stop_change_stream()
        helper.delay(seconds=5)

        # Push remaining event to postgres
        self.logger.info("Push remaining events to postgres")
        self.push_event_to_postgres()

        # Saving timestamp for the next run
        self.logger.info("Saving change stream checkpoint")
        
        # Wait for logger write all logs
        helper.delay(seconds=5)
        sys.exit(0)

if __name__ == "__main__":
    SourceConnector().run()