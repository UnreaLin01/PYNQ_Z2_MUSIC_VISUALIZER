# -*- coding: utf-8 -*-
# SPDX-License-Identifier: GPL-3.0-or-later
# File: main.py
# Author: William Lin
# Copyright (C) 2025 William Lin
#
# This file is part of a project that is licensed under the terms of the
# GNU General Public License v3.0 or later. You should have received a copy
# of the license with this file. If not, see <https://www.gnu.org/licenses/>.

from pynq import Overlay, allocate, MMIO, PL
from pynq.lib import AxiGPIO
from collections import deque
import time
import matplotlib.pyplot as plt
import numpy as np
import math
import socket

UDP_PORT = 5005

MIN_DB = 15
MAX_DB = 65

SAMPLERATE = 48000
WINDOW_SIZE = 960*2
HOP_SIZE = 960


FREQ_RANGES = [
    (   2,    4), # 20   ~ 50    Hz
    (   5,    8), # 50   ~ 100   Hz
    (   9,   17), # 100  ~ 200   Hz
    (  18,   34), # 200  ~ 400   Hz
    (  35,   68), # 400  ~ 800   Hz
    (  69,  102), # 800  ~ 1200  Hz
    ( 103,  136), # 1200 ~ 1600  Hz
    ( 137,  205), # 1600 ~ 2400  Hz
    ( 206,  410), # 2400 ~ 4800  Hz
    ( 411,  819), # 4800 ~ 9600  Hz
    ( 820, 1468)  # 9600 ~ 17200 Hz
]

# Connector at bottom left
#LED_MATRIX_MAP = [
#    [  0,   1,   2,   3,   4,   5,   6,   7,   8,   9,  10,  11,  12,  13,  14,  15,  16,  17,  18],
#    [ 37,  36,  35,  34,  33,  32,  31,  30,  29,  28,  27,  26,  25,  24,  23,  22,  21,  20,  19],
#    [ 38,  39,  40,  41,  42,  43,  44,  45,  46,  47,  48,  49,  50,  51,  52,  53,  54,  55,  56],
#    [ 75,  74,  73,  72,  71,  70,  69,  68,  67,  66,  65,  64,  63,  62,  61,  60,  59,  58,  57],
#    [ 76,  77,  78,  79,  80,  81,  82,  83,  84,  85,  86,  87,  88,  89,  90,  91,  92,  93,  94],
#    [113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101, 100,  99,  98,  97,  96,  95],
#    [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132],
#    [151, 150, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133],
#    [152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170],
#    [189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 173, 172, 171],
#    [190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208],
#]

# Connector at bottom right
LED_MATRIX_MAP = [
    [190, 189, 152, 151, 114, 113,  76,  75,  38,  37,   0],
    [191, 188, 153, 150, 115, 112,  77,  74,  39,  36,   1],
    [192, 187, 154, 149, 116, 111,  78,  73,  40,  35,   2],
    [193, 186, 155, 148, 117, 110,  79,  72,  41,  34,   3],
    [194, 185, 156, 147, 118, 109,  80,  71,  42,  33,   4],
    [195, 184, 157, 146, 119, 108,  81,  70,  43,  32,   5],
    [196, 183, 158, 145, 120, 107,  82,  69,  44,  31,   6],
    [197, 182, 159, 144, 121, 106,  83,  68,  45,  30,   7],
    [198, 181, 160, 143, 122, 105,  84,  67,  46,  29,   8],
    [199, 180, 161, 142, 123, 104,  85,  66,  47,  28,   9],
    [200, 179, 162, 141, 124, 103,  86,  65,  48,  27,  10],
    [201, 178, 163, 140, 125, 102,  87,  64,  49,  26,  11],
    [202, 177, 164, 139, 126, 101,  88,  63,  50,  25,  12],
    [203, 176, 165, 138, 127, 100,  89,  62,  51,  24,  13],
    [204, 175, 166, 137, 128,  99,  90,  61,  52,  23,  14],
    [205, 174, 167, 136, 129,  98,  91,  60,  53,  22,  15],
    [206, 173, 168, 135, 130,  97,  92,  59,  54,  21,  16],
    [207, 172, 169, 134, 131,  96,  93,  58,  55,  20,  17],
    [208, 171, 170, 133, 132,  95,  94,  57,  56,  19,  18]
]

