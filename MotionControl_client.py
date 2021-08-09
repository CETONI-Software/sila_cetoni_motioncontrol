#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*MotionControl client*

:details: MotionControl:
    Allows to control motion systems like axis systems

:file:    MotionControl_client.py
:authors: Florian Meinicke

:date: (creation)          2020-12-15T07:36:30.354320
:date: (last modification) 2021-07-09T10:33:31.619430

.. note:: Code generated by sila2codegenerator 0.3.6

_______________________________________________________________________

**Copyright**:
  This file is provided "AS IS" with NO WARRANTY OF ANY KIND,
  INCLUDING THE WARRANTIES OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

  For further Information see LICENSE file that comes with this distribution.
________________________________________________________________________
"""
__version__ = "0.1.0"

# import general packages
import logging
import argparse
import grpc
import time

# import meta packages
from typing import Union, Optional

# Import our client base class
from ..io.QmixIO_client import QmixIOClient

# import SiLA2 library modules
from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2
from sila2lib.framework.std_features import SiLAService_pb2 as SiLAService_feature_pb2
from sila2lib.error_handling import client_err
#   Usually not needed, but - feel free to modify
# from sila2lib.framework.std_features import SimulationController_pb2 as SimController_feature_pb2

# import feature gRPC modules
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

# import all feature clients
from impl.de.cetoni.motioncontrol.axis.AxisSystemControlService.AxisSystemControlService_client import AxisSystemControlServiceClient
from impl.de.cetoni.motioncontrol.axis.AxisSystemPositionController.AxisSystemPositionController_client import AxisSystemPositionControllerClient
from impl.de.cetoni.motioncontrol.axis.AxisPositionController.AxisPositionController_client import AxisPositionControllerClient
from impl.de.cetoni.core.ShutdownController.ShutdownController_client import ShutdownControllerClient



# noinspection PyPep8Naming, PyUnusedLocal
class MotionControlClient(QmixIOClient):
    """
        Allows to control motion systems like axis systems

    .. note:: For an example on how to construct the parameter or read the response(s) for command calls and properties,
              compare the default dictionary that is stored in the directory of the corresponding feature.
    """

    axisSystemControlService_client =  None
    axisSystemPositionController_client =  None
    axisPositionController_client =  None
    shutdownController_client =  None

    # The following variables will be filled when run() is executed
    #: Storage for the connected servers version
    server_version: str = ''
    #: Storage for the display name of the connected server
    server_display_name: str = ''
    #: Storage for the description of the connected server
    server_description: str = ''


    def __init__(self,
                 name: str = "MotionControlClient",
                 description: str = "Allows to control motion systems like axis systems",
                 server_name: Optional[str] = None,
                 client_uuid: Optional[str] = None,
                 version: str = __version__,
                 vendor_url: str = "cetoni.de",
                 server_hostname: str = "localhost",
                 server_ip: str = "127.0.0.1", server_port: int = 50052,
                 cert_file: Optional[str] = None):
        """Class initialiser"""
        super().__init__(
            name=name, description=description,
            server_name=server_name,
            client_uuid=client_uuid,
            version=version,
            vendor_url=vendor_url,
            server_hostname=server_hostname, server_ip=server_ip, server_port=server_port,
            cert_file=cert_file
        )

        logging.info(
            f"Starting SiLA2 service client for service MotionControl with service name: {name}"
        )

        self.axisSystemControlService_client = AxisSystemControlServiceClient(self.channel)
        self.axisSystemPositionController_client = AxisSystemPositionControllerClient(self.channel)
        self.axisPositionController_client = AxisPositionControllerClient(self.channel)
        self.shutdownController_client = ShutdownControllerClient(self.channel)


        # initialise class variables for server information storage
        self.server_version = ''
        self.server_display_name = ''
        self.server_description = ''

    def run(self, show_info: bool = True) -> bool:
        """
        Starts the actual client and retrieves the meta-information from the server.

        :returns: True or False whether the connection to the server is established.
        """
        # type definition, just for convenience
        grpc_err: grpc.Call

        if show_info:
            self.get_all_server_connection_info()

        return True

    def stop(self, force: bool = False) -> bool:
        """
        Stop SiLA client routine

        :param force: If set True, the client is supposed to disconnect and stop immediately. Otherwise it can first try
                      to finish what it is doing.

        :returns: Whether the client could be stopped successfully or not.
        """
        # TODO: Implement all routines that have to be executed when the client is stopped.
        #   Feel free to use the "force" parameter to abort any running processes. Or crash your machine. Your call!
        return True

    @staticmethod
    def grpc_error_handling(error_object: grpc.Call) -> None:
        """Handles exceptions of type grpc.RpcError"""
        # pass to the default error handling
        grpc_error =  client_err.grpc_error_handling(error_object=error_object)

        # Access more details using the return value fields
        logging.error(grpc_error.error_type)
        if hasattr(grpc_error.message, "parameter"):
            logging.error(grpc_error.message.parameter)
        logging.error(grpc_error.message.message)

def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(description="A SiLA2 client: MotionControl")

    # connection parameters
    parser.add_argument('-i', '--server-ip-address', action='store', default='127.0.0.1',
                        help='SiLA server IP address')
    parser.add_argument('--server-hostname', action='store', default='localhost',
                        help='SiLA server hostname')
    parser.add_argument('-p', '--server-port', action='store', default=50052,
                        help='SiLA server port')

    # encryption
    parser.add_argument('-X', '--encryption', action='store', default='sila2_server',
                        help='The name of the private key and certificate file (without extension).')
    parser.add_argument('--encryption-key', action='store', default=None,
                        help='The name of the encryption key (*with* extension). Can be used if key and certificate '
                             'vary or non-standard file extensions are used.')
    parser.add_argument('--encryption-cert', action='store', default=None,
                        help='The name of the encryption certificate (*with* extension). Can be used if key and '
                             'certificate vary or non-standard file extensions are used.')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    return parser.parse_args()


if __name__ == '__main__':
    # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    parsed_args = parse_command_line()

    # start the server
    sila_client = MotionControlClient(server_ip=parsed_args.server_ip_address,
                                        server_port=int(parsed_args.server_port))
    sila_client.run()

    # Log connection info
    logging.info(
        (
            f'Connected to SiLA Server {sila_client.server_display_name} running in version {sila_client.server_version}.' '\n'
            f'Service description: {sila_client.server_description}'
        )
    )

    # TODO:
    #   Use a separate module, like the test client to run the client as a standalone application.
