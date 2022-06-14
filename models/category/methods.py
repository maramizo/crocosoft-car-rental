from __future__ import annotations
from werkzeug.local import LocalProxy
from models.db import get_db
from dataclasses import dataclass, replace
from models.base import BaseModel


@dataclass
class Category(BaseModel):
    id: int = None
    name: str = None
    carry_capacity: int = None
    _table_name: str = "categories"
