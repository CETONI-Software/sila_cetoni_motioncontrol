from __future__ import annotations
import logging

import time
from threading import Event
from concurrent.futures import Executor
from typing import Any, Dict

from sila2.framework import FullyQualifiedIdentifier
from sila2.framework.command.execution_info import CommandExecutionStatus
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import ObservableCommandInstance

import math
import numpy as np
import shapely.geometry as geom
import shapely.ops as ops
from qmixsdk.qmixbus import DeviceError

# only for debugging the positioning shape
# from matplotlib import use
# use('Agg')
# import matplotlib.pyplot as plt

from qmixsdk.qmixmotion import Axis, AxisSystem

from ..generated.axissystempositioncontroller import (
    AxisSystemPositionControllerBase,
    AxisSystemPositionControllerFeature,
    MoveToHomePosition_Responses,
    MoveToPosition_Responses,
    Position,
    StopMoving_Responses,
    MovementBlocked,
)


class AxisSystemPositionControllerImpl(AxisSystemPositionControllerBase):
    __axis_system: AxisSystem
    __axes: Dict[str, Axis]
    __stop_event: Event

    def __init__(self, axis_system: AxisSystem, device_properties: Dict[str, Any], executor: Executor):
        super().__init__()
        self.__axis_system = axis_system
        self.__axes = {
            self.__axis_system.get_axis_device(i).get_device_name(): self.__axis_system.get_axis_device(i)
            for i in range(self.__axis_system.get_axes_count())
        }

        if "jib_length" in device_properties:
            self.positioning_shape = self._create_positioning_shape(device_properties["jib_length"])
        else:
            x_axis = self.__axis_system.get_axis_device(0)
            y_axis = self.__axis_system.get_axis_device(1)
            self.positioning_shape = geom.box(
                x_axis.get_position_min(),
                y_axis.get_position_min(),
                x_axis.get_position_max(),
                y_axis.get_position_max(),
            )
        # plt.plot(*self.positioning_shape.exterior.xy)
        # plt.savefig('fig.png')

        PROPERTY_SAFE_ROTATION_HEIGHT = 0
        try:
            # safe rotation height only supported by rotAXYS (non-360) but not by others
            self.__axis_system.set_device_property(PROPERTY_SAFE_ROTATION_HEIGHT, 1)
        except DeviceError:
            pass

        self.__stop_event = Event()

        def update_position(stop_event: Event):
            new_position = position = self.__axis_system.get_actual_position_xy()
            while not stop_event.is_set():
                new_position = self.__axis_system.get_actual_position_xy()
                if not math.isclose(new_position.x, position.x) or not math.isclose(new_position.y, position.y):
                    position = new_position
                    self.update_Position(position)
                time.sleep(0.1)

        # initial value
        self.update_Position(self.__axis_system.get_actual_position_xy())

        executor.submit(update_position, self.__stop_event)

    def _create_positioning_shape(self, jib_length):
        """
        Create the positioning shape that represents the valid space of (X, Y)
        coordinates for movement commands of the axis system

        :param jib_length: The capillary distance from the central axis of the pivot arm
        """

        if "360" in self.__axis_system.get_device_name():
            # circular shape for rotAXYS360

            min_radius = self.__axes["rotAXYS360_1_Radius"].get_position_min()
            max_radius = self.__axes["rotAXYS360_1_Radius"].get_position_max()
            inner_radius = math.sqrt(min_radius**2 + jib_length**2)
            outer_radius = math.sqrt(max_radius**2 + jib_length**2)
            inner_circle = geom.Point(0, 0).buffer(inner_radius)
            outer_circle = geom.Point(0, 0).buffer(outer_radius)
            return geom.Polygon(outer_circle.exterior.coords, [inner_circle.exterior.coords])

        else:
            # arc-like shape for rotAXYS

            # the number of line segments to approximate an arc-like shape
            num_segments = 1000

            min_radius = self.__axes["rotAXYS_1_Radius"].get_position_min()
            max_radius = self.__axes["rotAXYS_1_Radius"].get_position_max()
            min_angle = self.__axes["rotAXYS_1_Rotation"].get_position_min()
            max_angle = self.__axes["rotAXYS_1_Rotation"].get_position_max()
            inner_angle = math.atan(jib_length / min_radius)
            outer_angle = math.atan(jib_length / max_radius)
            inner_angle_min = min_angle - inner_angle
            inner_angle_max = max_angle - inner_angle
            outer_angle_min = min_angle - outer_angle
            outer_angle_max = max_angle - outer_angle

            # the inner arc
            inner_radius = math.sqrt(min_radius**2 + jib_length**2)  # 46.1546
            inner_start_angle = math.degrees(-inner_angle_min)  # 151.767
            inner_end_angle = math.degrees(-inner_angle_max)  # 46.8603
            inner_theta = np.radians(np.linspace(inner_start_angle, inner_end_angle, num_segments))
            inner_x = inner_radius * np.cos(inner_theta)
            # we need to invert this because the coordinate system has a Y-axis that is flipped
            inner_y = -inner_radius * np.sin(inner_theta)

            inner_arc = geom.LineString(np.column_stack([inner_x, inner_y]))

            # the outer arc
            outer_radius = math.sqrt(max_radius**2 + jib_length**2)  # 145.617
            outer_start_angle = math.degrees(-outer_angle_min)  # 135.913
            outer_end_angle = math.degrees(-outer_angle_max)  # 31.0069
            outer_theta = np.radians(np.linspace(outer_start_angle, outer_end_angle, num_segments))
            outer_x = outer_radius * np.cos(outer_theta)
            # we need to invert this because the coordinate system has a Y-axis that is flipped
            outer_y = -outer_radius * np.sin(outer_theta)

            outer_arc = geom.LineString(np.column_stack([outer_x, outer_y]))

            # connect the first and last points of both arcs to get a closed shape
            left_bound = geom.LineString([inner_arc.coords[0], outer_arc.coords[0]])
            logging.debug(f"left_bound: {left_bound}")
            right_bound = geom.LineString([inner_arc.coords[-1], outer_arc.coords[-1]])
            logging.debug(f"right_bound: {right_bound}")

            return geom.Polygon(ops.linemerge([left_bound, inner_arc, outer_arc, right_bound]))

    def MoveToHomePosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> MoveToHomePosition_Responses:
        self.__axis_system.find_home()

    def StopMoving(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopMoving_Responses:
        self.__axis_system.stop_move()

    def _validate(self, point: geom.Point):
        """
        Validates that the given point `point` lies within the positioning shape
        of the axis system. If this is not the case an appropriate SiLAValidationError
        will be raised.

        :param point: The point to validate
        """

        # plt.plot(*point.xy, 'bo')
        # plt.savefig('fig.png')

        if not point.within(self.positioning_shape):
            nearest_point, dummy = ops.nearest_points(self.positioning_shape, point)
            logging.debug(f"nearest: {nearest_point}, other: {dummy}")
            raise ValidationError(
                AxisSystemPositionControllerFeature["MoveToPosition"].parameters.fields[0],
                f"The given Position {point.x, point.y} is not within the valid positioning range for the axis "
                f"system! The nearest valid position is ({nearest_point.x:.2f}, {nearest_point.y:.2f}).",
            )

    def MoveToPosition(
        self,
        Position: Position,
        Velocity: int,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
        instance: ObservableCommandInstance,
    ) -> MoveToPosition_Responses:
        logging.debug(f"Position: {Position}, Vel: {Velocity}")
        self._validate(Position)  # TODO Position type unknown
        self.StopMoving()

        # send first info immediately
        instance.status = CommandExecutionStatus.running
        instance.progress = 0

        try:
            self.__axis_system.move_to_postion_xy(Position.x, Position.y, Velocity / 100)
        except DeviceError as err:
            if err.errorcode == -1:  # Operation not permitted
                raise MovementBlocked()
            else:
                raise err
        logging.info(f"Started moving to {Position} with velocity of {Velocity}% of max velocity")

        is_moving = True
        while is_moving:
            time.sleep(0.5)
            logging.info("Position: %s", self.__axis_system.get_actual_position_xy())
            is_moving = not self.__axis_system.is_target_position_reached()

        if not is_moving:
            instance.status = CommandExecutionStatus.finishedSuccessfully
        else:
            instance.status = CommandExecutionStatus.finishedWithError
            logging.error("An unexpected error occurred: %s", self.__axis_system.read_last_error())

        logging.info("Finished moving!")

    def stop(self) -> None:
        self.__stop_event.set()
