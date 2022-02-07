from os.path import dirname, join

from sila2.framework import Feature

AxisSystemControlServiceFeature = Feature(open(join(dirname(__file__), "AxisSystemControlService.sila.xml")).read())
