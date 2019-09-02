#!/usr/bin/env python

import sys
import logging
import configparser
from godaddypy import Client, Account
from pif import get_public_ip
from logging.handlers import RotatingFileHandler

#
# Constants
#
CONFIG_PATH = r'GoDaddyDynDNS.ini'
LOG_FILENAME = r'GoDaddyDynDNS.log'
'''
LOG_FILENAME = 'GoDaddyDynDNS.log' for Windows 
LOG_FILENAME = '/var/log/GoDaddyDynDNS.log' for Linux
'''
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
FORMATTER = logging.Formatter('[%(asctime)s]: %(message)s', DATE_FORMAT)

#
# Setup Logging
#

sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
sh.setFormatter(FORMATTER)

fh = RotatingFileHandler(LOG_FILENAME, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)
fh.setLevel(logging.DEBUG)
fh.setFormatter(FORMATTER)

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
logger.addHandler(sh)
logger.addHandler(fh)

#
# Import GoDaddyDynDNS.ini
#

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

DOMAIN = config['DOMAIN']['Domain_Name']
A_RECORD = config['DOMAIN']['A_Record']
API_KEY = config['CREDENTIALS']['GoDaddyAPI_Key']
API_SECRET = config['CREDENTIALS']['GoDaddyAPI_Secret']

try:
    logger.info('Getting Public IP')
    publicIP = get_public_ip()
    logger.info('Got Public IP: ' + publicIP)

    logger.info('Getting GoDaddy Records')
    godaddy_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
    client = Client(godaddy_acct)
    records = client.get_records(DOMAIN, record_type='A', name=A_RECORD)

    for record in records:
        if publicIP != record["data"]:
            updateResult = client.update_record_ip(publicIP, DOMAIN, name=A_RECORD, record_type='A')
            if updateResult is True:
                logger.info('DNS Record Updated: ' + record["data"] + ' to ' + publicIP)
        else:
            logger.info('DNS Record Update not Needed: ' + publicIP)

except Exception:
    logger.error(sys.exec_info()[1])
    sys.exit()
