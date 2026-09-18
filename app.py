from flask import Flask, current_app, jsonify, redirect, request, send_from_directory

from shortcode import generate_code, is_valid_url
from storage import LinkStorage


def create_app(db_path: str = "links.db") -> Flask:
    app = Flask(__name__, static_folder="static")
    app.config["STORAGE"] = LinkStorage(db_path)

    @app.get("/")
    def index():
        return send_from_directory(current_app.static_folder, "index.html")

    @app.post("/api/shorten")
    def shorten():
        data = request.get_json(silent=True)
        url = data.get("url") if isinstance(data, dict) else None

        if not isinstance(url, str) or not is_valid_url(url):
            return jsonify({"error": "invalid url"}), 400

        storage = current_app.config["STORAGE"]
        while True:
            code = generate_code()
            try:
                storage.save(code, url)
                break
            except KeyError:
                continue

        return jsonify(
            {
                "code": code,
                "short_url": request.host_url + code,
                "url": url,
            }
        ), 201

    @app.get("/api/links")
    def list_links():
        return jsonify(current_app.config["STORAGE"].list_all())

    @app.get("/api/links/<code>")
    def link_detail(code):
        link = current_app.config["STORAGE"].get(code)
        if link is None:
            return jsonify({"error": "not found"}), 404
        return jsonify(link)

    @app.get("/<code>")
    def redirect_to_link(code):
        storage = current_app.config["STORAGE"]
        link = storage.get(code)
        if link is None:
            return jsonify({"error": "not found"}), 404

        storage.increment_clicks(code)
        return redirect(link["url"])

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
