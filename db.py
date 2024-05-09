from sqlmodel import create_engine, SQLModel, Session, select
import mysql.connector
import io
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv() #Loads environment variables
MYSQL_HOST          = os.environ['MYSQL_HOST']
MYSQL_USER         = os.environ['MYSQL_USER']
MYSQL_PASSWORD     = os.environ['MYSQL_PASSWORD']
MYSQL_PORT              = os.environ['MYSQL_PORT']

mydb = mysql.connector.connect(
  host=MYSQL_HOST,
  user=MYSQL_USER,
  password=MYSQL_PASSWORD,
  port=MYSQL_PORT,
  database='ProductsDatabase'
)

# engine = create_engine(
#     "sqlite:///warships.db",
#     connect_args={"check_same_thread": False}, # only for sqlite
#     echo=True # Log Generated SQL
# )
engine = create_engine(
    "mysql+mysqlconnector://"+MYSQL_USER+":"+MYSQL_PASSWORD+"@"+MYSQL_HOST+":"+MYSQL_PORT+"/ProductsDatabase"
    #echo=True # Log Generated SQL
)

def get_session():
    with Session(engine) as session:
        yield session
