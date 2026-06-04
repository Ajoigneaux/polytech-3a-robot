import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    id: controlPage
    width: parent.width
    height: parent.height

    //Necessite focus: true sur parent pour fonctionner sans focus de bouton par ex
    Keys.onUpPressed: marty_interaction.moveUp()
    Keys.onLeftPressed: marty_interaction.moveLeft()
    Keys.onRightPressed: marty_interaction.moveRight()
    Keys.onDownPressed: marty_interaction.moveDown()

    ColumnLayout
    {
        anchors.fill: parent
        anchors.margins: 10//A VOIR
        spacing: 20//A VOIR

        // Header with disconnection button
        Item
        {
            Layout.fillWidth: true
            Layout.preferredHeight: 50

            RowLayout
            {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10

                Button
                {
                    id: closeConnection
                    Layout.preferredHeight: 30
                    Layout.preferredWidth: 30
                    text: qsTr("✕")
                    font.pixelSize: 16
                    onClicked: marty_interaction.disconnect()
                }
                
                Item
                {
                    Layout.fillWidth: true
                }

                Text
                {
                    id: batteryLevelText
                    text: "..%"
                }
                Connections
                {
                    target: marty_interaction
                        function onBatteryLevelChanged(value)
                        {
                            
                            batteryLevelText.text=value+"%"
                        }
                }
            }
        }

        // Espaceur
        // Item { Layout.fillHeight: true }

        // Control commands
        RowLayout
        {
            ColumnLayout
            {
                Layout.alignment: Qt.AlignLeft
                spacing: 10

                Button
                {
                    id: moveUp
                    Layout.alignment: Qt.AlignHCenter
                    Layout.preferredHeight: 50
                    Layout.preferredWidth: 50
                    text: qsTr("↑")
                    font.pixelSize: 14
                    font.bold: true
                    onClicked: marty_interaction.moveUp()
                }

                RowLayout
                {
                    spacing: 10

                    Button
                    {
                        id: moveLeft
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("←")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.moveLeft()
                    }

                    Item { Layout.preferredWidth: 50 } // Space

                    Button
                    {
                        id: moveRight
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("→")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.moveRight()
                    }
                }

                Button
                {
                    id: moveDown
                    Layout.alignment: Qt.AlignHCenter
                    Layout.preferredHeight: 50
                    Layout.preferredWidth: 50
                    text: qsTr("↓")
                    font.pixelSize: 14
                    font.bold: true
                    onClicked: marty_interaction.moveDown()
                }
            }
 
            //BRAS
            ColumnLayout
            {
                Layout.alignment: Qt.AlignLeft
                spacing: 10

                RowLayout
                {
                    Button
                    {
                        id: leftArmForward
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("L↑")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.leftArmForward()
                    }

                    Button
                    {
                        id: rightArmForward
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("R↑")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.rightArmForward()
                    }
                }
                
                Item { Layout.preferredWidth: 50 } // Space

                RowLayout
                {
                    Button
                    {
                        id: leftArmBack
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("L↓")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.leftArmBack()
                    }

                    Button
                    {
                        id: rightArmBack
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("R↓")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.rightArmBack()
                    }

                    Button
                    {
                        id: resetArms
                        Layout.alignment: Qt.AlignHCenter
                        Layout.preferredHeight: 50
                        Layout.preferredWidth: 50
                        text: qsTr("RESET")
                        font.pixelSize: 14
                        font.bold: true
                        onClicked: marty_interaction.resetArms()
                    }
                }    
            }
        }
    }
}