from PySide2.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
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
        if filename:
            self.load_from_json(filename)

    def load_from_json(self, filename):
        with open (filename, encoding = "utf-8") as file:
            self.settlement_list = json.load(file)

            for entry in self.settlement_list["features"]:
                lon = entry["geometry"]["coordinates"][0]
                lat = entry["geometry"]["coordinates"][1]
                entry["geometry"]["coordinates"] = QGeoCoordinate(float(lon), float(lat))
    
    def rowCount(self, parent:QtCore.QModelIndex=...) -> int:
        return len(self.settlement_list["features"])
        

    def data(self, index:QtCore.QModelIndex, role:int=...) -> typing.Any:
        if role == QtCore.Qt.DisplayRole:
            return self.settlement_list["features"][index.row()]["properties"]["NAZ_OBEC"]
        elif role == self.Roles.LOC.value: 
            return self.settlement_list["features"][index.row()]["geometry"]["coordinates"]
        elif role == self.Roles.POP.value:
            return self.settlement_list["features"][index.row()]["properties"]["POCET_OBYV"]
        elif role == self.Roles.AREA.value:
            return round(self.settlement_list["features"][index.row()]["properties"]["area"],2)
        """
        elif role == self.Roles.DISTRICT.value:
            return self.settlement_list["features"]["properties"][index.row()]["NAZ_OKRES"]
        elif role == self.Roles.REGION.value:
            return self.settlement_list["features"]["properties"][index.row()]["NAZ_KRAJ"]
        elif role == self.Roles.IS_CITY.value:
            return self.settlement_list["features"]["properties"][index.row()]["is_city"]
        """


    def roleNames(self) -> typing.Dict[int, QByteArray]:
        roles = super().roleNames()
        roles[self.Roles.LOC.value] = QByteArray(b'location')
        roles[self.Roles.POP.value] = QByteArray(b'population')
        roles[self.Roles.AREA.value] = QByteArray(b'area')
        print(roles)
        return roles

app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)
settlementlist_model = SettlementListModel(SETTLEMENT_LIST)
ctxt = view.rootContext()
ctxt.setContextProperty('settlementListModel', settlementlist_model)
view.setSource(url)
view.show()
app.exec_()
print (len(settlement_list))