#! /usr/bin/python3.5

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/pi/PycharmProjects/doc_system')
from app import app as application
application.secret_key = "kl2j45rlkh24r5o[i2345"
