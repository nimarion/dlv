from typing import Union

from fastapi import FastAPI
import sqlite3
from typing import Optional

app = FastAPI(title="DLV", docs_url="/swagger",
              openapi_url="/swagger-json", redoc_url=None)


def create_connection():
    conn = sqlite3.connect("file:stammdaten.db?mode=ro",
                           uri=True, isolation_level='IMMEDIATE')
    return conn


def query_db(query, args=(), one=False):
    cur = create_connection().cursor()
    cur.execute(query, args)
    r = [dict((cur.description[i][0], value)
              for i, value in enumerate(row)) for row in cur.fetchall()]
    cur.connection.close()
    return (r[0] if r else None) if one else r


@app.get("/clubs/{lv}")
def read_clubs_by_lv(lv: str, q: Union[str, None] = None):
    query = f"SELECT * FROM Club WHERE lv = '{lv}'"
    clubs = query_db(query)
    return clubs


@app.get("/lv")
def read_lv():
    query = f"SELECT DISTINCT lv FROM Club"
    connection = create_connection()
    lv = connection.execute(query).fetchall()
    connection.close()
    lv = [item for t in lv for item in t]
    return lv


@app.get("/athletes/{guid}")
def get_athlete_by_guid(guid: str):
    query = f"SELECT * FROM Athlete WHERE guid = '{guid}'"
    athlete = query_db(query)
    if (len(athlete) == 0):
        return None
    return athlete[0]


@app.get("/athletes")
def get_athletes(
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    clubId: Optional[str] = None,
    worldAthleticsId: Optional[int] = None,
    lv: Optional[str] = None,
    limit: Optional[int] = 100,
    page: Optional[int] = 0,
):
    query = "SELECT Athlete.*,C.name as club,lv FROM Athlete JOIN main.Club C on Athlete.clubId = C.id"

    conditions = []

    if firstname:
        conditions.append(f"firstname LIKE '%{firstname}%'")
    if lastname:
        conditions.append(f"lastname LIKE '%{lastname}%'")
    if clubId:
        conditions.append(f"clubId = '{clubId}'")
    if worldAthleticsId:
        conditions.append(f"worldAthleticsId = '{worldAthleticsId}'")
    if lv:
        conditions.append(f"lv = '{lv}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if (limit > 100):
        limit = 100

    query += f" LIMIT {limit} OFFSET {page * limit}"

    athletes = query_db(query)
    return athletes
