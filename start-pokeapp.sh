#!/bin/bash

# Wait for Postgres to become ready
until nc -z -v -w30 postgres 5432; do
 echo 'Waiting for Postgres...'
 sleep 1
done

# Wait for Redis to become ready
until nc -z -v -w30 redis 6379; do
 echo 'Waiting for Redis...'
 sleep 1
done

# Start your Flask app
flask run --host=0.0.0.0
