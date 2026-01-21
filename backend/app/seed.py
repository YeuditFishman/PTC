from app.database import SessionLocal, engine, Base
from app.db_utils import run_seed
from app.csv_utils import read_csv_data
import os

Base.metadata.create_all(bind=engine)

data_file = os.getenv("EXR_DATA_FILE")
data = list(read_csv_data(data_file))

db = SessionLocal()
run_seed(db, data)
db.close()
