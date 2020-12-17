# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import AxisPositionController_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()
default_dict['DataType_Velocity'] = {
    'Velocity': silaFW_pb2.Real(value=0.0)
}

default_dict['MoveToPosition_Parameters'] = {
    'Position': silaFW_pb2.Real(value=0.0),
    'Velocity': pb2.DataType_Velocity(**default_dict['DataType_Velocity'])
}

default_dict['MoveToPosition_Responses'] = {
    
}

default_dict['MoveToHomePosition_Parameters'] = {
    
}

default_dict['MoveToHomePosition_Responses'] = {
    
}

default_dict['StopMoving_Parameters'] = {
    
}

default_dict['StopMoving_Responses'] = {
    
}

default_dict['Subscribe_Position_Responses'] = {
    'Position': silaFW_pb2.Real(value=0.0)
}

default_dict['Get_PositionUnit_Responses'] = {
    'PositionUnit': silaFW_pb2.String(value='default string')
}

default_dict['Get_MinimumPosition_Responses'] = {
    'MinimumPosition': silaFW_pb2.Real(value=0.0)
}

default_dict['Get_MaximumPosition_Responses'] = {
    'MaximumPosition': silaFW_pb2.Real(value=0.0)
}

default_dict['Get_MinimumVelocity_Responses'] = {
    'MinimumVelocity': pb2.DataType_Velocity(**default_dict['DataType_Velocity'])
}

default_dict['Get_MaximumVelocity_Responses'] = {
    'MaximumVelocity': pb2.DataType_Velocity(**default_dict['DataType_Velocity'])
}

default_dict['Get_FCPAffectedByMetadata_AxisIdentifier_Responses'] = {
    'AffectedCalls': [silaFW_pb2.String(value='default string')]
}
