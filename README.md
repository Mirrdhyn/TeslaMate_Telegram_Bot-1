# TeslaMate Telegram Bot

## A propos / Disclamer
Ce fork du projet est fait pour montrer ce qu'on peut faire avec ce bout de code de départ, avec le projet [Tesla MQTT API](https://github.com/tlj/teslamate-mqtt-api) et quelques lignes de codes Python 3.8 pour avoir des informations sur sa Tesla.

Le code partagé dans le dossier src a été retouché dans ce sens, mais présente trop de changement par rapport au dépot initial. C'est pourquoi ce fork, en laissant les liens initiaux (PayPal et autres), tout en partageant mes modifications.

[![latest release](https://img.shields.io/github/v/release/JakobLichterfeld/TeslaMate_Telegram_Bot)](https://github.com/JakobLichterfeld/TeslaMate_Telegram_Bot/releases/latest)
[![](https://images.microbadger.com/badges/version/teslamatetelegrambot/teslamatetelegrambot.svg)](https://hub.docker.com/r/teslamatetelegrambot/teslamatetelegrambot)
[![](https://images.microbadger.com/badges/image/teslamatetelegrambot/teslamatetelegrambot.svg)](https://microbadger.com/images/teslamatetelegrambot/teslamatetelegrambot)
[![donation](https://img.shields.io/badge/Donate-PayPal-informational.svg?logo=paypal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZE9EHN48GYWMN&source=url)

This is a telegram bot written in Python to notify by Telegram message when a new SW update for your Tesla is available. It uses the MQTT topic which [TeslaMate](https://github.com/adriankumpf/teslamate) offers.

## Screenshots

<p align="center">
  <img src="screenshots/teslabot2.png" alt="Telegram Message: SW Update available" title="telegram_message_sw_update" />
</p>

## Table of contents

- [TeslaMate Telegram Bot](#teslamate-telegram-bot)
  - [Screenshots](#screenshots)
  - [Table of contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Update](#update)
  - [Contributing](#contributing)
  - [Donation](#donation)
  - [Disclaimer](#disclaimer)

## Features

- [x] Envoyer un message Telegram quand une mise à jour est disponible
- [x] Envoyer un message Telegram quand un changement d'état se produit
- [x] Envoyer un message Telegram quand une portière s'ouvre
- [x] Envoyer un message Telegram quand une charge démarre ou s'arrête
- [x] Envoyer un message Telegram quand le temps de charge change
- [x] Envoyer la dernière position GPS connue de la voiture lorsqu'elle se verrouille (utile pour retrouver dans un parking plein air par exemple)

## Requirements

- A Machine that's always on and runs [TeslaMate](https://github.com/adriankumpf/teslamate)
- Docker _(if you are new to Docker, see [Installing Docker and Docker Compose](https://dev.to/rohansawant/installing-docker-and-docker-compose-on-the-raspberry-pi-in-5-simple-steps-3mgl))_
- External internet access, to send telegram messages.
- A mobile with [Telegram](https://telegram.org/) client installed
- your own Telegram Bot, see [Creating a new telegram bot](https://core.telegram.org/bots#6-botfather)
- your own Telegram chat id, see [get your telegram chat id](https://docs.influxdata.com/kapacitor/v1.5/event_handlers/telegram/#get-your-telegram-chat-id)

## Installation

Make sure you fulfill the [Requirements](#requirements).

It is recommended to backup your data first.

This document provides the necessary steps for installation of TeslaMate Telegram Bot on a any system that runs Docker.

This setup is recommended only if you are running TeslaMate Telegram Bot **on your home network**, as otherwise your telegram API tokens might be at risk.

1. Create a file called `docker-compose.yml` with the following content (adopt with your own values):

   ```yml title="docker-compose.yml"
      version: "3"

      services:
        teslamatetelegrambot:
          image: teslamatetelegrambot/teslamatetelegrambot:latest
          restart: unless-stopped
          environment:
            - MQTT_BROKER_HOST=IP_Adress
            - MQTT_BROKER_PORT=1883 #optional, default 1883
            - TELEGRAM_BOT_API_KEY=secret_api_key
            - TELEGRAM_BOT_CHAT_ID=secret_chat_id
            - TELSAMATE_MQTT_API_URL=http://127.0.0.1:3040/car/1?api_key=xxxxx #CHANGEME with the MQTT API URL
          ports:
            - 1883
          build:
            context: .
            dockerfile: Dockerfile
   ```

2. Build and start the docker container with `docker-compose up`. To run the containers in the background add the `-d` flag:

   ```bash
   docker-compose build
   docker-compose up -d
   ```

## Update

Check out the [release notes](https://github.com/JakobLichterfeld/TeslaMate_Telegram_Bot/releases) before upgrading!

### Note FR : A faire uniquement si vous n'avez pas de modification apportée au code dans src.

Pull the new images:

```bash
docker-compose pull
```

and restart the stack with `docker-compose up`. To run the containers in the background add the `-d` flag:

```bash
docker-compose up -d
```

## Contributing

All contributions are welcome and greatly appreciated!

## Donation

Maintaining this project isn't effortless, or free. If you would like to kick in and help me cover those costs, that would be awesome. If you don't, no problem; just share your love and show your support.

<p align="center">
  <a href="https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZE9EHN48GYWMN&source=url">
    <img src="screenshots/paypal-donate-button.png" alt="Donate with PayPal" />
  </a>
</p>

## Disclaimer

Please note that the use of the Tesla API in general and this software in particular is not endorsed by Tesla. Use at your own risk.
