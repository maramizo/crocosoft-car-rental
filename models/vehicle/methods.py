from __future__ import annotations

from datetime import datetime

import MySQLdb
from werkzeug.local import LocalProxy
from models.db import get_db
from dataclasses import dataclass, replace
from models.base import BaseModel


@dataclass
class Vehicle(BaseModel):
    id: int = None
    name: str = None
    category_id: int = None
    price_per_day: float = None
    _table_name: str = "vehicles"

    def get_available(self, date: datetime) -> [Vehicle]:
        """
        Get all available vehicles.
        """
        cur = LocalProxy(get_db).cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute(
            f"SELECT {self.keys()} FROM vehicles WHERE id NOT IN (SELECT vehicle_id FROM bookings "
            "WHERE (hire_date <= %s AND end_date >= %s AND confirmed IS TRUE))",
            (date, date)
        )
        return [replace(self, **dict(x)) for x in cur.fetchall()]
