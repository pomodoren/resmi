#/bin/sh
cp .env.example .env
docker-compose up -d geores-db

cd georesilience
. venv/bin/activate
sleep 2
flask fab create-admin --username admin --password admin --firstname admin --lastname admin --email admin
sleep 2
python3 utils/seeder_settings.py
sleep 3
python3 utils/seeder_osm.py
python3 utils/seeder_gtfs.py
sleep 2
python3 run.py
