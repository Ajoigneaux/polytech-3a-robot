import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item
{
    id:color_calibration
    width: parent.width
    height: parent.height

    RowLayout
    {

        TextField
            {
                id: colorStandingOn
                width: startWindow.width/4

                selectByMouse: true
                placeholderText: qsTr("What is this color ?")
            }

        Button
            {
                id: color_calibration_button_1
                width: 100
                height: 1.5*100
                

                text: "Calibration"
                onClicked: marty_interaction.callCalibrationfunction(colorStandingOn.text)//Appel du slot
            }

        Button
            {
                id: read_color
                width: 100
                height: 1.5*100
                

                text: "Lecture"
                onClicked: marty_interaction.callWhatIsThiColorFunction()//Appel du slot
            }
    }
}