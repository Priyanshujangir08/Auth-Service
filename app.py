from fastapi import FastAPI
from routers.user_routers import user_router
from routers.stats_routers import stats_router
from core.database import engine, Base

# Initialize Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Auth Service",
    docs_url="/",
    openapi_tags=[
        {"name": "User", "description":"User related operations"},
        {"name": "Stats","description": "Provides statistics for the user."}
    ]
)

# Register Routers
app.include_router(user_router, prefix="/user",tags=["User"])
app.include_router(stats_router, prefix="/stats",tags=["Stats"])
