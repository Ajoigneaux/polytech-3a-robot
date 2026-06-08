import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    id:connexion_page
    width: parent.width
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
        id: color_calibration_page_button
        width: 100
        height: 1.5*100

        text: "Calibration Couleur"
        onClicked: marty_interaction.calibrationColorPageSlot()//Appel du slot
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