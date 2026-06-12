import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Item {
    id: connection_page
    width: parent.width
    height: parent.height

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 6
        // Limite la largeur
        width: Math.min(parent.width*0.8, 350)

        Label {
            text: qsTr("Marty Controller")
            font.pixelSize: 22
            font.bold: true
            Layout.alignment: Qt.AlignHCenter
            Layout.bottomMargin: 10
        }

        Item { Layout.preferredHeight: 28 }

        Label {
            text: qsTr("Adresse IP du robot")
            font.pixelSize: 12
            leftPadding: 2
            font.weight: Font.Medium
        }

        TextField {
            id: martyIpAddress
            Layout.fillWidth: true
            selectByMouse: true
            placeholderText: qsTr("ex: 192.168.0.12")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}/ }
            Keys.onEnterPressed:  buttonConnect.clicked()
        }

        Item { Layout.preferredHeight: 20 }

        Label {
            text: qsTr("Adresse IP de l'arbitre (Optionnelle)")
            font.pixelSize: 12
            leftPadding: 2
            font.weight: Font.Medium
        }

        TextField {
            id: refereeIpAddress
            Layout.fillWidth: true
            selectByMouse: true
            placeholderText: qsTr("ex: 127.0.0.1")
            validator: RegularExpressionValidator { regularExpression: /([0-9]{1,3}\.){3}[0-9]{1,3}/ }
            Keys.onEnterPressed:  buttonConnect.clicked()
        }

        Item { Layout.preferredHeight: 20 }

        Button {
            id: buttonConnect
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            Layout.topMargin: 10
            
            text: qsTr("Se connecter")
            highlighted: true

            onClicked: {
                textError.text = "" // Réinitialise le texte d'erreur

                // Connexion au robot prioritaire
                if (martyIpAddress.text !== "") {
                    startWindow.expecting_referee = (refereeIpAddress.text !== "")// On dit a Main.qml qu'aucun arbitre n'est attendu
                    marty_manager.connect(martyIpAddress.text)
                } else {
                    textError.text = qsTr("Veuillez renseigner l'IP du robot.")
                    return;//Quitte la fonction si pas d'IP
                }

                // Connexion à l'arbitre si le champ n'est pas vide
                if (refereeIpAddress.text !== "") {
                    client_server.checkServer(refereeIpAddress.text)
                }
            }
        }

        Label {
            id: textError
            text: ""
            color: "#e53935"
            Layout.alignment: Qt.AlignHCenter
            wrapMode: Label.WordWrap
        }
    }

    // Gestion des signaux du backend Marty
    Connections {
        target: marty_manager
        function onConnectionToMartySuccess(result) {
            if (!result) {
                textError.text = qsTr("Erreur : Impossible de se connecter au robot")
            }
        }
        // AJOUTER ERREUR POUR CONNECTION A L'ARBITRE
    }
}
