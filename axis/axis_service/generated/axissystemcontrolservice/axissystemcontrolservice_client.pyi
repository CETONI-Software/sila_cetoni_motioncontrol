from __future__ import annotations

from typing import Iterable, List, Optional

from axissystemcontrolservice_types import (
    ClearFaultState_Responses,
    DisableAxisSystem_Responses,
    EnableAxisSystem_Responses,
)
from sila2.client import ClientMetadataInstance, ClientObservableProperty, ClientUnobservableProperty

class AxisSystemControlServiceClient:
    """
    Provides functionality to observe and control the state of an axis system
    """

    AvailableAxes: ClientUnobservableProperty[List[str]]
    """
    The names of the individual axes of the axis system.
    """

    AxisSystemState: ClientObservableProperty[str]
    """
    The current state of the axis system. This is either 'Enabled' or 'Disabled'. Only if the state is 'Enabled', the axis system can move.
    """

    AxesInFaultState: ClientObservableProperty[List[str]]
    """
    Returns all axes of the system that are currently in fault state. The fault state of all axes can be cleared by calling ClearFaultState.
    """

    def EnableAxisSystem(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> EnableAxisSystem_Responses:
        """
        Set all axes of the axis system into enabled state
        """
        ...
    def DisableAxisSystem(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> DisableAxisSystem_Responses:
        """
        Set all axes of the axis system into disabled state
        """
        ...
    def ClearFaultState(
        self, *, metadata: Optional[Iterable[ClientMetadataInstance]] = None
    ) -> ClearFaultState_Responses:
        """
        Clears the fault condition of all axes. This is some kind of error acknowledge that clears the last fault and sets the device in an error-free state.
        """
        ...
