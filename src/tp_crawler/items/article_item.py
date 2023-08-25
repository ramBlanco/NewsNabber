from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ArticleItem:
    date: Optional[int] = field(default=None)
    description: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    category: Optional[str] = field(default=None)
