#!/usr/bin/env python
# Copyright (C) 2020 rerobots, Inc.
# This is free software, released under the Apache License, Version 2.0.
# You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
from __future__ import print_function
import functools
import json
from queue import Queue
import random
from threading import Thread

# https://requests.readthedocs.io/en/stable/
import requests

# https://pypi.org/project/websocket_client/
# https://github.com/websocket-client/websocket-client.git
import websocket


def on_open(ws, recog_event_name, training_event_name):
    ws.send(json.dumps({
        'Operation': 'subscribe',
        'Type': 'FaceRecognition',
        'DebounceMS': None,
        'EventName': recog_event_name,
        'Message': '',
        'ReturnProperty': None,
    }))
    ws.send(json.dumps({
        'Operation': 'subscribe',
        'Type': 'FaceTraining',
        'DebounceMS': None,
        'EventName': training_event_name,
        'Message': '',
        'ReturnProperty': None,
    }))

def on_message(ws, msg, q):
    q.put(json.loads(msg))

def main_ws(mpurl, hon_open, hon_message):
    ws = websocket.WebSocketApp(mpurl + '/pubsub', on_open=hon_open, on_message=hon_message)
    ws.run_forever()


class LearnAndTrack(object):
    def __init__(self, mpurl):
        self.mpurl = mpurl
        self.recog_event_name = 'fr{}'.format(random.randint(0,1000))
        self.training_event_name = 'tr{}'.format(random.randint(0,1000))

    def clear_past(self):
        assert requests.post(self.mpurl + '/api/faces/detection/stop').ok
        assert requests.post(self.mpurl + '/api/faces/recognition/stop').ok
        assert requests.delete(self.mpurl + '/api/faces').ok

    def start_ws(self, hon_open, hon_message):
        if self.mpurl.startswith('https:'):
            mpurl = 'wss' + self.mpurl[5:]
        elif self.mpurl.startswith('http:'):
            mpurl = 'ws' + self.mpurl[4:]
        th = Thread(target=main_ws, args=(mpurl, hon_open, hon_message))
        th.start()
        return th

    def start(self):
        assert requests.post(self.mpurl + '/api/faces/recognition/start').ok
        assert requests.post(self.mpurl + '/api/faces/training/start', json={'FaceId': 'neighbour'}).ok
        q = Queue()
        hon_open = functools.partial(on_open, recog_event_name=self.recog_event_name, training_event_name=self.training_event_name)
        hon_message = functools.partial(on_message, q=q)
        th = self.start_ws(hon_open, hon_message)
        while True:
            msg = q.get()
            if msg['eventName'] == self.training_event_name:
                if isinstance(msg['message'], dict) and msg['message']['isProcessComplete']:
                    print('face training complete!')
            elif msg['eventName'] == self.recog_event_name:
                if isinstance(msg['message'], str):
                    print(msg['message'])
                else:
                    print('detected: {}'.format(msg['message']))
            else:
                print('rx: {}'.format(msg))


if __name__ == '__main__':
    # rerobots mistyproxy URL
    MPURL = ''

    params = {
        'Pitch': 0,
        'Roll': 0,
        'Yaw': 10,
        'Velocity': 80,
        'Units': 'degrees',
    }
    res = requests.post(MPURL + '/api/head', json=params)
    if not res.ok:
        print('response from POST /api/head: {} {}'.format(res.status_code, res.reason))

    lt = LearnAndTrack(MPURL)
    lt.clear_past()
    lt.start()
