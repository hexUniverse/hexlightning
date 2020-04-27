from dataclasses import dataclass, field


@dataclass
class Bot:
    token: str = field(hash=False, repr=True, compare=False, default=None)
    api_id: str = field(hash=False, repr=True, compare=False, default=None)
    api_hash: str = field(hash=False, repr=True, compare=False, default=None)
    country: str = field(hash=False, repr=True, compare=False, default=None)
    no: int = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Crowdin:
    project: str = field(hash=False, repr=True, compare=False, default=None)
    project_key: str = field(hash=False, repr=True,
                             compare=False, default=None)


@dataclass
class Rabbitmq:
    url: str = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Mongo:
    replica: int = field(hash=False, repr=True, compare=False, default=None)
    url: int = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Redis:
    url: str = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class NSFW:
    url: str = field(hash=False, repr=True, compare=False, default=None)
    maximum: int = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Log:
    namecheck: str = field(hash=False, repr=True, compare=False, default=None)
    spamname: str = field(hash=False, repr=True, compare=False, default=None)
    evidence: str = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Info:
    version: int = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Logging:
    status: int = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class Configure:
    """設定檔類型
    """
    bot: Bot = field(hash=False, repr=True, compare=False, default=None)
    crowdin: Crowdin = field(hash=False, repr=True,
                             compare=False, default=None)
    rabbitmq: Rabbitmq = field(
        hash=False, repr=True, compare=False, default=None)
    mongo: Mongo = field(hash=False, repr=True, compare=False, default=None)
    redis: Redis = field(hash=False, repr=True, compare=False, default=None)
    nsfw: NSFW = field(hash=False, repr=True, compare=False, default=None)
    log: Log = field(hash=False, repr=True, compare=False, default=None)
    info: Info = field(hash=False, repr=True, compare=False, default=None)
    logging: Logging = field(hash=False, repr=True,
                             compare=False, default=None)
