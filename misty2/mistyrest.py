#!/usr/bin/env python
"""Demo of changing face on Misty II Field Trial via rerobots API

Besides standard Python libraries, this example code requires
`requests` (https://pypi.org/project/requests/).


This is free software, released under the Apache License, Version 2.0.
You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0

Copyright (c) 2019 rerobots, Inc.
"""
import time

import requests


# TODO: put here the https URL from the "Misty robot proxy" panel of
# your instance details page under https://rerobots.net/instances
#
# For example,
#
#     MPURL = 'https://proxy.rerobots.net/7947941869cbaf5e8bc75d80fd7ea8307ec67f16ee84c1043dcbeae85aaf3d28/mistyproxy/5de82c965c7544e25321b5323e5f72e841c74a7c6f5ae25015ddaaaee26d9fdd'
MPURL = ''


# Change the color of the chest LED to green
# https://docs.mistyrobotics.com/docs/reference/rest/#changeled
res = requests.post(MPURL + '/api/led', json={
    'red': 0,
    'green': 255,
    'blue': 0,
})
assert res.ok, 'response from POST /api/led: {} {}'.format(res.status_code, res.reason)

# Tilt the head forward
# https://docs.mistyrobotics.com/docs/reference/rest/#movehead
res = requests.post(MPURL + '/api/head', json={
    'Pitch': 20,
    'Roll': 0,
    'Yaw': 0,
    'Velocity': 3,
})
assert res.ok, 'response from POST /api/head: {} {}'.format(res.status_code, res.reason)

# Sleep for 5 seconds to allow more time for human to observe results
time.sleep(5)

# Tilt the head back
# https://docs.mistyrobotics.com/docs/reference/rest/#movehead
res = requests.post(MPURL + '/api/head', json={
    'Pitch': 0,
    'Roll': 0,
    'Yaw': 0,
    'Velocity': 3,
})
assert res.ok, 'response from POST /api/head: {} {}'.format(res.status_code, res.reason)

# Change the color of the chest LED to purple
# https://docs.mistyrobotics.com/docs/reference/rest/#changeled
res = requests.post(MPURL + '/api/led', json={
    'red': 255,
    'green': 0,
    'blue': 255,
})
assert res.ok, 'response from POST /api/led: {} {}'.format(res.status_code, res.reason)
