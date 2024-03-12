#!/usr/bin/env python
"""Demo of changing face on Misty II via rerobots API

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
# https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#changeled
res = requests.post(MPURL + '/api/led', json={
    'red': 0,
    'green': 255,
    'blue': 0,
})
assert res.ok, 'response from POST /api/led: {} {}'.format(res.status_code, res.reason)

# Tilt the head forward
# https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movehead
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
# https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movehead
res = requests.post(MPURL + '/api/head', json={
    'Pitch': 0,
    'Roll': 0,
    'Yaw': 0,
    'Velocity': 3,
})
assert res.ok, 'response from POST /api/head: {} {}'.format(res.status_code, res.reason)

# Change the color of the chest LED to purple
# https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#changeled
res = requests.post(MPURL + '/api/led', json={
    'red': 255,
    'green': 0,
    'blue': 255,
})
assert res.ok, 'response from POST /api/led: {} {}'.format(res.status_code, res.reason)


# Move the arms
# https://docs.mistyrobotics.com/misty-ii/web-api/api-reference/#movearms
res = requests.post(MPURL + '/api/arms/set', json={
    'LeftArmPosition': -20,
    'RightArmPosition': -20,
    'LeftArmVelocity': 40,
    'RightArmVelocity': 40,
})
assert res.ok, 'response from POST /api/arms/set: {} {}'.format(res.status_code, res.reason)

# Sleep for 2 seconds to allow arms to complete motion
time.sleep(2)

res = requests.post(MPURL + '/api/arms/set', json={
    'LeftArmPosition': 90,
    'RightArmPosition': 90,
    'LeftArmVelocity': 40,
    'RightArmVelocity': 40,
})
assert res.ok, 'response from POST /api/arms/set: {} {}'.format(res.status_code, res.reason)


def drive_fwd(mpurl, duration):
    """Drive forward for given duration (ms)
    """
    params = {
        'LinearVelocity': 15,
        'AngularVelocity': 0,
        'TimeMS': duration,
    }
    res = requests.post(mpurl + '/api/drive/time', json=params)
    if not res.ok:
        print('response from POST /api/drive/time:',
              res.status_code,
              res.reason)

# Drive forward for 2 seconds (2000 milliseconds)
drive_fwd(MPURL, 2000)
time.sleep(2)
