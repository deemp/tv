# Lab 5

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
