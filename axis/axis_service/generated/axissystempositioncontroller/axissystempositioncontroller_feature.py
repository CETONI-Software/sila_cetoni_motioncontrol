from os.path import dirname, join

from sila2.framework import Feature

AxisSystemPositionControllerFeature = Feature(
    open(join(dirname(__file__), "AxisSystemPositionController.sila.xml")).read()
)
