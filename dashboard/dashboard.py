from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000)

from sqlalchemy import create_engine
from sqlalchemy import text

DB_PATH = "sqlite:///data/waste_management.db"

engine = create_engine(DB_PATH)

def create_database():

    with engine.connect() as conn:

        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS waste_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            bin_id TEXT,

            location TEXT,

            distance REAL,

            fill_percentage REAL,

            status TEXT,

            priority TEXT,

            alert TEXT
        )
        """))

        conn.commit()

def insert_record(data):

    with engine.connect() as conn:

        conn.execute(
            text("""
            INSERT INTO waste_data
            (
                timestamp,
                bin_id,
                location,
                distance,
                fill_percentage,
                status,
                priority,
                alert
            )
            VALUES
            (
                :timestamp,
                :bin_id,
                :location,
                :distance,
                :fill_percentage,
                :status,
                :priority,
                :alert
            )
            """),
            data
        )

        conn.commit()