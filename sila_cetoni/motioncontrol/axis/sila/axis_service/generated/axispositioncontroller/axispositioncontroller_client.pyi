from __future__ import annotations

from typing import Iterable, Optional

from axispositioncontroller_types import MoveToHomePosition_Responses, MoveToPosition_Responses, StopMoving_Responses
from sila2.client import (
    ClientMetadata,
    ClientMetadataInstance,
    ClientObservableCommandInstance,
    ClientObservableProperty,
    ClientUnobservableProperty,
)

from .axispositioncontroller_types import Velocity

class AxisPositionControllerClient:
    """
    Allows to control the position of one axis of an axis system
    """

    PositionUnit: ClientUnobservableProperty[str]
    """
    The position unit used for specifying the position of an axis
    """

    MinimumPosition: ClientUnobservableProperty[float]
    """
    The minimum position limit of an axis
    """

    MaximumPosition: ClientUnobservableProperty[float]
    """
    The maximum position limit of an axis
    """

    MinimumVelocity: ClientUnobservableProperty[Velocity]
    """
    The minimum velocity limit of an axis
    """

    MaximumVelocity: ClientUnobservableProperty[Velocity]
    """
    The maximum velocity limit of an axis
    """

    Position: ClientObservableProperty[float]
    """
    The current position of an axis
    """

    AxisIdentifier: ClientMetadata[str]
    """
    The identifier of a single axis of an axis system. Use AvailableAxes from the AxisSystemControlService Feature to get all possible values.
    """

    def MoveToHomePosition(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> MoveToHomePosition_Responses:
        """
        Move the axis to its home position
        """
        ...
    def StopMoving(self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None) -> StopMoving_Responses:
        """
        Immediately stops axis movement of a single axis
        """
        ...
    def MoveToPosition(
        self, Position: float, Velocity: Velocity, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClientObservableCommandInstance[None, MoveToPosition_Responses]:
        """
        Move the axis to the given position with a certain velocity
        """
        ...
