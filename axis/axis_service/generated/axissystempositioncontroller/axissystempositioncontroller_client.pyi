from __future__ import annotations

from typing import Iterable, Optional

from axissystempositioncontroller_types import (
    MoveToHomePosition_Responses,
    MoveToPosition_Responses,
    StopMoving_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableCommandInstance, ClientObservableProperty

from .axissystempositioncontroller_types import Position

class AxisSystemPositionControllerClient:
    """
    Allows to control the position of an axis system
    """

    Position: ClientObservableProperty[Position]
    """
    The current XY position of the axis system
    """

    def MoveToHomePosition(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> MoveToHomePosition_Responses:
        """
        Move the axis system to its home position. The axis system should manage the order of the movement and should know how to move all axes into a home state.
        """
        ...
    def StopMoving(self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None) -> StopMoving_Responses:
        """
        Immediately stops all movement of the axis system
        """
        ...
    def MoveToPosition(
        self, Position: Position, Velocity: int, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, MoveToPosition_Responses]:
        """
        Move the axis system to the given position with a certain velocity
        """
        ...
