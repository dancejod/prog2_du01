from pickle import FALSE, TRUE
from threading import Lock
from tkinter import ALL
from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import json
import sys
import typing
import copy

VIEW_URL = "view.qml"
SETTLEMENT_LIST = "sampleList.geojson"

class SettlementListModel(QAbstractListModel):
    
    class Roles(Enum):
        LOC = QtCore.Qt.UserRole+0
        POP = QtCore.Qt.UserRole+1
        AREA = QtCore.Qt.UserRole+2
        DISTRICT = QtCore.Qt.UserRole+3
        REGION = QtCore.Qt.UserRole+4
        IS_CITY = QtCore.Qt.UserRole+5
        
    def __init__(self, filename=None):
        QAbstractListModel.__init__(self)
        self.settlement_list = []
        self.filtered_list = []
        self.district_list = []
        self.region_list = []
        self.district_region_dict = {}
        self._min_slider = 0
        self._max_slider = 1267449
        self._settlement_type_city = True
        self._settlement_type_village = True
        self._show_district = "all"
        self._show_region = "all"

        if filename:
            self.load_from_json(filename)
    
    def load_from_json(self, filename):
        with open (filename, encoding = "utf-8") as file:
            self.settlement_list = json.load(file)

            for entry in self.settlement_list["features"]:
                lon = entry["geometry"]["coordinates"][0]
                lat = entry["geometry"]["coordinates"][1]
                entry["geometry"]["coordinates"] = QGeoCoordinate(float(lat), float(lon))
    
            self.filtered_list = self.settlement_list.copy()

    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.settlement_list["features"])
        

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_OBEC"]
        elif role == self.Roles.LOC.value: 
            return self.filtered_list["features"][index.row()]["geometry"]["coordinates"]
        elif role == self.Roles.POP.value:
            return self.filtered_list["features"][index.row()]["properties"]["POCET_OBYV"]
        elif role == self.Roles.AREA.value:
            return round(self.filtered_list["features"][index.row()]["properties"]["area"],2)
        elif role == self.Roles.DISTRICT.value:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_OKRES"]
        elif role == self.Roles.REGION.value:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_KRAJ"]
        elif role == self.Roles.IS_CITY.value:
            if self.filtered_list["features"][index.row()]["properties"]["is_city"] == "TRUE":
                return "Město"
            else:
                return "Vesnice" 
            #return self.settlement_list["features"][index.row()]["properties"]["is_city"]


    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.LOC.value] = QByteArray(b'location')
        roles[self.Roles.POP.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        roles[self.Roles.DISTRICT.value] = QByteArray(b'district')
        roles[self.Roles.REGION.value] = QByteArray(b'region')
        roles[self.Roles.IS_CITY.value] = QByteArray(b'township')
        print(roles)
        return roles

    def get_district_region_lists(self):
        for record in range(len(self.settlement_list["features"])):

            district_name = self.settlement_list["features"][record]["properties"]["NAZ_OKRES"]
            region_name = self.settlement_list["features"][record]["properties"]["NAZ_KRAJ"]

            if district_name not in self.district_list:
                self.district_list.append(district_name)
            if region_name not in self.region_list:
                self.region_list.append(region_name)

            if region_name not in self.district_region_dict.keys():
                self.district_region_dict[region_name] = []
            else:
                if district_name not in self.district_region_dict[region_name]:
                    self.district_region_dict[region_name].append(district_name)

        self.region_list.append("all")
        self.district_region_dict["all"] = self.district_list

    def get_min_slider(self):
        return self._min_slider

    def set_min_slider(self, val):
        if val != self.min_slider:
            self._min_slider = val
            self.min_slider_changed.emit()
    
    min_slider_changed = Signal()
    min_slider = Property(int, get_min_slider, set_min_slider, notify=min_slider_changed)

    def get_max_slider(self):
        return self._max_slider

    def set_max_slider(self, val):
        if val != self.max_slider:
            self._max_slider = val
            self.max_slider_changed.emit()
    
    max_slider_changed = Signal()
    max_slider = Property(int, get_max_slider, set_max_slider, notify=max_slider_changed)

    def get_cities(self):
        return self._settlement_type_city

    def set_cities(self, bool):
        if bool != self.show_cities:
            self._settlement_type_city = bool
            self.show_cities_changed.emit()
    
    show_cities_changed = Signal()
    show_cities = Property(bool, get_max_slider, set_max_slider, notify=show_cities_changed)

    def get_villages(self):
        return self._settlement_type_village

    def set_villages(self, bool):
        if bool != self.show_villages:
            self._settlement_type_village = bool
            self.show_villages_changed.emit()
    
    show_villages_changed = Signal()
    show_villages = Property(bool, get_max_slider, set_max_slider, notify=show_villages_changed)

    @Slot(bool)
    def city_checkbox_handler(self, bool):
        pass



app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
settlementlist_model = SettlementListModel(SETTLEMENT_LIST)
ctxt = view.rootContext()
ctxt.setContextProperty('settlementListModel', settlementlist_model)
view.setSource(url)
view.show()
app.exec_()