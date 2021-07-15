import uvicorn
from .settings import settings
from .tables import Base
from .database import engine

uvicorn.run(
    "my_finance.app:app",
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)


Base.metadata.create_all(engine)
