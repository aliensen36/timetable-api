from fastapi import FastAPI

app = FastAPI(
    title="Timetable API",
    version="0.1.0",
)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
