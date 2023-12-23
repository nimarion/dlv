import pandas as pd
import sqlite3
import os
from pathlib import Path
import argparse

def main(taf_path) -> None:
    conn = sqlite3.connect("stammdaten.db")

    clubs_path = Path(taf_path).joinpath("Settings/base_clubs.json")

    with open(clubs_path, encoding="utf-16-le", errors='ignore') as f:
        data = f.read()
        data = data[11:-1]
        with open('clubs.json', 'w', encoding="utf-8") as f:
            f.write(data)
        
        df = pd.read_json('clubs.json', encoding="utf-8-sig")
        df = df[["LV", "Name", "ShortName", "Code", "Type"]]
        df['Type'] = df['Type'].apply(lambda x: "CLUB" if x == 0 else "LG")

        df = df.drop(columns=['ShortName'])
        df = df.rename(columns={"LV": "lv", "Name": "name", "Code": "id", "Type": "type"})

        df.to_sql('Club', conn, if_exists='replace', index=False)
        os.remove('clubs.json')
    
    athletes_path = Path(taf_path).joinpath("Settings/base_athletes.json")

    with open(athletes_path, encoding="utf-16-le", errors='ignore') as f:
        data = f.read()
        data = data[11:-1]
        with open('athletes.json', 'w', encoding="utf-8") as f:
            f.write(data)
        
        df = pd.read_json('athletes.json', encoding="utf-8-sig")
        df['WorldAthleticsId'] = df['WorldAthleticsId'].fillna(0)
        
        df = df[df['Code'] != '']
        df = df[df['ExternalId'].notnull()]
        
        df = df[["ExternalId", "Code", "Firstname", "Lastname", "ClubCode", "Nation", "Yob", "Gender", "WorldAthleticsId"]]

        df['WorldAthleticsId'] = df['WorldAthleticsId'].apply(lambda x: None if x == 0 else int(x))
        df["Gender"] = df['Gender'].apply(lambda x: "M" if x == 0 else "W")

        df = df.rename(columns={"Code": "id", "ExternalId": "guid", "Firstname": "firstname", "Lastname": "lastname", "ClubCode": "clubId", "Nation": "country", "Yob": "birthyear", "Gender": "sex", "WorldAthleticsId": "worldAthleticsId" })

        df.to_sql('Athlete', conn, if_exists='replace', index=False)
        os.remove('athletes.json')
        

    conn.execute("DELETE FROM Athlete WHERE guid IN (SELECT guid FROM Athlete JOIN main.Club C on Athlete.clubId = C.id WHERE lv='')")
    conn.execute("DELETE FROM Club WHERE lv=''");
    conn.commit()
    conn.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--taf", required=True, dest="taf_path", help="Path to TAF folder")
    args = parser.parse_args()

    main(args.taf_path)