import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

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

        TextField//Conserver la dernière IP entrée ?
        {
            id: martyIpAddress
            width: startWindow.width/2

            selectByMouse: true
            placeholderText: qsTr("Marty IP Address")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}+/ }
        }

        Button//Touche entrée pour valider ?
        {
            id: buttonConnectMarty
            width: martyIpAddress.width
            height: 1.5*martyIpAddress.height

            text: qsTr("Connect to Marty")
            onClicked: marty_interaction.connect(martyIpAddress.text)//Appel du slot
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

        TextField//Conserver la dernière IP entrée ?
        {
            id: serverIpAddress
            width: startWindow.width/2

            selectByMouse: true
            placeholderText: qsTr("Server IP Address")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}+/ }
        }

        Button//Touche entrée pour valider ?
        {
            id: buttonConnectServer
            width: serverIpAddress.width
            height: 1.5*serverIpAddress.height

            text: qsTr("Connect to server referee")
            onClicked: client_server.checkServer(serverIpAddress.text)//Appel du slot
        }
    }

}