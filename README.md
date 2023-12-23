# dlv

Stellt Athleten und Vereins Daten des Deutschen Leichtathletik Verbandes (DLV) als Rest API zur Verfügung. Die Daten werden aus den Dateien `base_athletes.json` und `base_clubs.json` welche durch TAF3 erzeugt werden in eine Sqlite Datenbank importiert. 

# API

- /lv - Listet alle Kürzel der Landesverbände auf
- /clubs/{lv} - Listet alle Vereine eines Landesverbandes auf
- /athletes/{guid} - Gibt die Daten eines Athleten zurück
- /athletes?firstname=?&lastname=?&clubId=?&worldAthleticsId=?&lv=?&limit=?&page=? - Sucht nach Athleten für die angegebenen Parameter. Die Parameter sind ale optional und können beliebig kombiniert werden. Die Parameter `limit` und `page` sind für die Paginierung der Ergebnisse gedacht. Maximal werden 100 Ergebnisse pro Seite zurückgegeben.

Stellt alle Athleten und Vereins Stammdaten als Rest API zur Verfügung. Die Datenbank wird durch die Datei `base_athletes.json`und `base_clubs.json` welche durch TAF3 erzeugt wird erzeugt. 

# Datenbank erstellen

Erstellt und aktualisiert wird die Datenbank durch ausführen des Skripts `taf2db.py` und angabe des Pfades zu den TAF3 Dateien.

```bash
python .\taf2db.py --taf 'C:\Users\Niklas Marion\Documents\TAF'
```

Die Sqlite Datenbank befindet sich nach dem Ausführen des Skripts in der Datei `stammdaten.db`.

# Server starten

Entwicklung:

```bash
uvicorn main:app --reload
```

Für den produktiven Einsatz existiert ein Dockerimage.

```bash
docker run -d \
    --name dlv \
    --restart=always \
    -v "$(pwd)/stammdaten.db:/code/stammdaten.db" \
    -p 80:80 \
    ghcr.io/nimarion/dlv:main
```

<p align="center">
  <img alt="Haha yes " width="250px" src="https://i.imgur.com/5bXJeZt.png">
  <br>
</p>