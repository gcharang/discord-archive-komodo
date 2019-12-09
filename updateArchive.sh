#!/bin/bash

cat << EOF > config.json
{
  "token": $DISCORD_TOKEN,
  "serverId": "412898016371015680"
}

EOF

until ./main.py
do
    echo "..."
    sleep 1
done
