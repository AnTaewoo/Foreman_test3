from shortcode import generate_code, is_valid_url


def test_generate_code_default_length_and_alphabet():
    result = generate_code()
    assert len(result) == 6
    assert all(character.isalnum() for character in result)


def test_generate_code_custom_length():
    assert len(generate_code(12)) == 12


def test_is_valid_url_accepts_http_and_https():
    assert is_valid_url("http://example.com")
    assert is_valid_url("https://example.com/path")


def test_is_valid_url_rejects_invalid_schemes():
    assert not is_valid_url("ftp://example.com")
    assert not is_valid_url("example.com")
    assert not is_valid_url("://missing-scheme")


def test_is_valid_url_rejects_missing_host():
    assert not is_valid_url("http://")
    assert not is_valid_url("https:///path")
