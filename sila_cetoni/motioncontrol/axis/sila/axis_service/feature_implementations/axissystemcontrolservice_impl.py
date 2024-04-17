from __future__ import annotations

import logging
from typing import Dict, List

from qmixsdk.qmixmotion import Axis, AxisSystem
from sila2.server import MetadataDict, SilaServer

from sila_cetoni.application.server_configuration import ServerConfiguration
from sila_cetoni.application.system import ApplicationSystem
from sila_cetoni.utils import PropertyUpdater, not_equal

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

    def __init__(self, server: SilaServer, axis_system: AxisSystem):
        super().__init__(server)
        self.__axis_system = axis_system
        self.__axes = {
            self.__axis_system.get_axis_device(i).get_device_name(): self.__axis_system.get_axis_device(i)
            for i in range(self.__axis_system.get_axes_count())
        }

        self.run_periodically(
            PropertyUpdater(
                self._is_all_axes_enabled,
                not_equal,
                lambda val: self.update_AxisSystemState("Enabled" if val else "Disabled"),
            )
        )
        self.run_periodically(
            PropertyUpdater(
                self._get_axes_in_fault_state,
                not_equal,
                self.update_AxesInFaultState,
            )
        )

    def start(self) -> None:
        self.__config = ServerConfiguration(self.parent_server.server_name, ApplicationSystem().device_config.name)
        self._restore_last_position_counters()
        super().start()

    def stop(self) -> None:
        super().stop()
        self.__config.axis_position_counters = {name: axis.get_position_counter() for name, axis in self.__axes.items()}
        self.__config.write()

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
