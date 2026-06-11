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

    property bool is_marty_connected: false
    property bool is_referee_connected: false
    property bool expecting_referee: false

    function checkNavigation()
    {
        if (is_marty_connected && (!expecting_referee || is_referee_connected)) {// On change de page si le robot est connecté et qu'on attend pas d'arbitre ou il est connecté aussi
            
            // Sécurité pour éviter d'empiler la page plusieurs fois si les deux signaux arrivent en même temps
            if (main_stack.depth === 1) {
                main_stack.push("ControlPage.qml")
            }
        }
    }

    StackView
    {
        id: main_stack
        focus: true//Pour navigation clavier dans control page
        initialItem: "ConnectionPage.qml"

        anchors.fill: parent
    }

    Connections
    {
        target: marty_manager
        function onConnectionToMartySuccess(result)
        {
            startWindow.is_marty_connected = result
            if(result)
                startWindow.checkNavigation()
        }
        function onDisconnectionToMartySuccess(result)
        {
            startWindow.is_marty_connected = !result
            startWindow.is_referee_connected = !result
            if(result) {
                main_stack.pop()
            }
        }
    }

    // A IMPLEMENTER
    // Connections
    // {
    //     target: marty_to_referee 

    //     function onConnectionToRefereeSuccess(result)
    //     {
    //         startWindow.is_referee_connected = result
    //         if(result) {
    //             startWindow.checkNavigation()
    //         }
    //     }
    // }

    Connections
    {
        target: marty_calibration
        function onCalibrationColorPage(result)
        {
                main_stack.push("ColorCalibration.qml")
        }
    }


}