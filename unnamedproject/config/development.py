import os

# Enable debug mode.
DEBUG = True

# Connect to the database
if not 'DBHOST' in os.environ:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_database.db'
else:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.environ['DBUSER'],
        dbpass=os.environ['DBPASS'],
        dbhost=os.environ['DBHOST'],
        dbname=os.environ['DBNAME']
    )

# Turn off the Flask-SQLAlchemy event system and warning
SQLALCHEMY_TRACK_MODIFICATIONS = False
