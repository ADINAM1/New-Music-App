import os
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    Response,
)

from formatting import format_sql

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")
MAX_UPLOAD_SIZE = 1 * 1024 * 1024  # 1MB
ALLOWED_EXTENSIONS = {".sql"}


def _read_uploaded_file(file_storage):
    filename = file_storage.filename
    _, ext = os.path.splitext(filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Only .sql files are allowed")
    data = file_storage.read()
    if len(data) > MAX_UPLOAD_SIZE:
        raise ValueError("File too large")
    return data.decode("utf-8")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/format", methods=["POST"])
def format_route():
    keyword_case = request.form.get("keyword_case", "upper")
    text = request.form.get("sql_text", "")
    file = request.files.get("sql_file")

    if file and file.filename:
        try:
            text = _read_uploaded_file(file)
        except Exception as exc:  # pragma: no cover - defensive
            flash(str(exc))
            return redirect(url_for("index"))

    text = text.strip()
    if not text:
        flash("Please provide SQL text or upload a .sql file.")
        return redirect(url_for("index"))

    try:
        formatted = format_sql(text, keyword_case)
    except Exception:  # pragma: no cover - sqlparse rarely fails
        flash("Failed to parse SQL.")
        return redirect(url_for("index"))

    session["formatted_sql"] = formatted
    return render_template("result.html", formatted_sql=formatted)


@app.route("/download")
def download():
    formatted = session.get("formatted_sql")
    if formatted is None:
        flash("No formatted SQL available.")
        return redirect(url_for("index"))
    return Response(
        formatted,
        mimetype="text/plain",
        headers={"Content-Disposition": "attachment; filename=formatted.sql"},
    )


if __name__ == "__main__":  # pragma: no cover
    app.run(debug=True)
