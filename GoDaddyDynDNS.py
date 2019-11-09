#!/usr/bin/env python

import configparser
import logging
import sys
import time

from godaddypy import Client, Account
from logging.handlers import RotatingFileHandler
from pif import get_public_ip

start_time = time.time()

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
FORMATTER = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s', DATE_FORMAT)

#
# Setup Logging
#
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.INFO)
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

try:
    DOMAINS = config.items('DOMAINS')
    RECORD_TYPE = config['RECORD']['Record_Type']
    RECORD_NAME = config['RECORD']['Record_Name']
    API_KEY = config['CREDENTIALS']['GoDaddyAPI_Key']
    API_SECRET = config['CREDENTIALS']['GoDaddyAPI_Secret']

except KeyError:
    logger.error('Error loading ini: check ini exists and settings are correct')
    quit()

try:
    logger.debug('Getting Public IP')
    publicIP = get_public_ip()
    logger.info('Got Public IP: ' + publicIP)

except Exception as e:
    logger.error('Error Getting Public IP: ' + e.__str__())
    sys.exit()

for DOMAIN in DOMAINS:
    try:
        logger.debug('Getting GoDaddy Records for ' + DOMAIN[1])
        godaddy_acct = Account(api_key=API_KEY, api_secret=API_SECRET)
        client = Client(godaddy_acct)
        records = client.get_records(DOMAIN[1], record_type=RECORD_TYPE, name=RECORD_NAME)
        try:
            for record in records:
                if publicIP != record["data"]:
                    updateResult = client.update_record_ip(publicIP, DOMAIN[1], name=RECORD_NAME,
                                                           record_type=RECORD_TYPE)
                    if updateResult is True:
                        logger.info('DNS Record Updated for ' + DOMAIN[1] + ':' + record["data"] + ' to ' + publicIP)
                else:
                    logger.info('DNS Record Update not Needed for ' + DOMAIN[1] + ':' + publicIP)

        except Exception as e:
            logger.error('Error Trying to Update DNS Record' + e.__str__())
            sys.exit()

    except Exception as e:
        logger.error('Error Getting GoDaddy Records: ' + e.__str__())

logger.info("Code Executed in %s Seconds", (time.time() - start_time))


