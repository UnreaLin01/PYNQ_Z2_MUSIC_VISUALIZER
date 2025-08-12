# PYNQ-Z2 Music Visualizer 🎵💡

![image](https://hackmd.io/_uploads/HkCAJ2p4xe.jpg)

[![image](https://hackmd.io/_uploads/r1zlpLduee.jpg)](https://www.youtube.com/watch?v=f9keKouVoJM)

An FPGA-based real-time audio spectrum visualizer built on the PYNQ-Z2 development board. The system utilizes programmable logic (PL) for FFT acceleration and WS2812B addressable RGB LED driving, while the processor system (PS) handles audio streaming over Ethernet and generates dynamic LED panel patterns.

## ✨ Features

- Learn Zynq-7000 FPGA development through a hands-on project
- Fully leverage the strengths of both the PL and PS for optimal performance
- Deliver eye-catching, vivid, and smooth audio-reactive visuals
- Stream audio in real time over Ethernet with minimal latency
- Hardware-accelerated FFT with integrated magnitude calculation

## 📌 System Diagram

![image](https://hackmd.io/_uploads/S1HlYjPzeg.png)

## 📽️ Demo Video
* [PYNQ-Z2 Music Visualizer - YOASOBI「Watch Me!」](https://youtu.be/f9keKouVoJM)
* [PYNQ-Z2 Music Visualizer - VALORANT x Madge「2WORLDS」](https://youtu.be/hBvHBqEr2Rw)
* [PYNQ-Z2 Music Visualizer - cute girls doing cute things「Surprise」](https://youtu.be/C2-kPhmhrjE)
* [PYNQ-Z2 Music Visualizer - Frequency Sweep 20Hz - 20KHz](https://youtu.be/82kyBqZx_8Q)

## 🛠️ Minimum Requirements

### Hardware

* PYNQ-Z2 — **1 pc**
* Micro SD Card — **1 pc**
* Micro USB Cable — **1 pc**
* Ethernet Cable — **1 pc**
* WS2812B Addressable RGB LED Strip (144 LEDs / meter) — **2 meters**
* TXS0108E Level Shifter Module — **1 pc**
* Hook-Up Wire — **some**

### Software

* BalenaEtcher
* MobaXterm
* Python
* Virtual Cable

## 📄 Full Documentation & Tutorial

* [HackMD Article](https://hackmd.io/@UnreaLin/H11WDXEfee)

## 📎References

* [PYNQ Official Document](https://pynq.readthedocs.io/en/latest/)
* [PYNQ Controlled NeoPixel LED Cube](https://www.hackster.io/adam-taylor/pynq-controlled-neopixel-led-cube-92a1c1)
* [FFT IP Core Tutorial Part 1: Vivado Simulation with Complex Numbers](https://www.youtube.com/watch?v=ZdCnJutIMp8)
* [FFT IP Core Tutorial Part 2: FPGA FFT Acceleration using AXI DMA](https://www.youtube.com/watch?v=HR4h_T4HZB0)

## 🙏 Acknowledgements

- [Adam Taylor](https://www.hackster.io/adam-taylor) — Original NeoPixel IP design
- [FPGAPS](https://www.youtube.com/@FPGAPS) — Excellent FFT IP tutorials