from pathlib import Path


def test_readme_documents_run_api_and_test_commands():
    readme = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

    assert "## Run" in readme
    assert "## API" in readme
    assert "## Test" in readme
    assert "python app.py" in readme
    assert "pytest -q" in readme
    assert "http://127.0.0.1:5000" in readme
    assert "curl" in readme
    assert "/api/shorten" in readme
    assert "/api/links" in readme
    assert "curl -L http://127.0.0.1:5000/REPLACE_WITH_RETURNED_CODE" in readme
