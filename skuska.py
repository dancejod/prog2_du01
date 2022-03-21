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
    print(district_list)


def live_filter_checkboxes(self):
    if self._settlement_type_city == True and self._settlement_type_village == True:
        settlement_city = self.settlement_list["features"][13]["properties"]["is_city"]
        settlement_village = self.settlement_list["features"][0]["properties"]["is_city"]
        if settlement_city not in self.filtered_list or settlement_village not in self.filtered_list:
            for entry in self.settlement_list:
                self.filtered_list["features"].append(self.settlement_list["features"][entry])
                