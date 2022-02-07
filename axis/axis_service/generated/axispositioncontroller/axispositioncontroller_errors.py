from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .axispositioncontroller_feature import AxisPositionControllerFeature


class InvalidAxisIdentifier(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The sent Axis Identifier is not known"
        super().__init__(
            AxisPositionControllerFeature.defined_execution_errors["InvalidAxisIdentifier"], message=message
        )
