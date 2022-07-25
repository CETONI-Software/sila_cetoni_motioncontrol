from __future__ import annotations

import logging
import time
from concurrent.futures import Executor
from threading import Event
from typing import Any, Dict, List

from qmixsdk.qmixmotion import Axis, AxisSystem
from sila2.framework import FullyQualifiedIdentifier
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.server_configuration import ServerConfiguration
from sila_cetoni.application.system import ApplicationSystem

from ..generated.axissystemcontrolservice import (
    AxisSystemControlServiceBase,
    ClearFaultState_Responses,
    DisableAxisSystem_Responses,
    EnableAxisSystem_Responses,
)

LOG_LEVEL_TRACE = 5
logger = logging.getLogger(__name__)


class AxisSystemControlServiceImpl(AxisSystemControlServiceBase):
    __axis_system: AxisSystem
    __axes: Dict[str, Axis]
    __config: ServerConfiguration
    __stop_event: Event

    def __init__(self, server: SilaServer, axis_system: AxisSystem, executor: Executor):
        super().__init__(server)
        self.__axis_system = axis_system
        self.__axes = {
            self.__axis_system.get_axis_device(i).get_device_name(): self.__axis_system.get_axis_device(i)
            for i in range(self.__axis_system.get_axes_count())
        }

        self.__config = ServerConfiguration(self.parent_server.server_name, ApplicationSystem().device_config.name)
        self.__stop_event = Event()

        self._restore_last_position_counters()

        def update_axis_system_state(stop_event: Event):
            new_is_enabled = is_enabled = self._is_all_axes_enabled()
            while not stop_event.is_set():
                new_is_enabled = self._is_all_axes_enabled()
                if new_is_enabled != is_enabled:
                    is_enabled = new_is_enabled
                    self.update_AxisSystemState("Enabled" if is_enabled else "Disabled")
                time.sleep(0.1)

        def update_axes_in_fault_state(stop_event: Event):
            new_axes_in_fault = axes_in_fault = self._get_axes_in_fault_state()
            while not stop_event.is_set():
                new_axes_in_fault = self._get_axes_in_fault_state()
                if new_axes_in_fault != axes_in_fault:
                    axes_in_fault = new_axes_in_fault
                    self.update_AxesInFaultState(axes_in_fault)
                time.sleep(0.1)

        # initial value
        self.update_AxisSystemState("Enabled" if self._is_all_axes_enabled() else "Disabled")
        self.update_AxesInFaultState(self._get_axes_in_fault_state())

        executor.submit(update_axis_system_state, self.__stop_event)
        executor.submit(update_axes_in_fault_state, self.__stop_event)

    def _restore_last_position_counters(self):
        """
        Reads the last position counters from the server's config file.
        """
        for axis_name in self.__axes.keys():
            pos_counter = self.__config.axis_position_counters.get(axis_name)
            if pos_counter is not None:
                logger.debug(f"Restoring position counter: {pos_counter}")
                self.__axes[axis_name].restore_position_counter(pos_counter)
            else:
                logger.warning(
                    f"Could not read position counter for {axis_name} from config file. " "Homing move needed!"
                )

    def _is_all_axes_enabled(self) -> bool:
        """
        Returns whether all axes of this axis system are enabled or not
        """
        enabled = True
        for name, axis in self.__axes.items():
            logger.log(LOG_LEVEL_TRACE, f"Axis {name} {'is' if axis.is_enabled() else 'is not'} enabled")
            enabled &= axis.is_enabled()
        return enabled

    def _get_axes_in_fault_state(self) -> List[str]:
        """
        Returns a list of the names of all axes that are currently in a fault state
        """
        return [axis_name for axis_name, axis in self.__axes.items() if axis.is_in_fault_state()]

    def get_AvailableAxes(self, *, metadata: MetadataDict) -> List[str]:
        return self.__axes.keys()

    def EnableAxisSystem(self, *, metadata: MetadataDict) -> EnableAxisSystem_Responses:
        self.__axis_system.enable(True)

    def DisableAxisSystem(self, *, metadata: MetadataDict) -> DisableAxisSystem_Responses:
        self.__axis_system.enable(False)

    def ClearFaultState(self, *, metadata: MetadataDict) -> ClearFaultState_Responses:
        for axis in self.__axes.values():
            axis.clear_fault()

    def stop(self) -> None:
        self.__stop_event.set()
        self.__config.axis_position_counters = {name: axis.get_position_counter() for name, axis in self.__axes.items()}
        self.__config.write()
