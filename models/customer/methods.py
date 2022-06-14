from __future__ import annotations
from werkzeug.local import LocalProxy
from models.db import get_db
from dataclasses import dataclass, replace
from models.base import BaseModel


@dataclass
class Customer(BaseModel):
    id: int = None
    name: str = None
    email: str = None
    number: str = None
    address: str = None
    _hash: str = None
    _table_name: str = "customers"
