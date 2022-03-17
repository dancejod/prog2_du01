import json
from PySide6.QtPositioning import QGeoCoordinate

settlement_list = []

with open ("sampleList.geojson", encoding = "utf-8") as file:
    settlement_list = json.load(file)

    for entry in settlement_list["features"]:
        lat = entry["geometry"]["coordinates"][0]
        lon = entry["geometry"]["coordinates"][1]
        entry["geometry"]["coordinates"] = QGeoCoordinate(float(lat), float(lon))
        print(entry["geometry"]["coordinates"])
