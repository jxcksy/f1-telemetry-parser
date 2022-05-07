# F1 2021 Telemetry Parser 🏎 

![F1 2021 Redbull](img/rb.jpeg)

### Python UDP Client & Telemetry Parser for the F12021 game by Codemasters.

The UDP Specification (Packet Decoding) by Codemasters used for this project can be found [here.](https://forums.codemasters.com/topic/80231-f1-2021-udp-specification/?do=findComment&comment=624274)

## Overview

The F1 series of games support the outputting of key game data via UDP, allowing developers to receive, decode and make use of this data for many different applications (Dashboards, HUD Displays, Performance Analysis etc.)

This project was designed with the intention of becoming a solid 'base' project that will allow anyone to easily stem from or build on, which is why I chose to use Python. 

For optimisation purposes, I hope to develop a C/C++ version of this project at some point in the future.

## Usage

**1. Enable UDP Telemetry on F12021:**

- **Game Options -> Settings -> Telemetry Settings**

![Telemetry Settings](img/telemetry-settings.png)






