#!/bin/bash

# Simple script to test the Social Media API endpoints

BASE_URL="http://localhost:3000"

echo "=== 1. Registering Users ==="
curl -X POST $BASE_URL/register -H "Content-Type: application/json" -d '{"username":"alice", "email":"alice@example.com", "password":"password123", "bio":"Hello world"}'
echo -e "\n"
curl -X POST $BASE_URL/register -H "Content-Type: application/json" -d '{"username":"bob", "email":"bob@example.com", "password":"password123", "bio":"Bob here"}'
echo -e "\n"

echo "=== 2. Creating a Post (as Alice, ID=1) ==="
curl -X POST $BASE_URL/posts -H "Content-Type: application/json" -H "x-user-id: 1" -d '{"content":"My first post!"}'
echo -e "\n"

echo "=== 3. Following Alice (as Bob, ID=2) ==="
curl -X POST $BASE_URL/users/1/follow -H "x-user-id: 2"
echo -e "\n"

echo "=== 4. Liking Alice's Post (as Bob, ID=2) ==="
curl -X POST $BASE_URL/posts/1/like -H "x-user-id: 2"
echo -e "\n"

echo "=== 5. Getting Bob's Feed ==="
curl -X GET $BASE_URL/feed -H "x-user-id: 2"
echo -e "\n"

echo "=== 6. Checking Alice's Notifications ==="
curl -X GET $BASE_URL/notifications -H "x-user-id: 1"
echo -e "\n"

echo "Testing completed."
