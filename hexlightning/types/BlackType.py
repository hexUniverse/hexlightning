from dataclasses import dataclass, field
from typing import List


@dataclass
class BlackType:
    """黑名單類型
    Parameters:
        name (``str``):
            處理時顯示
        description (``str``):
            點擊左側時顯示解說
        code (``str``):
            代號
        emoji (``str``):
            emoji 代表
        height (``int``):
            Photo height.
        druations (``int``):
            處刑幾日
    """
    name: str = field(hash=False, repr=True, compare=False, default=None)
    description: str = field(hash=False, repr=True,
                             compare=False, default=None)
    emoji: str = field(hash=False, repr=True, compare=False, default=None)
    druations: int = field(hash=False, repr=True, compare=False, default=None)
    code: str = field(hash=False, repr=True, compare=False, default=None)


@dataclass
class BlackTypeList:
    spam: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    ads: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    halal: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    porn: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    child: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    vio: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    scam: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    botspam: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    coin: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
    harass: BlackType = field(
        hash=False, repr=True, compare=False, default=None)
