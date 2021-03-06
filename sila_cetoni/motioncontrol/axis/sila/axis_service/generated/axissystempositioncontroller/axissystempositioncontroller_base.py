# Generated by sila2.code_generator; sila2.__version__: 0.8.0
from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import TYPE_CHECKING, Optional

from sila2.server import FeatureImplementationBase, MetadataDict, ObservableCommandInstance

from .axissystempositioncontroller_types import (
    MoveToHomePosition_Responses,
    MoveToPosition_Responses,
    Position,
    StopMoving_Responses,
)

if TYPE_CHECKING:
    from sila2.server import SilaServer


class AxisSystemPositionControllerBase(FeatureImplementationBase, ABC):

    _Position_producer_queue: Queue[Position]

    def __init__(self, parent_server: SilaServer):
        """
        Allows to control the position of an axis system
        """
        super().__init__(parent_server=parent_server)

        self._Position_producer_queue = Queue()

    def update_Position(self, Position: Position, queue: Optional[Queue[Position]] = None):
        """
        The current XY position of the axis system

        This method updates the observable property 'Position'.
        """
        if queue is None:
            queue = self._Position_producer_queue
        queue.put(Position)

    def Position_on_subscription(self, *, metadata: MetadataDict) -> Optional[Queue[Position]]:
        """
        The current XY position of the axis system

        This method is called when a client subscribes to the observable property 'Position'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property.
            If None, the default Queue will be used.
        """
        pass

    @abstractmethod
    def MoveToHomePosition(self, *, metadata: MetadataDict) -> MoveToHomePosition_Responses:
        """
        Move the axis system to its home position. The axis system should manage the order of the movement and should know how to move all axes into a home state.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def StopMoving(self, *, metadata: MetadataDict) -> StopMoving_Responses:
        """
        Immediately stops all movement of the axis system


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def MoveToPosition(
        self, Position: Position, Velocity: int, *, metadata: MetadataDict, instance: ObservableCommandInstance
    ) -> MoveToPosition_Responses:
        """
        Move the axis system to the given position with a certain velocity


        :param Position: The position to move to

        :param Velocity: An integer value between 0 (exclusive) and 100 (inclusive) defining the relative speed at which all axes of the axis system should move. The velocity value is multiplied with the maximum velocity value of each axis. So a value of 100 means, all axes travel with their maximum velocity. A value of 50 means, all axes travel with the half of the maximum velocity.

        :param metadata: The SiLA Client Metadata attached to the call
        :param instance: The command instance, enabling sending status updates to subscribed clients

        """
        pass
