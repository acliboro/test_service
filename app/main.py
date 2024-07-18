import gzip
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.params import Body
from pydantic import BaseModel

from random import randrange
import psycopg2
import pandas as pd
from psycopg2.extras import RealDictCursor
import time
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import mode
from . import models, schemas
from .database import engine, get_db
from .routers import post, user, sid

models.Base.metadata.create_all(bind=engine)

# Load Security Master from Database

# print("Reading Parquet File")
# read_start_time = datetime.utcnow()
# df = pd.read_parquet('/q/cw/coredata/data/prod/na/4.64/sm/equ_sec_master.parq')
# read_end_time = datetime.utcnow()
# print(f"Time elapsed: {read_end_time-read_start_time}")
# print("Writing csv file")
# write_start_time = datetime.utcnow()
# df.to_csv("equ_sec_master.csv.gz", index=False, compression="gzip")
# write_end_time = datetime.utcnow()
# print(f"Time elapsed: {write_end_time-write_start_time}")
# # df.to_sql('testsecuritymaster', engine, if_exists='replace', index=False)
# print("DONE transferring")

# raw_conn = engine.raw_connection()
# cur = raw_conn.cursor()

# with gzip.open('/q/home/ph.amiel.liboro/amiel_scripts/sidservice/equ_sec_master.csv.gz', 'rt') as input_file:
#     headers = input_file.readline()
#     header_col = headers.rstrip()
#     table_name = 'testsecuritymaster'
#     table_columns = f"{table_name} ({header_col})"
#     copy_sql = """
#            COPY %s FROM stdin WITH CSV HEADER
#            DELIMITER as ','
#            """
#     cur.copy_expert(sql=copy_sql % table_columns, file=input_file)
#     print("Copy Start")
#     copy_start_time = datetime.utcnow()
#     raw_conn.commit()
#     copy_end_time = datetime.utcnow()
#     print(f"Time elapsed: {copy_end_time-copy_start_time}")
#     cur.close()

#     # next(input_file)
#     # cur.copy_from(input_file, 'testsecuritymaster', sep=',', quote='"')
#     print("DONE transferring")
#     input_file.close()

app = FastAPI()


# from sqlalchemy import create_engine
# engine = create_engine('your_connection_string')
# connection = engine.raw_connection()
# cursor = connection.cursor()


# while True:
#     try:
#         conn = psycopg2.connect(host='casfs-plus-node-prod-ph-amiel-liboro-fastapi.cnp5tdzehhhs.us-east-2.rds.amazonaws.com', database='fastapi', user='{username}', 
#             password='{password}', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connection was succesfull!")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error: ", error)
#         time.sleep(2)


# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
# {"title": "favorite foods", "content": "I like pizza", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i
@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(post.router)
# app.include_router(sid.router)
# app.include_router(user.router)
# app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Instrumentator().instrument(app).expose(app)


