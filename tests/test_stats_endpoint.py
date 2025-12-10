import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_stats_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/stats")
        assert response.status_code == 200
        data = response.json()

        assert "last_run_status" in data
        assert "last_run_records" in data
        assert "last_run_duration_ms" in data
        assert "last_success" in data
        assert "last_failure" in data
