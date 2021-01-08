#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: SiLA2_python

*MotionControl*

:details: MotionControl:
    Allows to control motion systems like axis systems

:file:    MotionControl_server.py
:authors: Florian Meinicke

:date: (creation)          2020-12-15T07:36:30.341671
:date: (last modification) 2020-12-15T07:36:30.341671

.. note:: Code generated by sila2codegenerator 0.2.0

________________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

import os
import logging
import argparse

# Import our server base class
from ..io.QmixIO_server import QmixIOServer

# Import gRPC libraries of features
from impl.de.cetoni.motioncontrol.axis.AxisSystemControlService.gRPC import AxisSystemControlService_pb2
from impl.de.cetoni.motioncontrol.axis.AxisSystemControlService.gRPC import AxisSystemControlService_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.motioncontrol.axis.AxisSystemControlService.AxisSystemControlService_default_arguments import default_dict as AxisSystemControlService_default_dict
from impl.de.cetoni.motioncontrol.axis.AxisSystemPositionController.gRPC import AxisSystemPositionController_pb2
from impl.de.cetoni.motioncontrol.axis.AxisSystemPositionController.gRPC import AxisSystemPositionController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.motioncontrol.axis.AxisSystemPositionController.AxisSystemPositionController_default_arguments import default_dict as AxisSystemPositionController_default_dict
from impl.de.cetoni.motioncontrol.axis.AxisPositionController.gRPC import AxisPositionController_pb2
from impl.de.cetoni.motioncontrol.axis.AxisPositionController.gRPC import AxisPositionController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.motioncontrol.axis.AxisPositionController.AxisPositionController_default_arguments import default_dict as AxisPositionController_default_dict
from impl.de.cetoni.core.ShutdownController.gRPC import ShutdownController_pb2
from impl.de.cetoni.core.ShutdownController.gRPC import ShutdownController_pb2_grpc
# import default arguments for this feature
from impl.de.cetoni.core.ShutdownController.ShutdownController_default_arguments import default_dict as ShutdownController_default_dict

# Import the servicer modules for each feature
from impl.de.cetoni.motioncontrol.axis.AxisSystemControlService.AxisSystemControlService_servicer import AxisSystemControlService
from impl.de.cetoni.motioncontrol.axis.AxisSystemPositionController.AxisSystemPositionController_servicer import AxisSystemPositionController
from impl.de.cetoni.motioncontrol.axis.AxisPositionController.AxisPositionController_servicer import AxisPositionController
from impl.de.cetoni.core.ShutdownController.ShutdownController_servicer import ShutdownController

# import qmixsdk
from qmixsdk import qmixmotion


class MotionControlServer(QmixIOServer):
    """
    Allows to control motion systems like axis systems
    """

    def __init__(
        self,
        cmd_args,
        axis_system: qmixmotion.AxisSystem,
        io_channels = [],
        device_properties: dict = {},
        simulation_mode: bool = True):
        """
        Class initialiser

            :param cmd_args: Arguments that were given on the command line
            :param axis_system: The qmixmotion.AxisSystem object that this server shall use
            :param io_channels: (optional) I/O channels of the axis system
            :param device_properties: (optional) Additional device properties that cannot be retrieved from QmixSDK functions
            :param simulation_mode: Sets whether at initialisation the simulation mode is active or the real mode
        """
        super().__init__(cmd_args, io_channels, simulation_mode=simulation_mode)

        data_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                                                 'features', 'de', 'cetoni', 'motioncontrol', 'axis'))

        # registering features
        #  Register de.cetoni.motioncontrol.axis.AxisSystemControlService
        self.AxisSystemControlService_servicer = AxisSystemControlService(
            axis_system=axis_system,
            sila2_conf=self.sila2_config,
            simulation_mode=self.simulation_mode
        )
        AxisSystemControlService_pb2_grpc.add_AxisSystemControlServiceServicer_to_server(
            self.AxisSystemControlService_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='AxisSystemControlService',
                         servicer=self.AxisSystemControlService_servicer,
                         data_path=data_path)
        #  Register de.cetoni.motioncontrol.axis.AxisSystemPositionController
        self.AxisSystemPositionController_servicer = AxisSystemPositionController(
            axis_system=axis_system,
            device_properties=device_properties,
            simulation_mode=self.simulation_mode
        )
        AxisSystemPositionController_pb2_grpc.add_AxisSystemPositionControllerServicer_to_server(
            self.AxisSystemPositionController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='AxisSystemPositionController',
                         servicer=self.AxisSystemPositionController_servicer,
                         data_path=data_path)
        #  Register de.cetoni.motioncontrol.axis.AxisPositionController
        self.AxisPositionController_servicer = AxisPositionController(
            axis_system=axis_system,
            simulation_mode=self.simulation_mode
        )
        AxisPositionController_pb2_grpc.add_AxisPositionControllerServicer_to_server(
            self.AxisPositionController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='AxisPositionController',
                         servicer=self.AxisPositionController_servicer,
                         data_path=data_path)

        #  Register de.cetoni.core.ShutdownController
        self.ShutdownController_servicer = ShutdownController(
            device=axis_system,
            server_name=self.server_name,
            sila2_conf=self.sila2_config,
            simulation_mode=simulation_mode
        )
        ShutdownController_pb2_grpc.add_ShutdownControllerServicer_to_server(
            self.ShutdownController_servicer,
            self.grpc_server
        )
        self.add_feature(feature_id='ShutdownController',
                            servicer=self.ShutdownController_servicer,
                            data_path=data_path.replace(os.path.join('motioncontrol', 'axis'), 'core'))

def parse_command_line():
    """
    Just looking for commandline arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 service: MotionControl")

    # Simple arguments for the server identification
    parser.add_argument('-s', '--server-name', action='store',
                        default="MotionControl", help='start SiLA server with [server-name]')
    parser.add_argument('-t', '--server-type', action='store',
                        default="Unknown Type", help='start SiLA server with [server-type]')
    parser.add_argument('-d', '--description', action='store',
                        default="Allows to control motion systems like axis systems", help='SiLA server description')

    # Encryption
    parser.add_argument('-X', '--encryption', action='store', default=None,
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    parsed_args = parser.parse_args()

    # validate/update some settings
    #   encryption
    if parsed_args.encryption is not None:
        # only overwrite the separate keys if not given manually
        if parsed_args.encryption_key is None:
            parsed_args.encryption_key = parsed_args.encryption + '.key'
        if parsed_args.encryption_cert is None:
            parsed_args.encryption_cert = parsed_args.encryption + '.cert'

    return parsed_args


if __name__ == '__main__':
    # or use logging.ERROR for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    args = parse_command_line()

    # generate SiLA2Server
    sila_server = MotionControlServer(cmd_args=args, simulation_mode=True)
