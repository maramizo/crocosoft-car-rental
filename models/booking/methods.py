from __future__ import annotations
from datetime import datetime
import MySQLdb
from werkzeug.local import LocalProxy
from models.db import get_db
from dataclasses import dataclass, replace
from models.base import BaseModel


@dataclass
class Booking(BaseModel):
    id: int = None
    vehicle_id: int = None
    customer_id: int = None
    hire_date: datetime | str = None
    end_date: datetime | str = None
    confirmed: bool = False
    _table_name: str = "bookings"

    def __post_init__(self):
        if type(self.hire_date) is str:
            self.hire_date = datetime.strptime(self.hire_date, "%Y-%m-%dT%H:%M:%S")
        if type(self.end_date) is str:
            self.end_date = datetime.strptime(self.end_date, "%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def get_created_today() -> list:
        """
        Get all bookings created today
        """
        cur = LocalProxy(get_db).cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute("SELECT id, vehicle_id, customer_id, hire_date, end_date, confirmed FROM bookings WHERE DATE(hire_date) = DATE(%s)", (datetime.now(),))
        return [Booking(**r) for r in cur.fetchall()]
