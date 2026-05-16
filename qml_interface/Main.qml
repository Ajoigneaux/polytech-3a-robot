import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow
{
    id: startWindow
    width: 640
    height: 480
    visible: true
    title: qsTr("SapinPastel - Marty Controller")

    StackView
    {
        id: main_stack
        initialItem: "ConnectionPage.qml"

        anchors.fill: parent
    }

    Connections
        {
            target: marty_interaction
            function onConnectionToMartySuccess()
            {
                main_stack.push("ControlPage.qml")
            }
    }

}