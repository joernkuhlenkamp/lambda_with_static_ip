import json
import logging
import datetime
from requests import get

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)

def main(event, context):
    ip = get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))

if __name__ == '__main__':
    main({}, {})