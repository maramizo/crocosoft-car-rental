from datetime import datetime
from werkzeug.routing import BaseConverter, ValidationError


class DateConverter(BaseConverter):
    """Extracts a ISO8601 date from the path and validates it."""

    regex = r'\d{4}-\d{2}-\d{2}:?\d{2}?:\d{2}?:\d{2}?'
    
    # Convert the date string to a datetime object.
    def to_python(self, value):
        try:
            return datetime.strptime(value, '%Y-%m-%d:%H:%M:%S')
        except ValueError:
            raise ValidationError()
        
    # Convert the datetime object to a string.
    def to_url(self, value):
        return value.strftime('%Y-%m-%d:%H:%M:%S')
