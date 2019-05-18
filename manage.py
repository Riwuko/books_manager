import sys
sys.path.append('app/')

from main import app, db

app.app_context().push()
db.create_all()
