import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Basic
import QtQuick.Layouts

ApplicationWindow
{
    id: startWindow
    width: 800
    height: 600
    visible: true
    title: "Serveur Arbitre"

    property bool serverRunning: false

    Connections
    {
        target: server_manager
        function onServerStateChanged(state)
        {
            serverRunning = state
        }
        function onLogMessage(message)
        {
            logModel.append({"message": message})
        }
    }

    ColumnLayout
    {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        RowLayout
        {
            Layout.fillWidth: true

            Text
            {
                text: serverRunning ? "Serveur : ON" : "Serveur : OFF"
                color: serverRunning ? "green" : "red"
                font.bold: true
            }

            Button
            {
                text: serverRunning ? "Arrêter" : "Démarrer"
                onClicked: serverRunning ? server_manager.stop() : server_manager.start()

                background: Rectangle
                {
                    color: parent.down ? "#b22222" : parent.hovered ? "#ff6666" : "#cc0000"
                    radius: 3
                }

                contentItem: Text
                {
                    text: parent.text
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
            }
        }


        Rectangle
        {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#f5f5f5"
            border.color: "#cccccc"
            border.width: 1
            radius: 3
            
            Column
            {
                anchors.fill: parent
                anchors.margins: 5
                spacing: 5

                Text
                {
                    text: "Log des messages"
                    font.bold: true
                    color : "#222222"
                }

        
                ListView
                {
                    id: logView
                    width: parent.width
                    height: parent.height - 30
                    clip: true

                    model: ListModel { id: logModel }

                    delegate: Text
                    {
                        width: logView.width
                        text: model.message
                        color: "#222222"
                        padding: 2
                    }

                    // Scroll automatique vers le bas quand un message arrive
                    onCountChanged: positionViewAtEnd()
                }
            }
        }    
    }
}