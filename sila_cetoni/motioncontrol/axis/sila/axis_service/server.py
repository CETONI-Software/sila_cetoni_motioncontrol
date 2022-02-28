from typing import Dict, List, Optional, Union
from uuid import UUID

from qmixsdk.qmixmotion import AxisSystem

from ....io.io_service.server import Server as IOServer
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
        super().__init__(
            io_channels,
            server_name=server_name or "Axis Service",
            server_type=server_type or "TestServer",
            server_description=server_description
            or "The SiLA 2 driver for CETONI sample handlers and positioning systems",
            server_version=server_version or "0.1.0",
            server_vendor_url=server_vendor_url or "https://www.cetoni.com",
            server_uuid=server_uuid,
        )

        self.axispositioncontroller = AxisPositionControllerImpl(axis_system, self.child_task_executor)
        self.axissystemcontrolservice = AxisSystemControlServiceImpl(axis_system, self.child_task_executor)
        self.axissystempositioncontroller = AxisSystemPositionControllerImpl(
            axis_system, device_properties, self.child_task_executor
        )

        self.set_feature_implementation(AxisPositionControllerFeature, self.axispositioncontroller)
        self.set_feature_implementation(AxisSystemControlServiceFeature, self.axissystemcontrolservice)
        self.set_feature_implementation(AxisSystemPositionControllerFeature, self.axissystempositioncontroller)
        # TODO shutdown controller
