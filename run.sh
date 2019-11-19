#!/bin/bash
#○source /home/mrmed/Desktop/test/venv/bin/activate
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
export YTS_KEY=7gvd57ugllfjic5c577ec57rep
/home/mrmed/Desktop/test/venv/bin/python3 start.py --debug false --sleep 900 --notif 10800
#/home/mrmed/Desktop/test/venv/bin/python3 start.py --debug true --sleep 5
