from application import app
from models import db
from routes import *
app.app_context().push()

db.create_all()
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
