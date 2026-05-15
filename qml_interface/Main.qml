import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow
{
    id: startWindow
    width: 640
    height: 480
    visible: true
    title: "SapinPastel - Marty Controller"//utiliser qsTr("blablabla") si on souhaite traduction

    StackView
    {
        id: main_stack
        initialItem: "ConnexionPage.qml"

        anchors.fill: parent
    }

}