import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location, date_from, date_to, status_code",
    [
        ("Алтай", "2025-10-15", "2025-10-10", 400),
        ("Алтай", "2025-10-10", "2025-10-10", 400),
        ("Алтай", "2025-10-10", "2025-10-15", 200),
    ],
)
async def test_get_hotels_by_location_and_time(
    location, date_from, date_to, status_code, ac: AsyncClient
):
    response = await ac.get(
        url=f"/hotels/{location}",
        params={"date_from": date_from, "date_to": date_to},
    )

    assert response.status_code == status_code
