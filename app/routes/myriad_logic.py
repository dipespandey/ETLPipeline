"""
Myriad API 1.0
myriad_logic.py
..................
contains endpoints for Myriad specific logics using the API
"""
import uuid
import base64
from . import routes


def generate_muid():
    return "myriadx-{}".format(str(uuid.uuid1()))
