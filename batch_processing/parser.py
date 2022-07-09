from model.change_event import ChangeEvent
class Parser():
    def __init__(self) -> None:
        pass

    def parse_change_event(self, event: ChangeEvent):
        pass

class DefaultParser(Parser):
    def __init__(self) -> None:
        super().__init__()

    def parse_change_event(self, event: ChangeEvent):
        return super().parse_change_event()