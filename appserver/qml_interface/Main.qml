import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow
{
    id: startWindow
    width: 800
    height: 600
    visible: true
    title: qsTr("Serveur Arbitre")

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
            robotModel.append({"rid": rid, "score": 0, "steps": 0})
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
        function onStepReceived(rid, col, arm, exp, points, nb_steps)
        {
            for(var i = 0; i < robotModel.count; i++)
            {
                if(robotModel.get(i).rid === rid)
                {
                    robotModel.setProperty(i, "score", robotModel.get(i).score + points)
                    robotModel.setProperty(i, "steps", nb_steps)
                    break
                }
            }
        }
    }

    ColumnLayout
    {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 15

        RowLayout
        {
            // Bouton STOP/START
            Layout.fillWidth: true
            //spacing : 15

            Label
            {
                text: "Serveur Arbitre"
                font.pixelSize: 20
                font.bold: true
                Layout.fillWidth: true
            }

            Label
            {
                text: serverRunning ? "● ON" : "● OFF"
                color: serverRunning ? "#43a047" : "#e53935"
                font.bold: true
                font.pixelSize: 14
            }

            Button
            {
                text: serverRunning ? "Arrêter" : "Démarrer"
                highlighted: !serverRunning
                onClicked: serverRunning ? server_manager.stop() : server_manager.start()
            }

            Item { Layout.preferredWidth: 10 }
            
        
            // Switch localhost
            RowLayout
            {
                spacing: 5
                Label { text: qsTr("Localhost") }
                Switch
                {
                    checked: false
                    onClicked: server_manager.set_localhost(checked)
                }
            }
            

            Pane
            {
                padding: 6
                background: Rectangle
                {
                    color: Qt.alpha(palette.highlight, 0.1)
                    radius: 6
                    border.color: palette.highlight
                }
                Label
                {
                    text: "IP : " + server_manager.get_local_ip()
                    font.bold: true
                }
            }

            Item { Layout.fillWidth: true }

            Button
            {
                text: "Charger .battle"
                highlighted: true
                enabled: true
                onClicked: fileDialog.open()

                // background: Rectangle
                // {
                //     color: parent.down ? "#005BB5" : parent.hovered ? "#1E90FF" : "#0078D7"
                //     radius: 3
                // }

                // contentItem: Text
                // {
                //     text: parent.text
                //     color: "white"
                //     horizontalAlignment: Text.AlignHCenter
                //     verticalAlignment: Text.AlignVCenter
                // }
            }

            FileDialog
            {
                id: fileDialog
                title: "Choisir un fichier .battle"
                nameFilters: ["Fichiers battle (*.battle)"]
                onAccepted: server_manager.load_battle(selectedFile)
            }

        }

        RowLayout
        {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 15

            // Tableau des robots
            Pane
            {
                Layout.fillHeight: true
                Layout.maximumWidth: 280
                Layout.fillWidth: true
                
                // color: "#f5f5f5"
                // border.color: "#cccccc"
                // border.width: 1
                // radius: 3

                background: Rectangle
                {
                    color: Qt.alpha(palette.window, 0.5)
                    radius: 12
                    border.color: palette.light
                }

                ColumnLayout
                {
                    anchors.fill: parent
                    spacing: 8

                    Label
                    {
                        text: "Robots connectés"
                        font.bold: true
                        font.pixelSize: 14
                    }

                    RowLayout
                    {
                        Layout.fillWidth: true
                        spacing: 0

                        Label { text: "RID";    font.bold: true; Layout.preferredWidth: 80 }
                        Label { text: "Steps";  font.bold: true; Layout.preferredWidth: 60 }
                        Label { text: "Points"; font.bold: true; Layout.fillWidth: true }
                        
                    }

                    Rectangle
                    {
                        Layout.fillWidth: true
                        height: 1
                        color: palette.mid
                    }

                    ListView
                    {
                        id: robotView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true

                        model: ListModel { id: robotModel }

                        delegate: RowLayout
                        {
                            width: robotView.width
                            spacing: 0
                            Label { text: model.rid;   Layout.preferredWidth: 80 }
                            Label { text: model.steps; Layout.preferredWidth: 60}
                            Label { text: model.score; Layout.fillWidth: true }
                        }
                    }
                }
            }

            // Log des messages 
            Pane
            {
                Layout.fillHeight: true
                Layout.fillWidth: true

                background: Rectangle
                {
                    color: Qt.alpha(palette.window, 0.5)
                    radius: 12
                    border.color: palette.light
                }

                ColumnLayout
                {
                    anchors.fill: parent
                    spacing: 8

                    Label
                    {
                        text: "Log des messages"
                        font.bold: true
                        font.pixelSize: 14
                    }

                    // Séparateur
                    Rectangle
                    {
                        Layout.fillWidth: true
                        height: 1
                        color: palette.mid
                    }

                    ListView
                    {
                        id: logView
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        clip: true

                        model: ListModel { id: logModel }

                        delegate: Label
                        {
                            width: logView.width
                            text: model.message
                            padding: 2
                            wrapMode: Label.WordWrap
                        }

                        // Scroll automatique vers le bas quand un message arrive
                        onCountChanged: positionViewAtEnd()
                    }
                }
            }
        }   
    }
}