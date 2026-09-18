from pathlib import Path


def test_index_contains_required_controls_and_script():
    content = (Path(__file__).parent / "static" / "index.html").read_text()

    for required_text in (
        "url-input",
        "shorten-btn",
        "result",
        "error",
        "links-table",
        "/static/app.js",
    ):
        assert required_text in content


def test_app_uses_required_fetch_endpoints():
    content = (Path(__file__).parent / "static" / "app.js").read_text()

    for required_text in (
        "/api/shorten",
        "/api/links",
        "fetch",
        "short_url",
    ):
        assert required_text in content
