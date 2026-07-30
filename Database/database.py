from langgraph.checkpoint.postgres import PostgresSaver
from psycopg_pool import ConnectionPool
from dotenv import load_dotenv, find_dotenv
import os
import psycopg
load_dotenv(find_dotenv())


DB_URI = os.getenv("DB_URI")

_conn_kwargs = {
    "autocommit": True,
    "prepare_threshold": 0,
    "keepalives": 1,
    "keepalives_idle": 60,
    "keepalives_interval": 20,
    "keepalives_count": 5,
}

def create_checkpoint():
    try:
        with psycopg.connect(DB_URI, autocommit=True) as conn:
            checkpointer = PostgresSaver(conn)
            checkpointer.setup()

        pool = ConnectionPool(
            conninfo=DB_URI,
            max_size=5,
            kwargs=_conn_kwargs,
        )
        checkpointer = PostgresSaver(pool)

        return checkpointer
    except Exception as e:
        print(f"Error creating checkpoint: {e}")
        raise