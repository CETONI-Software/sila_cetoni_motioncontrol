from os.path import dirname, join

from sila2.framework import Feature

AxisPositionControllerFeature = Feature(open(join(dirname(__file__), "AxisPositionController.sila.xml")).read())
