from __future__ import annotations

from typing import Dict, List, Optional, Union
from uuid import UUID

from qmixsdk.qmixmotion import AxisSystem

from sila_cetoni.io.sila.io_service.server import Server as IOServer

from .feature_implementations.axispositioncontroller_impl import AxisPositionControllerImpl
from .feature_implementations.axissystemcontrolservice_impl import AxisSystemControlServiceImpl
from .feature_implementations.axissystempositioncontroller_impl import AxisSystemPositionControllerImpl
from .generated.axispositioncontroller import AxisPositionControllerFeature
from .generated.axissystemcontrolservice import AxisSystemControlServiceFeature
from .generated.axissystempositioncontroller import AxisSystemPositionControllerFeature


class Server(IOServer):
    def __init__(
        self,
        axis_system: AxisSystem,
        io_channels: List = [],
        device_properties: Dict = {},
        server_name: str = "",
        server_type: str = "",
        server_description: str = "",
        server_version: str = "",
        server_vendor_url: str = "",
        server_uuid: Optional[Union[str, UUID]] = None,
    ):
        from .... import __version__

        super().__init__(
            io_channels,
            server_name=server_name or "Axis Service",
            server_type=server_type or "TestServer",
            server_description=server_description
            or "The SiLA 2 driver for CETONI sample handlers and positioning systems",
            server_version=server_version or __version__,
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        self.axispositioncontroller = AxisPositionControllerImpl(self, axis_system)
        self.axissystemcontrolservice = AxisSystemControlServiceImpl(self, axis_system)
        self.axissystempositioncontroller = AxisSystemPositionControllerImpl(self, axis_system, device_properties)

        self.set_feature_implementation(AxisPositionControllerFeature, self.axispositioncontroller)
        self.set_feature_implementation(AxisSystemControlServiceFeature, self.axissystemcontrolservice)
        self.set_feature_implementation(AxisSystemPositionControllerFeature, self.axissystempositioncontroller)
        # TODO shutdown controller
