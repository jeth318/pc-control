#!/bin/sh
branch=$(git branch --show-current)
destination="jeth@10.0.128.110:/home/jeth/apps/pc-control"

if [[ $branch == "main" ]]; then
    echo "On main branch. Will build and ship to server"
    echo "Shipping dist to server"
    rsync -arvz -e 'ssh -p 2244' --progress $(pwd)/server.py $destination
else
    echo "Not on main branch. Skipping build and deploy."
fi