#!/usr/bin/env python3

import os
import json
import logging
import sys
import time
from urllib3 import add_stderr_logger
import telepot
from itertools import chain
from datetime import date
from datetime import datetime
from telepot.loop import MessageLoop


log = logging.getLogger(__name__)
out_hdlr = logging.StreamHandler(sys.stdout)
out_hdlr.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
out_hdlr.setLevel(logging.INFO)
log.addHandler(out_hdlr)
log.setLevel(logging.INFO)

steps = {
        "punta": {
            "hours": [int(x) for x in list(chain(range(10, 14), range(18, 22)))],
            "alt": "cara"
        },
        "llana": {
            "hours": [int(x) for x in list(chain(range(8, 10), range(14, 18), range(22, 24)))],
            "alt": "intermedia"
        },
        "valle": {
            "hours": [int(x) for x in list(range(0, 8))],
            "alt": "barata"
        }
    }


def get_step(hour, weekend):
    if weekend:
        log.info("--> today is weekend")
        return "valle"
    else:
        for key, value in steps.items():
            if hour in value['hours']:
                log.info("--> {} in {}".format(hour,
                                               value['hours']))
                return key


def get_text():
    curr_time = datetime.now()
    curr_date = date.today()
    week_day_number = datetime.today().weekday()
    step = get_step(int(curr_time.strftime("%H")), week_day_number >= 5)
    return "Son las {} del {}, estás en el tramo '{}' ({})".format(curr_time.strftime("%H:%M"),
                                                                   curr_date.strftime("%d/%m/%Y"),
                                                                   step,
                                                                   steps[step]['alt'])


def handle(msg):
    _, _, chat_id = telepot.glance(msg)
    log.info(json.dumps(msg, indent=3) + '\n')
    if msg['text'] == '/tramo':
        telegram.sendMessage(chat_id, text=get_text())


if __name__ == "__main__":
    token = os.environ.get('TELEGRAM_TOKEN', None)
    if not token:
        log.error("Environment variable 'TELEGRAM_TOKEN' is not defined")
        sys.exit(1)
    telegram = telepot.Bot(token)
    MessageLoop(telegram, handle).run_as_thread()
    while 1:
        time.sleep(300)
