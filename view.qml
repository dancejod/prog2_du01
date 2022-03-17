import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14

Row {
    width: 800
    height: 500

    property var currentModelItem;

    ListView {
        id: settlementList
        width: 250
        height: parent.height
        focus: true

        Component {
            id: settlementListDelegate
            Item {
                width: parent.width
                height: childrenRect.height
                Text {
                    text: model.display
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: settlementList.currentIndex = index
                }
            }
        }

        model: DelegateModel {
            id: settlementListDelegateModel
            model: settlementListModel
            delegate: settlementListDelegate
        }

        onCurrentItemChanged: currentModelItem = settlementListDelegateModel.items.get(settlementList.currentIndex).model

        highlight: Rectangle {
            color: "lightsteelblue"
        }
    }

    Column {
        Text {
            text: currentModelItem.township
        }
        Text {
            text: "Rozloha:"
        }
        Text {
            textFormat: Text.RichText
            text: currentModelItem.area+" km<sup>2</sup>"
        }
        Text {
            text: "Počet obyvatel"
        }
        Text {
                text: currentModelItem.population
        }
        Text {
            text: "Okres"
        }
        Text {
                text: currentModelItem.district
        }
        Text {
            text: "Kraj"
        }
        Text {
                text: currentModelItem.region
        }
    }

    Plugin {
        id: mapPlugin
        name: "osm"
        PluginParameter {
             name:"osm.mapping.custom.host"
             value:"https://maps.wikimedia.org/osm/"
        }
    }

    Map {
        width: 500
        height: parent.height

        plugin: mapPlugin
        activeMapType: supportedMapTypes[supportedMapTypes.length - 1]

        center: currentModelItem.location
        zoomLevel: 10

        MapItemView {
            model: settlementListModel
            delegate: MapQuickItem {
                coordinate: model.location
                sourceItem: Text {
                    text: model.display
                }
            }
        }
    }

}

