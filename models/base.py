import json
import typing
from abc import ABC
from dataclasses import replace

import MySQLdb
from werkzeug.local import LocalProxy
from models.db import get_db

T = typing.TypeVar('T', bound='BaseModel')


class BaseModel(ABC):
    def keys(self) -> [str]:
        """
        Returns the non-private keys of the object.
        :return: A list of keys.
        """
        return [x for x in self.__dict__.keys() if x[0] != '_']

    def dict(self) -> dict:
        """
        Returns the object as a dictionary.
        Properties that start with an _ are not included.
        """
        return {x: val for x, val in self.__dict__.items() if x[0] != '_'}

    def get(self: T) -> T | None:
        """
        Get a model by id.
        Keys that start with an _ are not included, they are considered private.

        :return: The model or None if not found.
        """
        cur = LocalProxy(get_db).cursor(cursorclass=MySQLdb.cursors.DictCursor)
        cur.execute(
            f"SELECT {','.join(self.keys())} FROM {self._table_name} WHERE id = %s",
            (self.id,)
        )
        result = cur.fetchone()
        if result:
            return replace(self, **dict(result))
        return None

    def update(self: T) -> T:
        """
        Update a model by id

        :return: The updated model
        """
        keys = ['%s = %%s' % k for k in self.keys()]
        values = [self.__dict__[k] for k in self.keys()]
        LocalProxy(get_db).cursor().execute(
            f"UPDATE {self._table_name} SET %s WHERE id = %s" % (', '.join(keys), self.id), tuple(values)
        )
        LocalProxy(get_db).commit()
        return self

    def save(self: T) -> T:
        """
        Create a new booking
        """
        if self.id:
            return self.update()
        else:
            cur = LocalProxy(get_db).cursor()
            values = [self.__dict__[k] for k in self.keys()]
            cur.execute(
                f"INSERT INTO {self._table_name} ({','.join(self.keys())}) VALUES ({','.join(['%s' for _ in self.keys()])})",
                values
            )
            LocalProxy(get_db).commit()
            return replace(self, id=cur.lastrowid)

    def delete(self: T) -> None:
        """
        Delete a model by id
        """
        LocalProxy(get_db).cursor().execute(
            f"DELETE FROM {self._table_name} WHERE id = %s",
            (self.id,)
        )
        LocalProxy(get_db).commit()

    def jsonify(self):
        """
        Returns the object in a JSON format.
        Properties that start with an _ are not included.
        """
        return json.dumps({x: val for x, val in self.__dict__.items() if x[0] != '_'}, default=str)
