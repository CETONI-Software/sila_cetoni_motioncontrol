from __future__ import annotations

from abc import ABC, abstractmethod
from queue import Queue
from typing import Any, Dict, List, Optional

from sila2.framework import FullyQualifiedIdentifier
from sila2.server import FeatureImplementationBase

from .axissystemcontrolservice_types import (
    ClearFaultState_Responses,
    DisableAxisSystem_Responses,
    EnableAxisSystem_Responses,
)


class AxisSystemControlServiceBase(FeatureImplementationBase, ABC):

    _AxisSystemState_producer_queue: Queue[str]

    _AxesInFaultState_producer_queue: Queue[List[str]]

    def __init__(self):
        """
        Provides functionality to observe and control the state of an axis system
        """

        self._AxisSystemState_producer_queue = Queue()

        self._AxesInFaultState_producer_queue = Queue()

    @abstractmethod
    def get_AvailableAxes(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> List[str]:
        """
        The names of the individual axes of the axis system.

        :param metadata: The SiLA Client Metadata attached to the call
        :return: The names of the individual axes of the axis system.
        """
        pass

    def update_AxisSystemState(self, AxisSystemState: str, queue: Optional[Queue[str]] = None):
        """
        The current state of the axis system. This is either 'Enabled' or 'Disabled'. Only if the state is 'Enabled', the axis system can move.

        This method updates the observable property 'AxisSystemState'.
        """
        if queue:
            queue.put(AxisSystemState)
        else:
            self._AxisSystemState_producer_queue.put(AxisSystemState)

    def AxisSystemState_on_subscription(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> Optional[Queue[str]]:
        """
        The current state of the axis system. This is either 'Enabled' or 'Disabled'. Only if the state is 'Enabled', the axis system can move.

        This method is called when a client subscribes to the observable property 'AxisSystemState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    def update_AxesInFaultState(self, AxesInFaultState: List[str], queue: Optional[Queue[List[str]]] = None):
        """
        Returns all axes of the system that are currently in fault state. The fault state of all axes can be cleared by calling ClearFaultState.

        This method updates the observable property 'AxesInFaultState'.
        """
        if queue:
            queue.put(AxesInFaultState)
        else:
            self._AxesInFaultState_producer_queue.put(AxesInFaultState)

    def AxesInFaultState_on_subscription(
        self, *, metadata: Dict[FullyQualifiedIdentifier, Any]
    ) -> Optional[Queue[List[str]]]:
        """
        Returns all axes of the system that are currently in fault state. The fault state of all axes can be cleared by calling ClearFaultState.

        This method is called when a client subscribes to the observable property 'AxesInFaultState'

        :param metadata: The SiLA Client Metadata attached to the call
        :return: Optional `Queue` that should be used for updating this property
        """
        pass

    @abstractmethod
    def EnableAxisSystem(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> EnableAxisSystem_Responses:
        """
        Set all axes of the axis system into enabled state


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def DisableAxisSystem(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> DisableAxisSystem_Responses:
        """
        Set all axes of the axis system into disabled state


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass

    @abstractmethod
    def ClearFaultState(self, *, metadata: Dict[FullyQualifiedIdentifier, Any]) -> ClearFaultState_Responses:
        """
        Clears the fault condition of all axes. This is some kind of error acknowledge that clears the last fault and sets the device in an error-free state.


        :param metadata: The SiLA Client Metadata attached to the call

        """
        pass
