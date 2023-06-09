# Model-Controller-Sensor backend

[![Build Docker image and push to GHCR](https://github.com/ntdesmond/MCS-backend-test/actions/workflows/build-push-docker.yml/badge.svg)](https://github.com/ntdesmond/MCS-backend-test/actions/workflows/build-push-docker.yml)

## How to

1. Obtain a copy of [.env.docker](./.env.docker) and [docker-compose.yml](./docker-compose.yml) files (or just clone the repository)
2. The compose is already configured to run 8 sensors, 1 controller and 1 manipulator.

   To start them, run `docker compose --env-file .env.docker up -d`.

   After the services are started, interactive HTTP API docs will be available at <http://localhost:8000/docs>.

   Manipulator logs can be checked by running `docker logs mcs-manipulator-1`.
3. Use `docker compose --env-file .env.docker down` to stop the containers.

## HTTP API reference
- `GET /signals` — get a list of signals, where consecutive signals with the same status are merged into a common time interval.
- `POST /messages` — submit a message from a sensor.

## Sensor payload and status computation

- `payload` field of the sensor message is a number drawn randomly from range [-10, 10].
- Each 5 seconds the controller computes the average among received payloads.
- `"up"` or `"down"` status is logged and the control signal is sent to the manipulator over server-to-client TCP socket.
  The status is determined by whether the computed average is a positive number.
- After the status is sent, the received payload buffer is cleared, so that older data does not affect next status changes.