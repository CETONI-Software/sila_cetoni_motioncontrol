from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Dict, List, Optional, Union, overload

if TYPE_CHECKING:
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

    from .axis.sila.axis_service.server import Server

from qmixsdk import qmixmotion

from sila_cetoni.application.device import CetoniDevice
from sila_cetoni.utils import get_version


__version__ = get_version(__name__)

logger = logging.getLogger(__name__)


class CetoniAxisSystemDevice(CetoniDevice[qmixmotion.AxisSystem]):
    """
    Simple wrapper around `qmixmotion.AxisSystem` with additional information from the `CetoniDevice` class
    """

    def __init__(self, name: str, handle: qmixmotion.AxisSystem) -> None:
        super().__init__(name, "motioncontrol", handle)

    def set_operational(self):
        super().set_operational()
        self._device_handle.enable(False)


def parse_devices(json_devices: Optional[Dict[str, Dict]]) -> List[CetoniAxisSystemDevice]:
    """
    Parses the given JSON configuration `json_devices` and creates the necessary `CetoniAxisSystemDevice`s

    Parameters
    ----------
    json_devices: Dict[str, Dict] (optional)
        The `"devices"` section of the JSON configuration file as a dictionary (key is the device name, the value is a
        dictionary with the configuration parameters for the device, i.e. `"type"`, `"manufacturer"`, ...)

    Returns
    -------
    List[CetoniAxisSystemDevice]
        A list with all `CetoniAxisSystemDevice`s as defined in the JSON config
    """
    # CETONI devices are not defined directly in the JSON config
    return []


@overload
def create_devices(config: ApplicationConfiguration, scan: bool = False) -> None:
    """
    Looks up all controller devices from the current configuration and tries to auto-detect more devices if `scan` is
    `True`

    Parameters
    ----------
    config: ApplicationConfiguration
        The application configuration containing all devices for which SiLA Server and thus device driver instances
        shall be created
    scan: bool (default: False)
        Whether to scan for more devices than the ones defined in `config`
    """
    ...


@overload
def create_devices(config: CetoniDeviceConfiguration) -> List[CetoniAxisSystemDevice]:
    """
    Looks up all CETONI devices from the given configuration `config` and creates the necessary
    `CetoniAxisSystemDevice`s for them

    Parameters
    ----------
    config: CetoniDeviceConfiguration
        The CETONI device configuration

    Returns
    -------
    List[CetoniAxisSystemDevice]
        A list with all `CetoniAxisSystemDevice`s from the device configuration
    """

    ...


def create_devices(config: Union[ApplicationConfiguration, CetoniDeviceConfiguration], *args, **kwargs):
    from sila_cetoni.application.application_configuration import ApplicationConfiguration
    from sila_cetoni.application.cetoni_device_configuration import CetoniDeviceConfiguration

    if isinstance(config, ApplicationConfiguration):
        logger.info(
            f"Package {__name__!r} currently only supports CETONI devices. Parameter 'config' must be of type "
            f"'CetoniDeviceConfiguration'!"
        )
        return
    if isinstance(config, CetoniDeviceConfiguration):
        return create_devices_cetoni(config)
    raise ValueError(
        f"Parameter 'config' must be of type 'ApplicationConfiguration' or 'CetoniDeviceConfiguration', not"
        f"{type(config)!r}!"
    )


def create_devices_cetoni(config: CetoniDeviceConfiguration) -> List[CetoniAxisSystemDevice]:
    """
    Implementation of `create_devices` for devices from the CETONI device config

    See `create_devices` for an explanation of the parameters and return value
    """

    system_count = qmixmotion.AxisSystem.get_axis_system_count()
    logger.debug(f"Number of axis systems: {system_count}")

    devices: List[CetoniAxisSystemDevice] = []
    for i in range(system_count):
        axis_system = qmixmotion.AxisSystem()
        axis_system.lookup_by_device_index(i)
        axis_system_name = axis_system.get_device_name()
        logger.debug(f"Found axis system {i} named {axis_system.get_device_name()}")
        devices.append(CetoniAxisSystemDevice(axis_system_name, axis_system))
    return devices


def create_server(device: CetoniAxisSystemDevice, **server_args) -> Server:
    """
    Creates the SiLA Server for the given `device`

    Parameters
    ----------
    device: Device
        The device for which to create a SiLA Server
    **server_args
        Additional arguments like server name, server UUID to pass to the server's `__init__` function
    """
    from .axis.sila.axis_service.server import Server

    logger.info(f"Creating server for {device}")
    return Server(
        axis_system=device.device_handle,
        io_channels=device.io_channels,
        device_properties=device.device_properties,
        **server_args,
    )
