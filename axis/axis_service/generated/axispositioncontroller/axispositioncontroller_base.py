from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, List, Optional, Union

from sila2.framework import Command, Feature, FullyQualifiedIdentifier, Property
from sila2.server import FeatureImplementationBase, ObservableCommandInstance

from .axispositioncontroller_types import (
    MoveToHomePosition_Responses,
    MoveToPosition_Responses,
    StopMoving_Responses,
    Velocity,
)


class AxisPositionControllerBase(FeatureImplementationBase, ABC):

    _Position_producer_queue: Queue[float]

    def __init__(self):
        """
        Allows to control the position of one axis of an axis system
        """

        self._Position_producer_queue = Queue()

    @abstractmethod
    def get_PositionUnit(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> str:
        """
        The position unit used for specifying the position of an axis

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The position unit used for specifying the position of an axis
        """
        pass

    @abstractmethod
    def get_MinimumPosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> float:
        """
        The minimum position limit of an axis

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The minimum position limit of an axis
        """
        pass

    @abstractmethod
    def get_MaximumPosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> float:
        """
        The maximum position limit of an axis

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The maximum position limit of an axis
        """
        pass

    @abstractmethod
    def get_MinimumVelocity(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Velocity:
        """
        The minimum velocity limit of an axis

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The minimum velocity limit of an axis
        """
        pass

    @abstractmethod
    def get_MaximumVelocity(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Velocity:
        """
        The maximum velocity limit of an axis

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The maximum velocity limit of an axis
        """
        pass

    def update_Position(self, Position: float, queue: Optional[Queue[float]] = None):
        """
        The current position of an axis

        This method updates the observable property 'Position'.
        """
        if queue:
            queue.put(Position)
        else:
            self._Position_producer_queue.put(Position)

    def Position_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[float]]:
        """
        The current position of an axis

        This method is called when a client subscribes to the observable property 'Position'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    @abstractmethod
    def MoveToHomePosition(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> MoveToHomePosition_Responses:
        """
        Move the axis to its home position


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def StopMoving(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> StopMoving_Responses:
        """
        Immediately stops axis movement of a single axis


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def MoveToPosition(
        self,
        Position: float,
        Velocity: Velocity,
        *,
        metadata: Dict[FullyQualifiedIdentifier, Any],
        instance: ObservableCommandInstance,
    ) -> MoveToPosition_Responses:
        """
        Move the axis to the given position with a certain velocity


        :param Position: The position to move to. Has to be in the range between MinimumPosition and MaximumPosition. See PositionUnit for the unit that is used for a specific axis. E.g. for rotational axis systems one of the axes needs a position specified in radians.

        :param Velocity: The velocity value for the movement. Has to be in the range between MinimumVelocity and MaximumVelocity.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass

    @abstractmethod
    def get_calls_affected_by_AxisIdentifier(self) -> List[Union[Feature, Command, Property, FullyQualifiedIdentifier]]:
        """
        Returns the fully qualified identifiers of all features, commands and properties affected by the
        SiLA Client Metadata 'Delay'.

        **Description of 'AxisIdentifier'**:
        The identifier of a single axis of an axis system. Use AvailableAxes from the AxisSystemControlService Feature to get all possible values.

        :return: Fully qualified identifiers of all features, commands and properties affected by the
            SiLA Client Metadata 'Delay'.
        """
        pass
