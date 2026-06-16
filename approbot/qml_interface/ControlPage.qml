import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

Item {
    id: controlPage
    width: parent.width
    height: parent.height

    property bool is_file_selected: false

    // Navigation clavier
    focus: true
    Keys.onUpPressed: marty_interaction.moveUp(1, 0)
    Keys.onLeftPressed: marty_interaction.moveLeft(1, 0)
    Keys.onRightPressed: marty_interaction.moveRight(1, 0)
    Keys.onDownPressed: marty_interaction.moveDown(1, 0)

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 15

        // HEADER
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Button {
                text: "✕"
                Layout.preferredWidth: 40
                font.pixelSize: 18
                onClicked: {
                    client_server.bye()
                    marty_manager.disconnect()
                }
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Déconnexion")
            }

            Label {
                text: qsTr("Tableau de Bord Marty")
                font.pixelSize: 20
                font.bold: true
                Layout.fillWidth: true
            }

            Button {
                text: qsTr("Calibration couleurs")
                onClicked: main_stack.push("ColorCalibration.qml")
            }

            RowLayout {
                spacing: 5
                Label { text: "🔋" }
                Label {
                    id: batteryLevelText
                    text: "..%"
                    font.bold: true
                }
            }
        }

        // ZONE PRINCIPALE
        GridLayout {
            columns: 2
            Layout.fillWidth: true
            Layout.fillHeight: true
            columnSpacing: 20
            rowSpacing: 20

            // MOUVEMENTS
            Pane {
                Layout.fillWidth: true
                Layout.fillHeight: true
                background: Rectangle {
                    color: Qt.alpha(palette.window, 0.5)
                    radius: 12
                    border.color: palette.light
                }

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 10
                    Label { 
                        text: qsTr("Mouvements"); 
                        font.bold: true; 
                        Layout.alignment: Qt.AlignHCenter 
                    }

                    GridLayout {
                        columns: 3
                        Rectangle { width: 40; height: 40; color: "transparent" }
                        Button { text: "↑"; onClicked: marty_interaction.moveUp(1, 0); highlighted: true }
                        Rectangle { width: 40; height: 40; color: "transparent" }
                        Button { text: "←"; onClicked: marty_interaction.moveLeft(1); highlighted: true }
                        Button { text: "○"; onClicked: marty_interaction.stand(); highlighted: true }
                        Button { text: "→"; onClicked: marty_interaction.moveRight(1); highlighted: true }
                        Rectangle { width: 40; height: 40; color: "transparent" }
                        Button { text: "↓"; onClicked: marty_interaction.moveDown(1, 0); highlighted: true }
                        Rectangle { width: 40; height: 40; color: "transparent" }
                    }
                }
            }

            // BRAS
            Pane {
                Layout.fillWidth: true
                Layout.fillHeight: true
                background: Rectangle {
                    color: Qt.alpha(palette.window, 0.5)
                    radius: 12
                    border.color: palette.light
                }

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 10
                    Label { 
                        text: qsTr("Contrôle des Bras"); 
                        font.bold: true; 
                        Layout.alignment: Qt.AlignHCenter 
                    }

                    RowLayout {
                        spacing: 20
                        ColumnLayout {
                            Label { text: qsTr("Gauche"); Layout.alignment: Qt.AlignHCenter }
                            Button { text: "↑"; onClicked: marty_interaction.leftArmForward() }
                            Button { text: "↓"; onClicked: marty_interaction.leftArmBack() }
                        }
                        ColumnLayout {
                            Label { text: qsTr("Droit"); Layout.alignment: Qt.AlignHCenter }
                            Button { text: "↑"; onClicked: marty_interaction.rightArmForward() }
                            Button { text: "↓"; onClicked: marty_interaction.rightArmBack() }
                        }
                    }
                    Button {
                        text: qsTr("RESET BRAS")
                        Layout.fillWidth: true
                        onClicked: marty_interaction.resetArms()
                    }
                }
            }

            // DANCE
            Pane {
                Layout.columnSpan: 2
                Layout.fillWidth: true
                Layout.preferredHeight: 120
                background: Rectangle {
                    id: danceZoneRectangle
                    color: Qt.alpha(palette.light, 0.1)
                    radius: 12
                    border.color: palette.light
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 20

                    ColumnLayout {
                        Layout.fillWidth: true
                        Label { 
                            text: qsTr("Dance Battle")
                            font.bold: true 
                            font.pixelSize: 16
                        }
                        Label {
                            id: selectedFileNameLabel
                            text: qsTr("Aucun fichier sélectionné")
                            font.italic: true
                            color: palette.placeholderText
                        }
                    }

                    FileDialog {
                        id: danceFileDialog
                        title: qsTr("Choisir un fichier dance")
                        nameFilters: [qsTr("Fichiers Dance (*.dance)"), qsTr("Tous les fichiers (*)")]
                        onAccepted: {
                            // Conversion de l'URL du fichier en chemin local pour le backend
                            let path = selectedFile.toString().replace("file:///", "");
                            
                            marty_read_dance.setDanceFile(path)
                            selectedFileNameLabel.text = path.split(/[\\/]/).pop() // Affiche juste le nom du fichier
                            is_file_selected = true
                            danceZoneRectangle.border.color = '#007419'
                            danceZoneRectangle.color = Qt.alpha('#007419', 0.1)
                        }
                    }

                    Button {
                        text: qsTr("Parcourir...")
                        onClicked: danceFileDialog.open()
                    }

                    Button {
                        text: qsTr("LANCER LA BATTLE")
                        highlighted: true
                        enabled: is_file_selected
                        Layout.alignment: Qt.AlignRight
                        onClicked: marty_read_dance.startSequency()
                    }
                }
            }
        }
    }

    // Gestion niveau de batterie
    Connections {
        target: marty_manager
        function onBatteryLevelChanged(value) {
            batteryLevelText.text = value + "%"
            // Changement de couleur si batterie faible
            batteryLevelText.color = value < 20 ? "#e53935" : palette.text
        }
    }
}