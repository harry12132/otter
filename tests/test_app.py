from pathlib import Path

from fastapi.testclient import TestClient

from main import app


def test_requirements_file_exists():
    assert Path("requirements.txt").exists()


def test_home_endpoint():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_inspect_endpoint_handles_empty_or_non_c2pa_upload():
    client = TestClient(app)
    response = client.post(
        "/inspect",
        files={"file": ("sample.jpg", b"not-a-real-image", "image/jpeg")},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["filename"] == "sample.jpg"
    assert payload["has_c2pa_manifest"] is False
    assert payload["is_ai"] is False
    assert payload["otter_verdict"] == (
        "🟡 No C2PA Manifest Found\n"
        "Metadata was stripped or the file is unsigned. Stand by for Tier 2 pixel forensics."
    )
