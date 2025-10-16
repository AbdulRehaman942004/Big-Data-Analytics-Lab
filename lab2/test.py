# making connection to the database and testing if it is working
# using postgresql, mongodb, and elasticsearch (all are running locally on docker)

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from pymongo import MongoClient
from elasticsearch import Elasticsearch

# Load .env file
load_dotenv()

# Read values from .env
pg_user = os.getenv("POSTGRES_USER")
pg_password = os.getenv("POSTGRES_PASSWORD")
pg_db = os.getenv("POSTGRES_DB")
pg_port = os.getenv("POSTGRES_PORT", "5432")

mongo_port = os.getenv("MONGO_PORT", "27017")
elastic_port = os.getenv("ELASTIC_PORT", "9200")

# ==============================
# 1. Test PostgreSQL
# ==============================
try:
    engine = create_engine(f"postgresql+psycopg2://{pg_user}:{pg_password}@localhost:{pg_port}/{pg_db}")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ PostgreSQL connected:", result.fetchone())
except Exception as e:
    print("❌ PostgreSQL error:", e)

# ==============================
# 2. Test MongoDB
# ==============================
try:
    mongo_client = MongoClient(f"mongodb://localhost:{mongo_port}/")
    dbs = mongo_client.list_database_names()
    print("✅ MongoDB connected. Databases:", dbs)
except Exception as e:
    print("❌ MongoDB error:", e)

from elasticsearch import Elasticsearch

# ==============================
# 3. Test Elasticsearch
# ==============================
try:
    es = Elasticsearch(
        [f"http://localhost:{elastic_port}"],
        verify_certs=False,
        request_timeout=30
    )
    info = es.info()
    print("✅ Elasticsearch connected:", info.body)
except Exception as e:
    print("❌ Elasticsearch error:", e)
