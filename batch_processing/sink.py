import os
import sys
import json
import signal
import time

# local import
import const
import parser
import helper
from core.postgres_client import PostgresClient
from core.logger import setup_logger
from model.change_event import ChangeEvent


class SinkConnector():
    def __init__(self, parser: parser.Parser) -> None:
        # Graceful shutdown
        signal.signal(signal.SIGINT, self.graceful_shutdown)
        signal.signal(signal.SIGTERM, self.graceful_shutdown)
        self.kill_signal_received = False
        
        # Postgres
        self.postgres_client = PostgresClient(uri=os.environ.get(const.ENV_POSTGRES_URI))

        # Event config
        self.queue = []
        self.failed_event = {}

        # parser
        self.parser = parser

        # Logger
        self.logger = setup_logger(const.LOGGER_SINK_LOCATION, const.LOGGER_SINK)

    # Main function 
    def run(self):
        while not self.kill_signal_received:
            self.pull_event_from_postgres()
            self.process_event()
               
    # Sub-main functions
    def pull_event_from_postgres(self):
        """ Pull change event from postgres """
        self.logger.info("Pulling event from postgres")
        time.sleep(10)

    def process_event(self):
        """ Process events from queue """
        while len(self.queue) != 0:
            event: ChangeEvent = self.queue.pop()
            unique_id = event.get_unique_identity()
            if unique_id in self.failed_event:
                self.logger.info("Due to previous event has failed. Ignore this event")
            else:
                parse_result = self.parser.parse_change_event(event)
                if parse_result != const.PARSE_SUCCESS:
                    self.failed_event[unique_id] = parse_result

    def graceful_shutdown(self, *args): 
        self.kill_signal_received = True
        # Process remaining events
        self.logger.info("Process all remaining events")
        self.process_event()
        
        # Log failed events
        if len(self.failed_event) > 0:
            failed_event = json.dumps(self.failed_event)
            self.logger.error({"failed_event": failed_event})
            
        # Wait for logger write all logs
        helper.delay(5)
        sys.exit(0)

if __name__ == "__main__":
    SinkConnector(parser.DefaultParser()).run()