#!/usr/bin/env python3
"""
________________________________________________________________________

:PROJECT: sila_cetoni

*MotionControl test client*

:details: MotionControl:
    Allows to control motion systems like axis systems

:file:    MotionControl_testclient.py
:authors: Florian Meinicke

:date: (creation)          2021-07-09T10:33:33.517625
:date: (last modification) 2021-07-09T10:33:33.517625

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
import time
import datetime

# import meta packages
from typing import Union, Optional

# import SiLA client module
from .MotionControl_client import MotionControlClient


def parse_command_line():
    """
    Just looking for command line arguments
    """
    parser = argparse.ArgumentParser(
        description="A SiLA2 test client for: MotionControl")

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

    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ' + __version__)

    return parser.parse_args()


if __name__ == '__main__':
    # or use logging.INFO (=20) or logging.ERROR (=30) for less output
    logging.basicConfig(
        format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

    parsed_args = parse_command_line()

    # start the client
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
    #   Uncomment the calls you would like to test and remove type hints (given only for orientation) or
    #   write your further function calls here to run the client as a standalone application.

    # ------------- command calls -------------------

    # ----- de/cetoni/motioncontrol/axis/AxisSystemControlService
    # results = sila_client.axis_system_control_service.EnableAxisSystem()
    # print("EnableAxisSystem res: ", results)

    # results = sila_client.axis_system_control_service.DisableAxisSystem()
    # print("DisableAxisSystem res: ", results)

    # results = sila_client.axis_system_control_service.ClearFaultState()
    # print("ClearFaultState res: ", results)

    # ----- de/cetoni/motioncontrol/axis/AxisSystemPositionController
    # results = sila_client.axis_system_position_controller.MoveToPosition(Position: None = None,Velocity: int = 1)
    # print("AxisSystemPositionController MoveToPosition res: ", results)

    # results = sila_client.axis_system_position_controller.MoveToHomePosition()
    # print("MoveToHomePosition res: ", results)

    # results = sila_client.axis_system_position_controller.StopMoving()
    # print("StopMoving res: ", results)

    # ----- de/cetoni/motioncontrol/axis/AxisPositionController
    # results = sila_client.axis_position_controller.MoveToPosition(Position: float = 1.0,Velocity: float = 1.0)
    # print("AxisPositionController MoveToPosition res: ", results)

    # results = sila_client.axis_position_controller.MoveToHomePosition()
    # print("MoveToHomePosition res: ", results)

    # results = sila_client.axis_position_controller.StopMoving()
    # print("StopMoving res: ", results)

    # ----- de/cetoni/core/ShutdownController
    # results = sila_client.shutdown_controller.Shutdown()
    # print("Shutdown res: ", results)


    # ------------- property calls -------------------

    # ----- de/cetoni/motioncontrol/axis/AxisSystemControlService
    # results = sila_client.axis_system_control_service.Get_AvailableAxes()
    # print("AvailableAxes res: ", results)

    # results = sila_client.axis_system_control_service.Subscribe_AxisSystemState()
    # print("AxisSystemState res: ", results)

    # results = sila_client.axis_system_control_service.Subscribe_AxesInFaultState()
    # print("AxesInFaultState res: ", results)

    # ----- de/cetoni/motioncontrol/axis/AxisSystemPositionController
    # results = sila_client.axis_system_position_controller.Subscribe_Position()
    # print("AxisSystemPositionController Position res: ", results)

    # ----- de/cetoni/motioncontrol/axis/AxisPositionController
    # results = sila_client.axis_position_controller.Subscribe_Position()
    # print("AxisPositionController Position res: ", results)

    # results = sila_client.axis_position_controller.Get_PositionUnit()
    # print("PositionUnit res: ", results)

    # results = sila_client.axis_position_controller.Get_MinimumPosition()
    # print("MinimumPosition res: ", results)

    # results = sila_client.axis_position_controller.Get_MaximumPosition()
    # print("MaximumPosition res: ", results)

    # results = sila_client.axis_position_controller.Get_MinimumVelocity()
    # print("MinimumVelocity res: ", results)

    # results = sila_client.axis_position_controller.Get_MaximumVelocity()
    # print("MaximumVelocity res: ", results)

    # ----- de/cetoni/core/ShutdownController


    # ------------- metadata calls -------------------

    # results = sila_client.AxisPositionController_client.Get_FCPAffectedByMetadata_AxisIdentifier()
    # print("FCPAffectedByMetadata_AxisIdentifier res: ", results)


