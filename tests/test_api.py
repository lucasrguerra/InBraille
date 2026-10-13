import time

import pytest
from fastapi.testclient import TestClient

from src.web.app import create_app


@pytest.fixture()
def client():
    return TestClient(create_app())


def test_home_has_security_headers(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"


def test_google_verification_file(client):
    response = client.get("/google21a790a2c23c0ec5.html")
    assert response.status_code == 200
    assert response.text.startswith("google-site-verification:")


def test_docs_are_disabled(client):
    for path in ("/docs", "/redoc", "/openapi.json"):
        assert client.get(path).status_code == 404


@pytest.mark.parametrize("path", [
    "/public/../.env",
    "/public/%2e%2e/.env",
    "/public/..%2f.env",
    "/public/%2e%2e%2fmain.py",
    "/public/..%2fsrc%2fconfig.py",
    "/public//etc/passwd",
])
def test_static_path_traversal_is_blocked(client, path):
    response = client.get(path)
    assert response.status_code == 404
    assert "PORT" not in response.text and "root:" not in response.text


def test_static_serves_assets(client):
    assert client.get("/public/style.css").headers["content-type"].startswith("text/css")
    assert client.get("/public/index.js").headers["content-type"].startswith("text/javascript")


@pytest.mark.parametrize("alphabet", ["Brazilian", "North American", "Chinese"])
def test_encode_decode_roundtrip_runs(client, alphabet):
    text = "ni3 hao3" if alphabet == "Chinese" else "hello"
    encoded = client.post("/api/encode", json={"text": text, "alphabet": alphabet})
    assert encoded.status_code == 200
    braille = encoded.json()["encoded"]
    assert braille
    decoded = client.post("/api/decode", json={"braille": braille, "alphabet": alphabet})
    assert decoded.status_code == 200


def test_unknown_alphabet_rejected(client):
    assert client.post("/api/encode", json={"text": "a", "alphabet": "Klingon"}).status_code == 422


def test_oversized_text_rejected(client):
    assert client.post("/api/encode", json={"text": "a" * 5001}).status_code == 422


def test_oversized_body_rejected(client):
    assert client.post("/api/encode", content=b"x" * (70 * 1024)).status_code == 413


def test_stl_generation(client):
    response = client.post("/api/to-stl", json={"braille": "⠓⠑⠇⠇⠕", "resolution": 15})
    assert response.status_code == 200
    assert len(response.content) > 1000
    assert response.headers["content-disposition"] == "attachment; filename=output.stl"


@pytest.mark.parametrize("payload", [
    {"braille": "hello"},
    {"braille": ""},
    {"braille": "⠁" * 3001},
    {"braille": "⠁" * 201},
    {"braille": "\n".join(["⠁"] * 101)},
    {"braille": "⠁", "text_alignment": "../../etc"},
    {"braille": "⠁", "resolution": 10**9},
    {"braille": "⠁", "plate_thickness": -5},
])
def test_stl_invalid_input_rejected(client, payload):
    assert client.post("/api/to-stl", json=payload).status_code == 422


def test_stl_cost_budget_rejects_expensive_models(client):
    braille = "\n".join(["⠿" * 29] * 10)
    response = client.post("/api/to-stl", json={"braille": braille, "resolution": 50})
    assert response.status_code == 422
    assert "model too large" in response.text


def test_stl_worst_case_within_budget_is_bounded(client):
    braille = "\n".join(["⠿" * 12] * 5)  # 60 filled cells x resolution 50 = budget
    start = time.monotonic()
    response = client.post("/api/to-stl", json={"braille": braille, "resolution": 50})
    assert response.status_code == 200
    assert time.monotonic() - start < 30


def test_errors_do_not_leak_internals(client, monkeypatch):
    from src.translation import translator

    def boom(*_):
        raise RuntimeError("secret /app/internal/path")

    monkeypatch.setattr(translator, "encode", boom)
    response = client.post("/api/encode", json={"text": "a"})
    assert response.status_code == 500
    assert "secret" not in response.text


def test_rate_limit_kicks_in(client):
    codes = [client.post("/api/to-stl", json={"braille": "⠁", "resolution": 15}).status_code for _ in range(13)]
    assert 429 in codes
