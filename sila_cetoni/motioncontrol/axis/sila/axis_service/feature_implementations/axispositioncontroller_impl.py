from __future__ import annotations

import logging
import math
import time
from concurrent.futures import Executor
from queue import Queue
from threading import Event
from typing import Any, Dict, List, Optional, Union

from qmixsdk.qmixmotion import Axis, AxisSystem
from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Metadata, Property
from sila2.framework.command.execution_info import CommandExecutionStatus
from sila2.framework.errors.validation_error import ValidationError
from sila2.server import MetadataDict, ObservableCommandInstance, SilaServer

from ..generated.axispositioncontroller import (
    AxisPositionControllerBase,
    AxisPositionControllerFeature,
    InvalidAxisIdentifier,
    MoveToHomePosition_Responses,
    MoveToPosition_Responses,
    StopMoving_Responses,
    Velocity,
)

logger = logging.getLogger(__name__)


class AxisPositionControllerImpl(AxisPositionControllerBase):
    __axis_system: AxisSystem
    __axes: Dict[str, Axis]
    __axis_id_metadata: Metadata
    __value_queues: Dict[str, Queue[float]]  # same keys and number of items and order as `__axes`
    __stop_event: Event

    def __init__(self, server: SilaServer, axis_system: AxisSystem, executor: Executor):
        super().__init__(server)
        self.__axis_system = axis_system
        self.__axes = {
            self.__axis_system.get_axis_device(i).get_device_name(): self.__axis_system.get_axis_device(i)
            for i in range(self.__axis_system.get_axes_count())
        }
        self.__axis_id_metadata = AxisPositionControllerFeature["AxisIdentifier"]

        for name, axis in self.__axes.items():
            unit = axis.get_position_unit()
            unit_string = (unit.prefix.name if unit.prefix.name != "unit" else "") + unit.unitid.name
            logger.debug(f"{name}, {unit_string}")

        self.__stop_event = Event()

        self.__value_queues = {}
        for axis_id in self.__axes.keys():
            self.__value_queues[axis_id] = Queue()

            # initial value
            self.update_Position(self.__axes[axis_id].get_actual_position(), queue=self.__value_queues[axis_id])

            executor.submit(self.__make_position_updater(axis_id), self.__stop_event)

    def __make_position_updater(self, axis_id: str):
        def update_position(stop_event: Event):
            new_value = value = self.__axes[axis_id].get_actual_position()
            while not stop_event.is_set():
                new_value = self.__axes[axis_id].get_actual_position()
                if not math.isclose(new_value, value):
                    value = new_value
                    self.update_Position(value, queue=self.__value_queues[axis_id])
                time.sleep(0.1)

        return update_position

    def _get_axis(self, metadata: MetadataDict) -> Axis:
        """
        Retrieves the axis that is requested by the `metadata`
        """
        axis_identifier: str = metadata[self.__axis_id_metadata]
        logger.debug(f"axis id: {axis_identifier}")
        try:
            return self.__axes[axis_identifier]
        except KeyError:
            raise InvalidAxisIdentifier(
                message=f"The sent Axis Identifier '{axis_identifier}' is invalid. Valid identifiers are: {self.__axes.keys()}."
            )

    def get_PositionUnit(self, *, metadata: MetadataDict) -> str:
        unit = self._get_axis(metadata).get_position_unit()
        return (unit.prefix.name if unit.prefix.name != "unit" else "") + unit.unitid.name

    def get_MinimumPosition(self, *, metadata: MetadataDict) -> float:
        return self._get_axis(metadata).get_position_min()

    def get_MaximumPosition(self, *, metadata: MetadataDict) -> float:
        return self._get_axis(metadata).get_position_max()

    def get_MinimumVelocity(self, *, metadata: MetadataDict) -> Velocity:
        return 0

    def get_MaximumVelocity(self, *, metadata: MetadataDict) -> Velocity:
        return self._get_axis(metadata).get_velocity_max()

    def Position_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[float]]:
        axis_identifier: str = metadata[self.__axis_id_metadata]
        try:
            return self.__value_queues[axis_identifier]
        except IndexError:
            raise InvalidAxisIdentifier(
                message=f"The sent Axis Identifier '{axis_identifier}' is invalid. Valid identifiers are: {self.__axes.keys()}.",
            )

    def MoveToHomePosition(self, *, metadata: MetadataDict) -> MoveToHomePosition_Responses:
        axis = self._get_axis(metadata)
        axis_name = axis.get_device_name()
        axis.find_home()

        is_moving = True
        while is_moving:
            time.sleep(0.5)
            logger.info("Position: %s (axis: %s)", axis.get_actual_position(), axis_name)
            is_moving = not axis.is_homing_position_attained()
        logger.info(f"MoveToHomePosition for {axis_name} done")

    def StopMoving(self, *, metadata: MetadataDict) -> StopMoving_Responses:
        self._get_axis(metadata).stop_move()

    def _validate(self, axis: Axis, position: float, velocity: Velocity):
        min_position = axis.get_position_min()
        max_position = axis.get_position_max()
        if position < min_position or position > max_position:
            err = ValidationError(
                f"The given position {position} is not in the valid range {min_position, max_position} for this axis."
            )
            err.parameter_fully_qualified_identifier = (
                AxisPositionControllerFeature["MoveToPosition"].parameters.fields[0].fully_qualified_identifier
            )
            raise err

        min_velocity = 0
        max_velocity = axis.get_velocity_max()
        if velocity < min_velocity or velocity > max_velocity:
            err = ValidationError(
                f"The given velocity {velocity} is not in the valid range {min_velocity, max_velocity} for this axis."
            )
            err.parameter_fully_qualified_identifier = (
                AxisPositionControllerFeature["MoveToPosition"].parameters.fields[1].fully_qualified_identifier
            )
            raise err

    def MoveToPosition(
        self,
        Position: float,
        Velocity: Velocity,
        *,
        metadata: MetadataDict,
        instance: ObservableCommandInstance,
    ) -> MoveToPosition_Responses:
        axis = self._get_axis(metadata)
        self._validate(axis, Position, Velocity)

        axis.move_to_position(Position, Velocity)
        logger.info(f"Started moving to {Position} with velocity of {Velocity}")

        is_moving = True
        while is_moving:
            time.sleep(0.5)
            logger.info("Position: %s", axis.get_actual_position())
            is_moving = not axis.is_target_position_reached()

        if is_moving:
            raise RuntimeError(f"An unexpected error occurred: {axis.read_last_error()}")

        logger.info("Finished moving!")

    def get_calls_affected_by_AxisIdentifier(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        return [AxisPositionControllerFeature]

    def stop(self) -> None:
        super().stop()
        self.__stop_event.set()
