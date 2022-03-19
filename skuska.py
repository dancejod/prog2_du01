import json
from PySide6.QtPositioning import QGeoCoordinate

settlement_list = []
district_list = []
with open ("sampleList.geojson", encoding = "utf-8") as file:
    settlement_list = json.load(file)

    for entry in settlement_list["features"]:
        lat = entry["geometry"]["coordinates"][0]
        lon = entry["geometry"]["coordinates"][1]
        entry["geometry"]["coordinates"] = QGeoCoordinate(float(lat), float(lon))


def get_district_list():
    for okres in range(len(settlement_list["features"])):
        if settlement_list["features"][okres]["properties"]["NAZ_OKRES"] not in district_list:
            district_list.append(settlement_list["features"][okres]["properties"]["NAZ_OKRES"])
    print(district_list)
    print(len(district_list))
get_district_list()