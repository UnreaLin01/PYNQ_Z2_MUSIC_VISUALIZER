# SPDX-License-Identifier: GPL-3.0-or-later
# File: main.py
# Author: William Lin
# Copyright (C) 2025 William Lin
#
# This file is part of a project that is licensed under the terms of the
# GNU General Public License v3.0 or later. You should have received a copy
# of the license with this file. If not, see <https://www.gnu.org/licenses/>.

import sounddevice as sd
import numpy as np
import socket
from datetime import datetime

SAMPLERATE = 48000
CHUNK = 960
DEVICE = 18
UDP_IP = "192.168.1.37"
UDP_PORT = 5005

print("Device List:")
print(sd.query_devices())

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def callback(indata, frames, time_info, status):
    audio = indata[:, 0]
    rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
    sock.sendto(audio.tobytes(), (UDP_IP, UDP_PORT))
    #print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent {audio.size} samples to {UDP_IP}:{UDP_PORT}, RMS: {rms:.2f}")

try:
    with sd.InputStream(
        device=DEVICE,
        #channels=0,
        samplerate=SAMPLERATE,
        dtype='int16',
        blocksize=CHUNK,
        callback=callback,
        latency='low'
    ):
        while True:
            sd.sleep(1000)

except Exception as e:
    print(e)