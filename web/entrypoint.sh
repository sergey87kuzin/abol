#!/bin/bash
# // Миграции
sleep 10
alembic upgrade heads

python main.py
