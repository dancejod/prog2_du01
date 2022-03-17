from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QAbstractListModel, QByteArray
from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView
from PySide6.QtPositioning import QGeoCoordinate
from PySide6 import QtCore
from enum import Enum
import json
import sys
import typing

VIEW_URL = "view.qml"
SETTLEMENT_LIST = "sampleList.geojson"


app = QGuiApplication(sys.argv)
view = QQuickView()
url = QUrl(VIEW_URL)