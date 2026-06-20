try:
    from flask import Flask, abort, send_from_directory
except ImportError:
    print("No tienes Flask instalado. Ejecuta: pip3 install flask")
    raise SystemExit(1)

import os

static_file_dir = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_folder=static_file_dir)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0  # Desactiva cache durante desarrollo.


@app.route("/", methods=["GET"])
def serve_catalog():
    catalog_path = os.path.join(static_file_dir, "catalog.html")
    if not os.path.isfile(catalog_path):
        abort(404, description="No se encontró catalog.html")
    return send_from_directory(static_file_dir, "catalog.html")


@app.route("/<path:path>", methods=["GET"])
def serve_static(path):
    requested_path = os.path.join(static_file_dir, path)

    if os.path.isdir(requested_path):
        index_path = os.path.join(requested_path, "index.html")
        if os.path.isfile(index_path):
            path = os.path.join(path, "index.html")
        else:
            abort(404)
    elif not os.path.isfile(requested_path):
        abort(404)

    response = send_from_directory(static_file_dir, path)
    response.cache_control.max_age = 0
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
