import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Basic


Item
{
    id:connection_page
    width: parent.width
    height: parent.height

    Column
    {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        spacing: 15

        TextField
        {
            id: martyIpAddress
            width: startWindow.width/2

            selectByMouse: true
            placeholderText: qsTr("Marty IP Address")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}+/ }
        }

        Button
        {
            id: buttonConnectMarty
            width: martyIpAddress.width
            height: 1.5*martyIpAddress.height

            text: qsTr("Connect to Marty")
            onClicked: marty_interaction.connect(martyIpAddress.text)//Appel du slot

            contentItem: Text {
                text: buttonConnectMarty.text
                font: buttonConnectMarty.font
                opacity: enabled ? 1.0 : 0.3
                color: buttonConnectMarty.down ? "#17a81a" : "#21be2b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }

            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                border.color: buttonConnectMarty.down ? "#17a81a" : "#21be2b"
                border.width: 1
                radius: 2
            }
        }

        Text
        {
            id: textError
            text: ""
            color: "red"
        }

        Connections
        {
            target: marty_interaction
            function onConnectionToMartySuccess(result)
            {
                if(!result)
                    textError.text=qsTr("Error failed to connect")
            }
        }

        TextField
        {
            id: serverIpAddress
            width: startWindow.width/2

            selectByMouse: true
            placeholderText: qsTr("Server IP Address")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}+/ }
        }

        Button
        {
            id: buttonConnectServer
            width: serverIpAddress.width
            height: 1.5*serverIpAddress.height

            text: qsTr("Connect to server referee")
            onClicked: client_server.checkServer(serverIpAddress.text)//Appel du slot

            contentItem: Text {
                text: buttonConnectServer.text
                font: buttonConnectServer.font
                opacity: enabled ? 1.0 : 0.3
                color: buttonConnectServer.down ? "#17a81a" : "#21be2b"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                elide: Text.ElideRight
            }

            background: Rectangle {
                implicitWidth: 100
                implicitHeight: 40
                opacity: enabled ? 1 : 0.3
                border.color: buttonConnectServer.down ? "#17a81a" : "#21be2b"
                border.width: 1
                radius: 2
            }

        }
    }
}
