from __future__ import annotations

from typing import Optional

from sila2.framework.errors.defined_execution_error import DefinedExecutionError

from .axissystempositioncontroller_feature import AxisSystemPositionControllerFeature


class MovementBlocked(DefinedExecutionError):
    def __init__(self, message: Optional[str] = None):
        if message is None:
            message = "The movement of the axis system is blocked and rotation is not allowed. Rotation is only allowed if the upper limit sensor is on - that means if the lift axis is in its topmost position."
        super().__init__(
            AxisSystemPositionControllerFeature.defined_execution_errors["MovementBlocked"], message=message
        )
