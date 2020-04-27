from dataclasses import dataclass, field


@dataclass
class User:
    id: int = field(hash=False, repr=True, compare=False, default=None)
    first_name: str = field(hash=False, repr=True, compare=False, default=None)
    last_name: str = field(hash=False, repr=True, compare=False, default=None)
    participate: list = field(hash=False, repr=True,
                              compare=False, default=None)


@dataclass
class Chat:
    chat: User = field(hash=False, repr=True, compare=False, default=None)
