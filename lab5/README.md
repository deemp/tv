# Lab 5

## Prerequisites

- `VirtualBox` installed
- [Install Nix](https://github.com/deemp/flakes/blob/main/README/NixPrerequisites.md#install-nix)

## Commands

1. Enter directory

```sh
git clone https://github.com/deemp/tv
cd tv/lab5
nix develop
cd src
```

1. Start using `docker`

```sh
docker compose up
```

1. Try with `kubectl`

```sh
cd k8s
kubectl apply -f deploy.yaml,secrets.yaml,service.yaml,stateful-set.yaml
kubectl get po
```

## References

- PostgreSQL in Docker - [src](https://towardsdatascience.com/how-to-run-postgresql-and-pgadmin-using-docker-3a6a8ae918b5)
- Check PostgreSQL is running - [SO](https://stackoverflow.com/a/48648959)
- Docker volumes - [src](https://github.com/docker-library/rabbitmq/issues/530#issuecomment-1012985283)
  - To avoid access permission problems
- Recreate volumes - [SO](https://stackoverflow.com/a/67971684)
  - To re-initialize a DB
- A `Python` single-element tuple should have a comma like in `(a,)`
  - This is necessary when passing records via `psycopg2` - [src](https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries)
  - It's safer to use lists
