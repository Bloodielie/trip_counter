from dataclasses import dataclass


@dataclass(frozen=True)
class CallBackData:
    type: int
    offset: int
