from __future__ import annotations

from typing import TYPE_CHECKING

from sila2.client import SilaClient

from .axispositioncontroller import AxisPositionControllerFeature, InvalidAxisIdentifier
from .axissystempositioncontroller import AxisSystemPositionControllerFeature, MovementBlocked

if TYPE_CHECKING:

    from .axispositioncontroller import AxisPositionControllerClient
    from .axissystemcontrolservice import AxisSystemControlServiceClient
    from .axissystempositioncontroller import AxisSystemPositionControllerClient


class Client(SilaClient):

    AxisPositionController: AxisPositionControllerClient

    AxisSystemControlService: AxisSystemControlServiceClient

    AxisSystemPositionController: AxisSystemPositionControllerClient

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._register_defined_execution_error_class(
            AxisPositionControllerFeature.defined_execution_errors["InvalidAxisIdentifier"], InvalidAxisIdentifier
        )

        self._register_defined_execution_error_class(
            AxisSystemPositionControllerFeature.defined_execution_errors["MovementBlocked"], MovementBlocked
        )
