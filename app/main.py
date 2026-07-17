from fastapi import FastAPI

from app.api import schedules_router

app = FastAPI(
    title="Timetable API",
    version="0.1.0",
)


app.include_router(
    schedules_router,
    prefix="/api/v1",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
