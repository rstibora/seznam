#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username=postgres<<-EOSQL
     CREATE DATABASE seznam;
     CREATE USER seznam WITH PASSWORD '${SEZNAM_DB_PASSWORD}';
     GRANT ALL PRIVILEGES ON DATABASE seznam TO seznam;
     ALTER USER seznam CREATEDB;
EOSQL
