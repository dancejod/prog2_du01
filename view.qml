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
                        text: qsTr("Města")	// only `display` clashes with CheckBox property
                        checkable: true		// users can check
                        checked : true
                        onCheckStateChanged: {
                            if settlementListModel.live_filter_checkboxes()
                    }
                
                    CheckBox {
                        id: villagesChecked
                        text: qsTr("Vesnice")	// only `display` clashes with CheckBox property
                        checkable: true		// users can check
                        checked : true
                        onCheckStateChanged: settlementListModel.live_filter_checkboxes()
                    }
                    Binding {
                        target: settlementListModel
                        property: "show_cities"
                        value: citiesChecked.checked
        }
                    Binding {
                        target: settlementListModel
                        property: "show_villages"
                        value: villagesChecked.checked
                    }       
        }    

}
            Rectangle{
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
    
}}
        Rectangle{
            id: third_rectangle
            anchors.top: second_rectangle.bottom
            anchors.topMargin: 100
            

            Column{
                spacing: 5
                
                Text{
                    id: combo_kraj_label
                    text: "Kraj:"
                }

                ComboBox {
                    id: combo_kraj
                    currentIndex: -1
                    model: settlementListModel.region_list
                }

                Text{
                    id: combo_okres_label
                    text: "Okres:"
                }

                ComboBox {
                    currentIndex: -1
                    id: combo_okres
                    model: settlementListModel.district_list
                }
            }
        }
        Rectangle{
            id:forth_rectangle
            anchors.top:third_rectangle.bottom
            anchors.topMargin: 170
            width: 250
            height: 500
            
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
        }
        Rectangle{
            id:fifth_rectangle
            anchors.top:forth_rectangle.bottom
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
