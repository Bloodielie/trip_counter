#!/bin/bash

sleep 1;
echo "start migrate";
alembic upgrade head;

sleep 1;

exec python -m bot
