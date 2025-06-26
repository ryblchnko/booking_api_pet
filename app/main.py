import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from hawk_python_sdk.modules.fastapi import HawkFastapi
from prometheus_fastapi_instrumentator import Instrumentator
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config import settings
from app.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.logger import logger
from app.pages.router import router as router_pages
from app.users.router import router as router_users


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_rooms)

app.include_router(router_pages)
app.include_router(router_images)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)
app = VersionedFastAPI(app, version_format="{major}", prefix_format="/v{major}")


admin = Admin(app, engine, authentication_backend=authentication_backend)

app.mount("/static", StaticFiles(directory="app/static"), "static")

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


hawk = HawkFastapi(
    {
        "app_instance": app,
        "token": "eyJpbnRlZ3JhdGlvbklkIjoiOTc0ZjIwOGMtOGEyNi00NDhkLTgwZjgtZjg4M2MyOTViYTkyIiwic2VjcmV0IjoiM2M2YTRmNWEtNmU1ZC00M2VhLWEzZTQtODNmMzA4MDhmMjYwIn0=",
    }
)

instrumentator = Instrumentator(
    should_group_status_codes=False, excluded_handlers=[".*admin.*", "/metrics"]
)

instrumentator.instrument(app).expose(app)
