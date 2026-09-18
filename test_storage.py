import pytest

from storage import LinkStorage


def test_save_and_get_persists_link(tmp_path):
    storage = LinkStorage(str(tmp_path / "links.db"))

    storage.save("abc", "https://example.com")

    assert storage.get("abc") == {
        "code": "abc",
        "url": "https://example.com",
        "clicks": 0,
    }


def test_duplicate_code_raises_key_error(tmp_path):
    storage = LinkStorage(str(tmp_path / "links.db"))
    storage.save("abc", "https://example.com")

    with pytest.raises(KeyError):
        storage.save("abc", "https://example.org")


def test_get_missing_returns_none(tmp_path):
    storage = LinkStorage(str(tmp_path / "links.db"))

    assert storage.get("missing") is None


def test_increment_clicks(tmp_path):
    storage = LinkStorage(str(tmp_path / "links.db"))
    storage.save("abc", "https://example.com")

    assert storage.get("abc")["clicks"] == 0

    storage.increment_clicks("abc")
    assert storage.get("abc")["clicks"] == 1

    storage.increment_clicks("abc")
    assert storage.get("abc")["clicks"] == 2


def test_list_all_orders_by_code(tmp_path):
    storage = LinkStorage(str(tmp_path / "links.db"))
    storage.save("c", "https://c.example.com")
    storage.save("a", "https://a.example.com")
    storage.save("b", "https://b.example.com")

    assert storage.list_all() == [
        {"code": "a", "url": "https://a.example.com", "clicks": 0},
        {"code": "b", "url": "https://b.example.com", "clicks": 0},
        {"code": "c", "url": "https://c.example.com", "clicks": 0},
    ]
