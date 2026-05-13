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

    TextField//Conserver la dernière IP entrée ?
    {
        id: martyIpAddress
        width: startWindow.width/2
        anchors.horizontalCenter: parent.horizontalCenter//https://doc.qt.io/qt-6/qtquick-positioning-topic.html

        selectByMouse: true
        placeholderText: "Marty IP Address"
        validator: RegularExpressionValidator { regularExpression: /([0-9]{,3}.){3}[0-9]{,3}+/ }//Vérifier bon fonctionnement
    }

    Button
    {
        id: buttonConnect
        width: martyIpAddress.width
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: martyIpAddress.bottom

        text: "Connect to Marty"
        onClicked: con.outputStr("Hello")//Appel du slot
    }

}