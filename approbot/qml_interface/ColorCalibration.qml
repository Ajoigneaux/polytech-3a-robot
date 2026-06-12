import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: colorCalibrationPage
    width: parent.width
    height: parent.height

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        // HEADER
        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Button {
                text: "←"
                font.pixelSize: 18
                Layout.preferredWidth: 40
                onClicked: main_stack.pop() // Retour à la page précédente
                ToolTip.visible: hovered
                ToolTip.text: qsTr("Retour au contrôle")
            }

            Label {
                text: qsTr("Calibration du Capteur")
                font.pixelSize: 20
                font.bold: true
                Layout.fillWidth: true
            }
        }

        // ZONE PRINCIPALE
        Pane {
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignHCenter
            
            background: Rectangle {
                color: Qt.alpha(palette.window, 0.4)
                radius: 15
                border.color: palette.midlight
            }

            ColumnLayout {
                anchors.centerIn: parent
                width: parent.width * 0.8
                spacing: 25

                Label {
                    text: qsTr("Sélectionnez la couleur sur laquelle se trouve le robot :")
                    wrapMode: Label.WordWrap
                    horizontalAlignment: Label.AlignHCenter
                    Layout.fillWidth: true
                }

                ComboBox {
                    id: colorStandingOn
                    Layout.fillWidth: true
                    model: [ "Noir", "Mauve", "Bleu foncé", "Jaune", "Bleu ciel", "Vert", "Rouge" ]
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 15

                    Button {
                        id: color_calibration_button_1
                        text: qsTr("CALIBRER")
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        highlighted: true // Utilise la couleur d'accentuation du thème
                        onClicked: marty_calibration.calibrationColors(colorStandingOn.currentText)
                    }

                    Button {
                        id: read_color
                        text: qsTr("LIRE LE CAPTEUR")
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        onClicked: marty_calibration.whatIsThisColor()
                    }
                }
                
                Label {
                    id: feedbackLabel
                    text: qsTr("Positionnez le robot avant de cliquer.")
                    font.pixelSize: 12
                    font.italic: true
                    color: palette.placeholderText
                    Layout.alignment: Qt.AlignHCenter
                }
            }
        }

        // Espaceur bas
        Item { Layout.fillHeight: true }
    }
}