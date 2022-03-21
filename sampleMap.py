from PySide2.QtCore import Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide2.QtGui import QGuiApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtPositioning import QGeoCoordinate
from PySide2 import QtCore
from enum import Enum
import json
import sys
import typing

VIEW_URL = "view.qml"
SETTLEMENT_LIST = "sampleList.geojson"

class SettlementListModel(QAbstractListModel):
    
    # Deklaracia roli
    class Roles(Enum):
        LOC = QtCore.Qt.UserRole+0
        POP = QtCore.Qt.UserRole+1
        AREA = QtCore.Qt.UserRole+2
        DISTRICT = QtCore.Qt.UserRole+3
        REGION = QtCore.Qt.UserRole+4
        IS_CITY = QtCore.Qt.UserRole+5

    # Inicializacia potrebnych prvkov
    # Plan je do filtered_list prihadzovat a odoberat veci, ktore splnaju nase poziadavky, ten potom bude zodpovedny za display    
    def __init__(self, filename=None):
        QAbstractListModel.__init__(self)
        self.settlement_list = {}
        self.filtered_list = {}
        self.district_list = []
        self.region_list = []
        self.current_region = "všechny"
        self.current_districts = []
        self.current_district = ''
        self.district_region_dict = {}
        self._min_slider = 0
        self._max_slider = 1267449
        self.settlement_type_city = True
        self.settlement_type_village = True
        self._valid_districts = "všechny"
        self._selected_region = "všechny"

        if filename:
            self.load_from_json(filename)
            self.get_district_region_lists()
    
    # Nacitanie dat a korekcia geometrie
    def load_from_json(self, filename):
        with open (filename, encoding = "utf-8") as file:
            self.settlement_list = json.load(file)
            self.filtered_list["features"] = []
            i = 0
            for entry in self.settlement_list["features"]:
                lon = entry["geometry"]["coordinates"][0]
                lat = entry["geometry"]["coordinates"][1]
                entry["geometry"]["coordinates"] = QGeoCoordinate(float(lat), float(lon))

            # Vytvorenie kopie nacitanych dat, s filtered list potom manipulovat odoberanim/prihadzovanim ziadanych dat
               
                self.beginInsertRows(self.index(0).parent(), i, i)
                self.filtered_list["features"].append(entry)
                self.endInsertRows()
                i = +1

            self.settlement_list["features"] = sorted(self.settlement_list["features"], key=lambda d: d["properties"]["NAZ_OBEC"])
            self.filtered_list["features"] = sorted(self.filtered_list["features"], key=lambda d: d["properties"]["NAZ_OBEC"])

    # Metoda na manipulaciu s riadkami
    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.filtered_list["features"])
        
    # Priradenie hodnot k rolam, zaokruhlenie plochy na 2 desatinne miesta
    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_OBEC"]
        elif role == self.Roles.LOC.value: 
            return self.filtered_list["features"][index.row()]["geometry"]["coordinates"]
        elif role == self.Roles.POP.value:
            return self.filtered_list["features"][index.row()]["properties"]["POCET_OBYV"]
        elif role == self.Roles.AREA.value:
            return round(self.filtered_list["features"][index.row()]["properties"]["area"], 2)
        elif role == self.Roles.DISTRICT.value:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_OKRES"]
        elif role == self.Roles.REGION.value:
            return self.filtered_list["features"][index.row()]["properties"]["NAZ_KRAJ"]
        elif role == self.Roles.IS_CITY.value:
            if self.filtered_list["features"][index.row()]["properties"]["is_city"] == "TRUE":
                return "Město"
            else:
                return "Obec" 

    # Pomenovanie roli tak, ako budu zobrazovane v qml
    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.LOC.value] = QByteArray(b"location")
        roles[self.Roles.POP.value] = QByteArray(b"population")
        roles[self.Roles.AREA.value] = QByteArray(b"area")
        roles[self.Roles.DISTRICT.value] = QByteArray(b"district")
        roles[self.Roles.REGION.value] = QByteArray(b"region")
        roles[self.Roles.IS_CITY.value] = QByteArray(b"township")
        print(roles)
        return roles

    # Ziskanie zoznamov krajov a okresov, naplnenie slovnika: klucom su kraje, hodnotami su zoznamy okresov, ktore ku krajom patria
    # Na konci metody mimo cyklu pridany atribut "všechny" pre zobrazenie vsetkeho
    def get_district_region_lists(self):
        
        self.region_list.append("všechny")
        self.district_list.append("všechny")

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
        
        self.district_region_dict["všechny"] = self.district_list
        self.current_districts = self.district_list

    # Gettery, settery a properties pre slidere, mesta, obce
    # Mesta a obce pracuju s valeanom, pretoze mame len T/F
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
        return self.settlement_type_city

    def set_cities(self, val):
        if val != self.show_cities:
            self.settlement_type_city = val
            self.show_cities_changed.emit()
    
    show_cities_changed = Signal()
    show_cities = Property(bool, get_cities, set_cities, notify=show_cities_changed)

    def get_villages(self):
        return self.settlement_type_village

    def set_villages(self, val):
        if val != self.show_villages:
            self.settlement_type_village = val
            self.show_villages_changed.emit()
    
    show_villages_changed = Signal()
    show_villages = Property(bool, get_villages, set_villages, notify=show_villages_changed)

    def get_districts(self):
        return self.current_districts

    def set_districts(self, val):
        if val != self.valid_districts:
            self.current_districts = val
        self.current_districts_changed.emit()
    
    current_districts_changed = Signal()
    valid_districts = Property(list, get_districts, set_districts, notify=current_districts_changed)

    def get_region(self):
        return self.current_region

    def set_region(self, val):
        if val != self.selected_region:
            self.current_region = val
            self.valid_districts = self.district_region_dict[val]
        self.current_region_changed.emit()
    
    current_region_changed = Signal()
    selected_region = Property(str, get_region, set_region, notify=current_region_changed)

    def get_list_of_regions(self):
        return self.region_list

    def set_list_of_regions(self, val):
        if val != self.list_of_regions:
            self.region_list = val
        self.list_of_regions_changed.emit()

    list_of_regions_changed = Signal()
    list_of_regions = Property(list, get_list_of_regions, set_list_of_regions, notify=list_of_regions_changed)

    def get_selected_district(self):
        return self.current_district

    def set_selected_district(self, val):
        if val != self.sel_district:
            self.current_district = val
        self.selected_district_changed.emit()

    selected_district_changed = Signal()
    sel_district = Property(str, get_selected_district, set_selected_district, notify=selected_district_changed)

    def clear_filter(self) -> None:
        self.beginRemoveRows(self.index(0).parent(), 0, self.rowCount()-1)
        self.filtered_list["features"] = []
        self.endRemoveRows()

    # Handler pre checkboxy, treba vymysliet; plan je zaplnovat filtered_list tym, co tu bude zavolane
    @Slot()
    def filter(self):
        self.clear_filter()
        i = 0
        
        for settlement in self.settlement_list["features"]:
            if self.selected_region == settlement["properties"]["NAZ_KRAJ"] or self.selected_region == "všechny":
                if self.sel_district == settlement["properties"]["NAZ_OKRES"] or self.sel_district == "všechny":
                    if self.show_cities:
                        value = settlement["properties"]["is_city"]
                        if value == "TRUE":
                            if self.max_slider >= settlement["properties"]["POCET_OBYV"] >= self.min_slider:
                                self.beginInsertRows(self.index(0).parent(), i, i)
                                self.filtered_list["features"].append(settlement)
                                self.endInsertRows()
                                i += 1
            
                    if self.show_villages:
                        value = settlement["properties"]["is_city"]
                        if value == "FALSE":
                            if self.max_slider >= settlement["properties"]["POCET_OBYV"] >= self.min_slider:
                                self.beginInsertRows(self.index(0).parent(), i, i)
                                self.filtered_list["features"].append(settlement)
                                self.endInsertRows()
                                i += 1

    @Slot()
    def live_filter_r_d(self):
        self.clear_filter()
        i = 0
        
        for settlement in self.settlement_list["features"]:
            if self.selected_region == settlement["properties"]["NAZ_KRAJ"] or self.selected_region == "všechny":
                if self.sel_district == settlement["properties"]["NAZ_OKRES"] or self.sel_district == "všechny":
                    if self.show_cities:
                        value = settlement["properties"]["is_city"]
                        if value == "TRUE":
                            if self.max_slider >= settlement["properties"]["POCET_OBYV"] >= self.min_slider:
                                self.beginInsertRows(self.index(0).parent(), i, i)
                                self.filtered_list["features"].append(settlement)
                                self.endInsertRows()
                                i += 1
            
                    if self.show_villages:
                        value = settlement["properties"]["is_city"]
                        if value == "FALSE":
                            if self.max_slider >= settlement["properties"]["POCET_OBYV"] >= self.min_slider:
                                self.beginInsertRows(self.index(0).parent(), i, i)
                                self.filtered_list["features"].append(settlement)
                                self.endInsertRows()
                                i += 1
        
    
# Inicializacia aplikacie
app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
settlementlist_model = SettlementListModel(SETTLEMENT_LIST)
ctxt = view.rootContext()
ctxt.setContextProperty("settlementListModel", settlementlist_model)
view.setSource(url)
view.show()
app.exec_()