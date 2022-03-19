import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14
import QtQuick.Layouts 1.15

RowLayout {
	implicitWidth: 1280
	implicitHeight: 760	
	anchors.fill: parent
    property var currentModelItem;
    
    ColumnLayout {
		width: 200 		// width as parent
		height: parent.height	// height as CheckBox

        Column {
            width: parent.width
            height:500
            spacing:20

            Row {
                spacing: 5

			CheckBox {
                id: citiesChecked
				text: "Města"	// only `display` clashes with CheckBox property
				checkable: true		// users can check
                checked : true
				onCheckStateChanged: settlementListModel._settlement_type_city =  citiesChecked.checked
			}
        
            CheckBox {
                id: villagesChecked
				text: "Vesnice"	// only `display` clashes with CheckBox property
				checkable: true		// users can check
                checked : true
				onCheckStateChanged: settlementListModel._settlement_type_village =  villagesChecked.checked
            }
        }
    
        RangeSlider {
                    id: rangeSlider
                    from: 0
                    to: 1267449
                    first.value: settlementListModel.min_slider
                    second.value: settlementListModel.max_slider
                    Component.onCompleted: {
                            rangeSlider.setValues(0, 1267449)
                    }
                    Binding {
                        target: settlementListModel
                        property: "min_slider"
                        value: rangeSlider.first.value
                    }
                    Binding {
                        target: settlementListModel
                        property: "max_slider"
                        value: rangeSlider.second.value
                    }

                }
        }
    }    
    

    RowLayout {
        Layout.fillWidth: true

        ListView {
            id: settlementList
            width: 250
            height: 500
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
                        onClicked: settlementList.currentIndex = index-500+parent.height
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
                            text: currentModelItem.display
                            color: {
                                color = "black"
                                if (currentModelItem.township == "Město")
                                    color = "red"
                            }
                            font.bold: {
                                font.bold = false
                                if (currentModelItem.township == "Město")
                                    font.bold = true
                            }                        
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
