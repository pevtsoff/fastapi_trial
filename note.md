# Running migrations:
 docker-compose run app alembic revision --autogenerate -m "First migration" [--sql]
 
 docker-compose run app alembic downgrade -1 