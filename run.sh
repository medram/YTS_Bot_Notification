#!/bin/bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
#export YTS_KEY=155oavt64v7jii7nmf46hnkcp8
venv/bin/python3 start.py --debug false --notif 10800
#venv/bin/python3 start.py --debug false --sleep 900 --notif 10800
#venv/bin/python3 start.py --debug true --sleep 5
