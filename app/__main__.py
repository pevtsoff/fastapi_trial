import uvicorn
from .settings import settings
from .tables import Base
from .database import engine

uvicorn.run(
    "app.app:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)

# https://stackoverflow.com/questions/68230481/sqlalchemy-attributeerror-asyncengine-object-has-no-attribute-run-ddl-visit

Base.metadata.create_all(engine)
