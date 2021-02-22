from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask import g

load_dotenv()

# connect to database using env variable
# The engine variable manages the overall connection to the database.
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
# The Session variable generates temporary connections for performing create, read, update, and delete (CRUD) operations.
Session = sessionmaker(bind=engine)
# The Base class variable helps us map the models to real MySQL tables.
Base = declarative_base()

def init_db(app):
  Base.metadata.create_all(engine)

  app.teardown_appcontext(close_db)

def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()

  return g.db

# The pop() method attempts to find and remove db from the g object. If db exists (that is, db doesn't equal None), then db.close() will end the connection.
# The close_db() function won't run automatically, though. We need to tell Flask to run it whenever a context is destroyed.
# So in the same db/__init__.py file, update the init_db() function to look like the following code. Line 18
def close_db(e=None):
  db = g.pop('db', None)

  if db is not None:
    db.close()