# Rainbow LUT
#RAINBOW_LUT = [
# (12,  0,  0),
# (12,  2,  0),
# (12,  4,  0),
# (12,  6,  0),
# (11,  8,  0),
# (10, 10,  0),
# ( 9, 11,  0),
# ( 7, 12,  0),
# ( 5, 12,  1),
# ( 3, 12,  3),
# ( 1, 12,  6),
# ( 0, 11,  9),
# ( 0,  9, 11),
# ( 0,  6, 12),
# ( 1,  3, 12),
# ( 3,  1, 12),
# ( 6,  0, 11),
# ( 9,  0,  7),
# (12, 12, 12)
#]

RAINBOW_LUT = [
 ( 6, 0, 0),
 ( 6, 1, 0),
 ( 6, 2, 0),
 ( 6, 3, 0),
 ( 5, 4, 0),
 ( 5, 5, 0),
 ( 4, 5, 0),
 ( 3, 6, 0),
 ( 2, 6, 1),
 ( 1, 6, 3),
 ( 0, 6, 3),
 ( 0, 5, 4),
 ( 0, 4, 5),
 ( 0, 3, 6),
 ( 1, 2, 6),
 ( 1, 1, 6),
 ( 3, 0, 6),
 ( 4, 0, 3),
 ( 5, 5, 5)
]

class FFTAccelerator:
    def __init__(self, overlay):
    
        # Retrieve IP information from .hwh file
        self.dma = overlay.axi_dma_0
        
        # Allocate a space in DDR memory for DMA transmit and receive.
        self.dma_tx_buffer = allocate(shape=(4096,), dtype=np.uint32)
        self.dma_rx_buffer = allocate(shape=(4096,), dtype=np.float32)
    
    def execute(self, samples):
        self.dma_tx_buffer[:len(samples)] = samples
        self.dma.recvchannel.transfer(self.dma_rx_buffer)
        self.dma.sendchannel.transfer(self.dma_tx_buffer)
        self.dma.sendchannel.wait()
        self.dma.recvchannel.wait()
        return self.dma_rx_buffer


#class NeoPixel:
#    def __init__(self, base_addr = 0x80000000, mem_size = 1024, num_leds = 1):
#        self.mmio = MMIO(base_addr, mem_size)
#        self.num_leds = max(min(num_leds, 1023), 0)
#        self.base_addr = base_addr
#        self.addr_step = 0x4
#        self.mmio.write(0x0, self.num_leds)
#    
#    def get_led_num(self):
#        return self.num_leds
#        
#    def set_rgb(self, index, r, g, b):
#        if 0 <= index < self.num_leds:
#            r = max(min(r, 255), 0)
#            g = max(min(g, 255), 0)
#            b = max(min(b, 255), 0)
#            color = g << 16 | r << 8 | b
#            self.mmio.write(0x4 + (0x4 * index), color)
#            
#    def set_rgb_all(self, r, g, b):
#        for i in range(self.num_leds):
#            self.set_rgb(i, r, g, b)
#            
#    def close(self):
#        for i in range(self.num_leds):
#            self.set_rgb(i, 0, 0, 0)


class NeoPixel:
    def __init__(self, base_addr=0x80000000, mem_size=1024, num_leds=1):
        self.mmio = MMIO(base_addr, mem_size)
        self.num_leds = max(min(num_leds, 1023), 0)
        self.base_addr = base_addr
        self.addr_step = 0x4
        self.led_state = [(0, 0, 0)] * self.num_leds
        self.mmio.write(0x0, self.num_leds)

    def get_led_num(self):
        return self.num_leds

    def set_rgb(self, index, r, g, b):
        current = self.led_state[index]
        if current != (r, g, b):
            self.led_state[index] = (r, g, b)
            color = g << 16 | r << 8 | b
            self.mmio.write(0x4 + self.addr_step * index, color)

    def set_rgb_all(self, r, g, b):
        for i in range(self.num_leds):
            self.set_rgb(i, r, g, b)

    def close(self):
        self.set_rgb_all(0, 0, 0)

            
