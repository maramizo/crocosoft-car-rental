from flask import Flask, _app_ctx_stack
from misc.converters import DateConverter


app = Flask(__name__)
app.url_map.converters['date'] = DateConverter
import models.customer.routes
import models.booking.routes
import models.vehicle.routes
import models.category.routes
import models.reports.routes



@app.teardown_appcontext
def terminate_db(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'mysql_db'):
        top.mysql_db.close()


if __name__ == '__main__':
    app.run()
