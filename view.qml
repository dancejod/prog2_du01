import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14
import QtQuick.Layouts 1.15

ColumnLayout {
	implicitWidth: 1280
	implicitHeight: 760	
	anchors.fill: parent
    property var currentModelItem;
    
    RowLayout {
        Layout.fillWidth: true

        

        ListView {
            id: settlementList
            width: 250
            Layout.fillHeight: true
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
            Plugin {
            id: mapPlugin
            name: "osm"
            PluginParameter {
                name:"osm.mapping.custom.host"
                value:"https://maps.wikimedia.org/osm/"
            }
        }

        Map {
            Layout.fillWidth: true
            Layout.fillHeight: true

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
            MapItemView {
                model: settlementListModel
                delegate: MapQuickItem {
                    coordinate: model.location
                    sourceItem: Rectangle {
                        width: 10
                        height: width
                        color: "red"
                        border.color: "black"
                        border.width: 1
                        radius: width*0.5
                    }
                    
                }
            }        
        }

        Column {
            Text {
                text: currentModelItem.display
                font.bold: true
            }
            Text {
                text: currentModelItem.township
            }
            
            Text {
                textFormat: Text.RichText
                text: "Rozloha: "+currentModelItem.area+" km<sup>2</sup>"
            }
            
            Text {
                    text:"Počet obyvatel: "+currentModelItem.population
            }

            Text {
                    text:"Okres: " +currentModelItem.district
            }

            Text {
                    text:"Kraj: "+currentModelItem.region
            }
        }

    }
}
