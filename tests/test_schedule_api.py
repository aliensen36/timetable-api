import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_create_schedule() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/v1/schedules",
            json={
                "user_id": "user-1",
                "medicine_name": "Ibuprofen",
                "frequency": 3,
                "treatment_days": 10,
            },
        )

    assert response.status_code == 201
    assert "id" in response.json()
