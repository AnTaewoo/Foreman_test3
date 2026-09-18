# Flask URL Shortener

## Run

Start the application from the repository root:

```bash
python app.py
```

Open `http://127.0.0.1:5000` in a browser.

## API

Create a short link with `POST /api/shorten`:

```bash
curl -X POST http://127.0.0.1:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

The JSON response contains the original URL and the generated short-link `code` and `short_url`. Use the returned code or URL when following the link.

List created links with `GET /api/links`:

```bash
curl http://127.0.0.1:5000/api/links
```

The response is a JSON list of links, including their codes, short URLs, and destination URLs.

Follow a returned short link by replacing the placeholder with the `code` returned by `POST /api/shorten`:

```bash
curl -L http://127.0.0.1:5000/REPLACE_WITH_RETURNED_CODE
```

The short-link request redirects to the original URL.

## Test

```bash
pytest -q
```
