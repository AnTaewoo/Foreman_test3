import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    return create_app(str(tmp_path / "t.db")).test_client()


def test_index_serves_frontend(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"url-input" in response.data


def test_shorten_valid_url(client):
    response = client.post(
        "/api/shorten",
        json={"url": "https://example.com/path"},
        base_url="http://example.test",
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["url"] == "https://example.com/path"
    assert len(data["code"]) == 6
    assert data["short_url"] == f"http://example.test/{data['code']}"


def test_shorten_missing_or_invalid_url_returns_400(client):
    missing_response = client.post("/api/shorten", json={})
    invalid_response = client.post(
        "/api/shorten",
        json={"url": "not-a-url"},
    )

    assert missing_response.status_code == 400
    assert missing_response.get_json() == {"error": "invalid url"}
    assert invalid_response.status_code == 400
    assert invalid_response.get_json() == {"error": "invalid url"}


def test_list_and_detail_routes(client):
    shorten_response = client.post(
        "/api/shorten",
        json={"url": "https://example.com"},
    )
    code = shorten_response.get_json()["code"]

    list_response = client.get("/api/links")
    detail_response = client.get(f"/api/links/{code}")

    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert detail_response.get_json() == {
        "code": code,
        "url": "https://example.com",
        "clicks": 0,
    }


def test_missing_detail_returns_404(client):
    response = client.get("/api/links/missing")

    assert response.status_code == 404
    assert response.get_json() == {"error": "not found"}


def test_redirect_increments_clicks(client):
    shorten_response = client.post(
        "/api/shorten",
        json={"url": "https://example.com/target"},
    )
    data = shorten_response.get_json()
    code = data["code"]

    redirect_response = client.get(f"/{code}")
    detail_response = client.get(f"/api/links/{code}")

    assert redirect_response.status_code == 302
    assert redirect_response.headers["Location"] == "https://example.com/target"
    assert detail_response.get_json()["clicks"] == 1


def test_missing_redirect_returns_404(client):
    response = client.get("/missing")

    assert response.status_code == 404
    assert response.get_json() == {"error": "not found"}
