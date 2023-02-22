#!/bin/bash

set -e

exec python classifier.py &
exec python bot.py 
