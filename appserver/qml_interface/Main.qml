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
        function onRobotConnected(rid)
        {
            robotModel.append({"rid": rid, "score": 0})
        }
        function onRobotDisconnected(rid)
        {
            for(var i = 0; i < robotModel.count; i++)
            {
                if(robotModel.get(i).rid === rid)
                {
                    robotModel.remove(i)
                    break
                }
            }
        }
        function onStepReceived(rid, col, arm, exp, points)
        {
            for(var i = 0; i < robotModel.count; i++)
            {
                if(robotModel.get(i).rid === rid)
                {
                    robotModel.setProperty(i, "score", robotModel.get(i).score + points)
                    break
                }
            }
        }
    }

    ColumnLayout
    {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        RowLayout
        {
            // Bouton STOP/START
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

        RowLayout
        {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 10

            // Tableau des robots
            Rectangle
            {
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.maximumWidth: 250
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
                        text: "Robots connectés"
                        font.bold: true
                        color: "#222222"
                    }

                    Row
                    {
                        width: parent.width
                        spacing: 10

                        Text
                        {
                            text: "RID"
                            color: "#222222"
                            font.bold: true
                            width: 80
                        }
                        Text
                        {
                            text: "Points"
                            color: "#222222"
                            font.bold: true
                        }
                    }

                    Rectangle
                    {
                        width: parent.width
                        height: 1
                        color: "#cccccc"
                    }

                    ListView
                    {
                        id: robotView
                        width: parent.width
                        height: parent.height - 60
                        clip: true

                        model: ListModel { id: robotModel }

                        delegate: Row
                        {
                            spacing: 10
                            Text { text: model.rid;   color: "#222222" ; width: 80 }
                            Text { text: model.score; color: "#222222" }
                        }
                    }
                }
            }

            // Log des messages 
            Rectangle
            {
                Layout.fillHeight: true
                Layout.fillWidth: true
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
                        color: "#222222"
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
}