#!/usr/bin/env bash

# Helper script to start MariaDB, Backend API, and Frontend dev server together

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOCKET_PATH="/home/hp/mysql_data/mysql.sock"
DATADIR="/home/hp/mysql_data"

echo "=========================================================="
echo " Starting Social Media DBMS Project (Full Stack)"
echo "=========================================================="

# 1. Start MariaDB if not already running
if ! mariadb-admin ping --socket="$SOCKET_PATH" --silent 2>/dev/null; then
  echo "[1/3] Starting MariaDB server..."
  mariadbd --datadir="$DATADIR" --socket="$SOCKET_PATH" --port=3306 &
  MARIADB_PID=$!
  sleep 2
else
  echo "[1/3] MariaDB is already running on socket $SOCKET_PATH."
fi

# 2. Start Backend API
echo "[2/3] Starting Backend Express API on port 3000..."
cd "$PROJECT_ROOT/backend"
npm start &
BACKEND_PID=$!
sleep 1

# 3. Start Frontend
echo "[3/3] Starting Frontend React (Vite) on port 5173..."
cd "$PROJECT_ROOT/frontend"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo " Project is LIVE!"
echo " Frontend:  http://localhost:5173"
echo " Backend:   http://localhost:3000"
echo " MariaDB:   Port 3306 (Socket: $SOCKET_PATH)"
echo " Press Ctrl+C in this terminal to stop all services."
echo "=========================================================="

trap 'echo ""; echo "Shutting down services..."; kill $FRONTEND_PID $BACKEND_PID 2>/dev/null; wait $FRONTEND_PID $BACKEND_PID 2>/dev/null; echo "Done."; exit' INT TERM

wait
