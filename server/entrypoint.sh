#!/bin/sh


echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

echo "Waiting for mongodb..."

while ! nc -z $MONGO_DB_HOST $MONGO_DB_PORT; do
  sleep 0.1
done

echo "MongDB started"


#python manage.py flush --no-input
#python manage.py migrate

exec "$@"
echo "Starting front"
cd front
npm run serve