class IO:
    def __init__(self, overlay):
    
        # Retrieve IP information from .hwh file
        self.leds = overlay.leds.channel1
        self.btns = overlay.btns.channel1
        self.sws = overlay.sws.channel1
        
    def set_led(self, index, state):
        if index <= 3 and index >= 0:
            if state == 1 or state == 0:
                self.leds.write(state << index, 0b0001 << index)
                
    def set_led_all(self, state):
        if state == 1:
            self.leds.write(0b1111, 0b1111)
        elif state == 0:
            self.leds.write(0b0000, 0b1111)
            
    def get_btn_state(self, index):
        if index <= 3 and index >= 0:
            return (self.btns.read() >> index) & 0b0001
        return -1
        
    def get_sw_state(self, index):
        if index <= 1 and index >= 0:
            return (self.sws.read() >> index) & 0b0001
        return -1

def main():

    # Clear cache
    PL.reset()
    
    # Load bitstream file into SRAM
    print("Loading Bitstream...")
    overlay = Overlay("design_1_wrapper.bit", download=True)
    print("Bitstream Loaded!")

    # Initialize IPs
    fft = FFTAccelerator(overlay)
    io = IO(overlay)
    
    # Initialize and test LED panel
    ws2812 = NeoPixel(num_leds = 209)
    ws2812.set_rgb_all(10, 0, 0)
    time.sleep(0.5)
    ws2812.set_rgb_all(0, 10, 0)
    time.sleep(0.5)
    ws2812.set_rgb_all(0, 0, 10)
    time.sleep(0.5)
    ws2812.close()
    
#    for i in range(ws2812.get_led_num()):
#        ws2812.set_rgb(i, 5, 5, 5)
#        time.sleep(0.01)
#        
#    for i in range(ws2812.get_led_num()):
#        ws2812.set_rgb(i, 0, 0, 0)
#        time.sleep(0.01)
        
    for x in range(11):
        for y in range(19):
            ws2812.set_rgb(LED_MATRIX_MAP[y][x], 5, 5, 5)
            time.sleep(0.005)
            
    for x in range(11):
        for y in range(19):
            ws2812.set_rgb(LED_MATRIX_MAP[y][x], 0, 0, 0)
            time.sleep(0.005)
    
    
    # Initialize UDP server
    print("Initial UDP Server...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", UDP_PORT))
    print(f'Listening on Port {UDP_PORT}...')
    
    loop_count = 0
    start_time = time.time()
    
    alpha = 0.4  
    levels = np.zeros(11, dtype = np.float32)
    levels_smoothed = np.zeros(11, dtype = np.float32)
    normalization = np.zeros(11, dtype = np.float32)    
    
    audio_buffer = deque(maxlen = WINDOW_SIZE)
    window_function = np.hanning(WINDOW_SIZE)
    
    while True:
        data, addr = sock.recvfrom(8192)
        audio_samples = np.frombuffer(data, dtype=np.int16)
        
        audio_buffer.extend(audio_samples)
        if len(audio_buffer) == WINDOW_SIZE:
            fft_result = fft.execute((np.array(audio_buffer) * window_function).astype(np.int16))
            audio_buffer = deque(list(audio_buffer)[HOP_SIZE:], maxlen = WINDOW_SIZE)
        
#            for i, (start, end) in enumerate(FREQ_RANGES):
#                levels[i] = 20 * np.log10(np.max(fft_result[start:end]) + 0.89125093)
#            
#            normalization = np.clip((levels - MIN_DB) / (MAX_DB - MIN_DB), 0.0, 1.0)

            for i, (start, end) in enumerate(FREQ_RANGES):
                levels[i] = 20 * np.log10(np.max(fft_result[start:end]) + 0.89125093)
            
            levels_smoothed = alpha * levels_smoothed + (1 - alpha) * levels
            normalization = np.clip((levels_smoothed - MIN_DB) / (MAX_DB - MIN_DB), 0.0, 1.0)
            
            for x in range(11):
                on_num = int(normalization[x] * 19)
                for y in range(19):
                  if on_num > y:
                    ws2812.set_rgb(LED_MATRIX_MAP[y][x], *RAINBOW_LUT[y])
                  else:
                    ws2812.set_rgb(LED_MATRIX_MAP[y][x], 0, 0, 0)
            
#            if io.get_sw_state(0) == 1:
#            print("  ".join(f"{lv:5.2f}" for lv in levels))
            
            loop_count += 1
            if time.time() - start_time >= 1.0:
                elapsed_time = time.time() - start_time
                print(f'loop count:{loop_count}, cost {elapsed_time / loop_count * 1000} ms')
                loop_count = 0
                start_time = time.time()
        
if __name__ == "__main__":
    main()