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
CONFIG_PATH = r'LocalConfig/GoDaddyDynDNS.ini'
LOG_FILENAME = r'LocalConfig/GoDaddyDynDNS.log'
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

DOMAINS = config.items('DOMAINS')
RECORD_TYPE = config['RECORD']['Record_Type']
RECORD_NAME = config['RECORD']['Record_Name']
API_KEY = config['CREDENTIALS']['GoDaddyAPI_Key']
API_SECRET = config['CREDENTIALS']['GoDaddyAPI_Secret']

try:
    logger.info('Getting Public IP')
    publicIP = get_public_ip()
    logger.info('Got Public IP: ' + publicIP)

except Exception as e:
    logger.error('Error Getting Public IP: ' + e.__str__())
    sys.exit()

for DOMAIN in DOMAINS:
    try:
        logger.info('Getting GoDaddy Records for ' + DOMAIN[1])
        godaddy_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
        client = Client(godaddy_acct)
        records = client.get_records(DOMAIN[1], record_type=RECORD_TYPE, name=RECORD_NAME)
        try:
            for record in records:
                if publicIP != record["data"]:
                    updateResult = client.update_record_ip(publicIP, DOMAIN[1], name=RECORD_NAME, record_type=RECORD_TYPE)
                    if updateResult is True:
                        logger.info('DNS Record Updated: ' + record["data"] + ' to ' + publicIP)
                else:
                    logger.info('DNS Record Update not Needed: ' + publicIP)

        except Exception as e:
            logger.error('Error Trying to Update DNS Record' + e.__str__())
            sys.exit()

    except Exception as e:
        logger.error('Error Getting GoDaddy Records: ' + e.__str__())


