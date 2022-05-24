#!/usr/bin/env bash


python3 -m pip install ara

export ANSIBLE_CALLBACK_PLUGINS="$(python3 -m ara.setup.callback_plugins)"
export ARA_API_SERVER="http://127.0.0.1:8000"
export ARA_API_CLIENT="http"

ara_server_path="$(pwd)/ara/server"
if [[ ! -e "$ara_server_path" ]]; then
  mkdir -p ara/server
fi

docker run --name api-server \
           --detach \
           --tty \
           --volume "$ara_server_path:/opt/ara:z" \
           -p 8000:8000 \
           docker.io/recordsansible/ara-api:latest

exit 0
