from fastapi import FastAPI
from .router import SecuriseMiddleware, router as _home
from .router.dashboard import router as dashboard_router
from .router.download import router as download_router, \
  DownloadMiddleware
from .router.action import router as action_router

app= FastAPI()
app.add_middleware(SecuriseMiddleware)
app.add_middleware(DownloadMiddleware)

app.include_router(_home)
app.include_router(dashboard_router)
app.include_router(download_router)
app.include_router(action_router)

