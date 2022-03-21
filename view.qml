import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQml.Models 2.1
import QtLocation 5.14
import QtPositioning 5.14
import QtQuick.Layouts 1.15

RowLayout {
	
	anchors.fill: parent
    property var currentModelItem;
    

        Column {
            id:main_column
            anchors.fill: parent
            Layout.minimumWidth: 210
            Rectangle{
                id:first_rectangle
                Row {
                    spacing: 20
                
                    
                    CheckBox {
                        id: citiesChecked
                        text: qsTr("Města")
                        checkable: true
                        checked : true
                        onCheckStateChanged: settlementListModel.show_cities = citiesChecked.checked
                    }
                
                    CheckBox {
                        id: villagesChecked
                        text: qsTr("Vesnice")
                        checkable: true	
                        checked : true
                        onCheckStateChanged: settlementListModel.show_villages = villagesChecked.checked
                    }
                    
                }    

            }
            Rectangle {
                id: second_rectangle
                anchors.top: first_rectangle.bottom
                anchors.topMargin: 50
                Text{
                    id:heading_rangeslider
                    text:"Počet obyvatel: "
                }
                RangeSlider {
                    id: rangeSlider
                    from: 0
                    to: 1267449
                    first.value: settlementListModel.min_slider
                    second.value: settlementListModel.max_slider
                    Layout.alignment: Qt.AlignHCenter
                    anchors.top: heading_rangeslider.bottom
                    
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
        RowLayout {
            anchors.top: second_rectangle.bottom
            anchors.topMargin: 70
            
            Label {
                text: "Od: "
            }
            TextInput {
                id: minSliderInput
                text: settlementListModel.min_slider
                Binding {
                    target: settlementListModel
                    property: "min_slider"
                    value: minSliderInput.text
                }
            }
            
       
            Label {
                text: "Do: "
            }
            TextInput {
                id: maxSliderInput
                text: settlementListModel.max_slider
                Binding {
                    target: settlementListModel
                    property: "max_slider"
                    value: maxSliderInput.text
                }
            }    
    
        }
    }
        Rectangle {
            id: third_rectangle
            anchors.top: second_rectangle.bottom
            anchors.topMargin: 100

            Button {
                Layout.alignment: Qt.AlignHCenter
                anchors.topMargin: 150
                id: filterButton
                text: "Filter"

                onClicked: {
                    settlementListModel.filter()
                    settlementListModel.currentIndex = -1
                    mapSettlements.fitViewportToVisibleMapItems()

                }
            }

        }
        Rectangle {
            id: fourth_rectangle
            anchors.top: third_rectangle.bottom
            anchors.topMargin: 80

            Column {
                spacing: 5
                
                Text {
                    id: combo_region_label
                    text: "Kraj:"
                }

                ComboBox {
                    id: combo_region
                    model: settlementListModel.list_of_regions
                    onActivated: {
                        settlementListModel.selected_region = settlementListModel.list_of_regions[currentIndex]
                        settlementListModel.live_filter_r_d()
                        }
                }

                Text {
                    id: combo_district_label
                    text: "Okres:"
                }

                ComboBox {
                    id: combo_district
                    model: settlementListModel.valid_districts
                    onActivated: {
                        settlementListModel.sel_district = settlementListModel.valid_districts[currentIndex]
                        settlementListModel.live_filter_r_d()
                    }
                }
            }
        }
        Rectangle {
            id: fifth_rectangle
            anchors.top: fourth_rectangle.bottom
            anchors.topMargin: 150
            width: 250
            height: 400
            
            ListView {
                id: settlementList
                width: parent.width
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
        }
        Rectangle {
            id: sixth_rectangle
            anchors.top: fifth_rectangle.bottom
            anchors.topMargin:50
           
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
       
    RowLayout {
        Layout.fillWidth: true

        
            Plugin {
            id: mapPlugin
            name: "osm"
            PluginParameter {
                name:"osm.mapping.custom.host"
                value:"https://maps.wikimedia.org/osm/"
            }
        }

        Map {
            id: mapSettlements
            Layout.fillWidth: true
            Layout.fillHeight: true

            plugin: mapPlugin
            activeMapType: supportedMapTypes[supportedMapTypes.length - 1]

            center: currentModelItem.location
            zoomLevel: 12

            MapItemView {
                model: settlementListModel
                
                delegate: MapQuickItem {
                    coordinate: model.location
                        anchorPoint.x: -10
                        anchorPoint.y: -5
                    sourceItem: Text {
                        text: model.display
                        color: {
                            if (model.township == "Město")
                                color = "red"
                            if (model.township == "Obec")
                                color = "black"
                            
                        }
                        font.bold: {
                            font.bold = false
                            if (model.township == "Město")
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

    }
}
