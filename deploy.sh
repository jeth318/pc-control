#!/bin/sh
branch=$(git branch --show-current)
destination="jeth@elara.local:~/apps/pc-control"

if [[ $branch == "main" ]]; then
    echo "On main branch. Will ship to server"
    echo "Shipping dist to server"
    rsync -arvz -e 'ssh -p 2244' --progress $(pwd)/server.py $destination
else
    echo "Not on main branch. Skipping  deploy."
fi