# DonkeyCar Documentation

This document will guide you in installing the necessary software on your pc in order to train a model for the car and help you drive your car and collect data for training.

## Time constraints

Training a ML model for the car requires a lot of resources, so we recommend that you find out who in your team has the most powerful pc, and install the software for training on that pc.

While the software is being installed, you can take your car for a ride on the track, so that you get acquainted with it and with driving it with the controller. Once you are ready, you can begin to collect data for training.

## 1. Install software on host pc (the powerful pc)

### 1.1 Docker

To install docker, follow the instruction from https://docs.docker.com/get-docker/

### 1.2 Environment

To setup and get started follow the following steps:

- git clone https://github.com/trifork/donkeycar-quickstart
- cd donkeycar-quickstart
- docker image build -t donkey_train_web_api .
- docker run -p 5000:5000 -d donkey_train_web_api

Nu kører en hjemmeside lokalt på din computer. 

