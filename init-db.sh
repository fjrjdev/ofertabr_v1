#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    SELECT 'CREATE DATABASE n8n_db'
    WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'n8n_db')\gexec
EOSQL

echo "Database n8n_db created successfully!"