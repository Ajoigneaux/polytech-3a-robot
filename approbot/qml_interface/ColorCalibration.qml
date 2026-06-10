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

        ComboBox 
            {
                width: 200
                model: [ "Noir", "Mauve", "Bleu foncé", "Jaune", "Bleu ciel", "Vert", "Rouge" ]
            }

        Button
            {
                id: color_calibration_button_1
                width: 100
                height: 1.5*100
                

                text: "Calibration"
                onClicked: marty_calibration.calibrationColors(colorStandingOn.text)//Appel du slot
            }

        Button
            {
                id: read_color
                width: 100
                height: 1.5*100
                

                text: "Lecture"
                onClicked: marty_calibration.whatIsThisColor()//Appel du slot
            }
    }
}