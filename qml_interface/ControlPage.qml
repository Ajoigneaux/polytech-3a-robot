import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    id:connexion_page
    width: parent.width//TypeError: Cannot read property 'height' of null A RESOUDRE ??
    height: parent.height

    Rectangle
    {
        height: 100
        width: 100
        color: "red"
        Text
        {
            text: "Control Page"
        }
    }

    Button
    {
        id: closeConnection
        height: 30
        width: closeConnection.height

        text: qsTr("X")
        onClicked: marty_interaction.disconnect()
    }
}