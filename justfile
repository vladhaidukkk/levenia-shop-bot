compose_file := "docker-compose-local.yaml"

up:
    docker compose -f {{compose_file}} up -d

down:
    docker compose -f {{compose_file}} down
