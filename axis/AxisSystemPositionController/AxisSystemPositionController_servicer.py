"""
________________________________________________________________________

:PROJECT: sila_cetoni

*Axis System Position Controller*

:details: AxisSystemPositionController:
    Allows to control the position of an axis system

:file:    AxisSystemPositionController_servicer.py
:authors: Florian Meinicke

:date: (creation)          2020-12-15T07:50:56.817849
:date: (last modification) 2021-07-09T10:33:22.745789

.. note:: Code generated by sila2codegenerator 0.3.6

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""

__version__ = "0.1.0"

# import general packages
import logging
import grpc

# meta packages
from typing import Union

# import SiLA2 library
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
from impl.common.qmix_errors import QmixSDKSiLAError, SiLAError, DeviceError

# import gRPC modules for this feature
from .gRPC import AxisSystemPositionController_pb2 as AxisSystemPositionController_pb2
from .gRPC import AxisSystemPositionController_pb2_grpc as AxisSystemPositionController_pb2_grpc

# import simulation and real implementation
from .AxisSystemPositionController_simulation import AxisSystemPositionControllerSimulation
from .AxisSystemPositionController_real import AxisSystemPositionControllerReal

# import SiLA Defined Error factories
from .AxisSystemPositionController_defined_errors import MovementBlockedError

class AxisSystemPositionController(AxisSystemPositionController_pb2_grpc.AxisSystemPositionControllerServicer):
    """
    Allows to control motion systems like axis systems
    """
    implementation: Union[AxisSystemPositionControllerSimulation, AxisSystemPositionControllerReal]
    simulation_mode: bool

    def __init__(self, axis_system, device_properties: dict, simulation_mode: bool = True):
        """
        Class initialiser.

        :param axis_system: The axis system that this feature shall operate on
        :param device_properties: Additional device properties
        :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode.
        """

        self.axis_system = axis_system
        self.device_properties = device_properties

        self.simulation_mode = simulation_mode
        if simulation_mode:
            self.switch_to_simulation_mode()
        else:
            self.switch_to_real_mode()

    def _inject_implementation(self,
                               implementation: Union[AxisSystemPositionControllerSimulation,
                                                     AxisSystemPositionControllerReal]
                               ) -> bool:
        """
        Dependency injection of the implementation used.
            Allows to set the class used for simulation/real mode.

        :param implementation: A valid implementation of the MotionControlServicer.
        """

        self.implementation = implementation
        return True

    def switch_to_simulation_mode(self):
        """Method that will automatically be called by the server when the simulation mode is requested."""
        self.simulation_mode = True
        self._inject_implementation(AxisSystemPositionControllerSimulation())

    def switch_to_real_mode(self):
        """Method that will automatically be called by the server when the real mode is requested."""
        self.simulation_mode = False
        self._inject_implementation(AxisSystemPositionControllerReal(self.axis_system, self.device_properties))

    def MoveToPosition(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.CommandConfirmation:
        """
        Executes the observable command "Move To Position"
            Move the axis system to the given position with a certain velocity

        :param request: gRPC request containing the parameters passed:
            request.Position (Position): The position to move to
            request.Velocity (Velocity): A real value between 0 (exclusive) and 100 (inclusive) defining the relative speed at which all axes of the axis system should move.The velocity value is multiplied with the maximum velocity value of each axis. So a value of 100 means, all axes travel with their maximum velocity. A value of 50 means, all axes travel with the half of the maximum velocity.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A command confirmation object with the following information:
            commandId: A command id with which this observable command can be referenced in future calls
            lifetimeOfExecution: The (maximum) lifetime of this command call.
        """

        logging.debug(
            "MoveToPosition called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        # parameter validation
        # if request.my_paramameter.value out of scope :
        #        sila_val_err = SiLAValidationError(parameter="myParameter",
        #                                           msg=f"Parameter {request.my_parameter.value} out of scope!")
        #        sila_val_err.raise_rpc_error(context)

        try:
            return self.implementation.MoveToPosition(request, context)
        except (SiLAError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context=context)

    def MoveToPosition_Info(self, request, context: grpc.ServicerContext) \
            -> silaFW_pb2.ExecutionInfo:
        """
        Returns execution information regarding the command call :meth:`~.MoveToPosition`.

        :param request: A request object with the following properties
            CommandExecutionUUID: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: An ExecutionInfo response stream for the command with the following fields:
            commandStatus: Status of the command (enumeration)
            progressInfo: Information on the progress of the command (0 to 1)
            estimatedRemainingTime: Estimate of the remaining time required to run the command
            updatedLifetimeOfExecution: An update on the execution lifetime
        """

        logging.debug(
            "MoveToPosition_Info called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            for value in self.implementation.MoveToPosition_Info(request, context):
                yield value
        except (SiLAError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context=context)

    def MoveToPosition_Result(self, request, context: grpc.ServicerContext) \
            -> AxisSystemPositionController_pb2.MoveToPosition_Responses:
        """
        Returns the final result of the command call :meth:`~.MoveToPosition`.

        :param request: A request object with the following properties
            CommandExecutionUUID: The UUID of the command executed.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "MoveToPosition_Result called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            return self.implementation.MoveToPosition_Result(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)


    def MoveToHomePosition(self, request, context: grpc.ServicerContext) \
            -> AxisSystemPositionController_pb2.MoveToHomePosition_Responses:
        """
        Executes the unobservable command "Move To Home Position"
            Move the axis system to its home position. The axis system should manage the order of the movement and should know how to move all axes into a home state.

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "MoveToHomePosition called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        # parameter validation
        # if request.my_paramameter.value out of scope :
        #        sila_val_err = SiLAValidationError(parameter="myParameter",
        #                                           msg=f"Parameter {request.my_parameter.value} out of scope!")
        #        sila_val_err.raise_rpc_error(context)

        try:
            return self.implementation.MoveToHomePosition(request, context)
        except (SiLAError, DeviceError) as err:
            if isinstance(err, DeviceError):
                err = QmixSDKSiLAError(err)
            err.raise_rpc_error(context=context)

    def StopMoving(self, request, context: grpc.ServicerContext) \
            -> AxisSystemPositionController_pb2.StopMoving_Responses:
        """
        Executes the unobservable command "Stop Moving"
            Immediately stops all movement of the axis system

        :param request: gRPC request containing the parameters passed:
            request.EmptyParameter (Empty Parameter): An empty parameter data type used if no parameter is required.
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: The return object defined for the command with the following fields:
            EmptyResponse (Empty Response): An empty response data type used if no response is required.
        """

        logging.debug(
            "StopMoving called in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )

        # parameter validation
        # if request.my_paramameter.value out of scope :
        #        sila_val_err = SiLAValidationError(parameter="myParameter",
        #                                           msg=f"Parameter {request.my_parameter.value} out of scope!")
        #        sila_val_err.raise_rpc_error(context)

        try:
            return self.implementation.StopMoving(request, context)
        except SiLAError as err:
            err.raise_rpc_error(context=context)

    def Subscribe_Position(self, request, context: grpc.ServicerContext) \
            -> AxisSystemPositionController_pb2.Subscribe_Position_Responses:
        """
        Requests the observable property Position
            The current XY position of the axis system

        :param request: An empty gRPC request object (properties have no parameters)
        :param context: gRPC :class:`~grpc.ServicerContext` object providing gRPC-specific information

        :returns: A response stream with the following fields:
            Position (Position): The current XY position of the axis system
        """

        logging.debug(
            "Property Position requested in {current_mode} mode".format(
                current_mode=('simulation' if self.simulation_mode else 'real')
            )
        )
        try:
            for value in self.implementation.Subscribe_Position(request, context):
                yield value
        except SiLAError as err:
            err.raise_rpc_error(context=context)
