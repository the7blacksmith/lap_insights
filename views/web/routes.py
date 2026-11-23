import json

from flask import Blueprint, render_template, request, send_file

from scripts.data import Henakart

web = Blueprint("web", __name__)

MAX_CSV_BYTES = 5 * 1024 * 1024


@web.route("/")
def t_home():
    return render_template("index.html")


@web.route("/download")
def download():
    return send_file("staticFiles/test.csv", as_attachment=True)


@web.route("/race", methods=["GET", "POST"])
def plot_race():
    file = request.files.get("file")
    if file is None or not file.filename:
        return "No file selected.", 400

    raw_csv = file.read(MAX_CSV_BYTES + 1)
    if len(raw_csv) > MAX_CSV_BYTES:
        return "CSV is too large. Maximum file size is 5 MiB.", 413

    try:
        lines = raw_csv.decode("utf-8-sig").splitlines(keepends=True)
    except UnicodeDecodeError:
        return "Please upload a UTF-8 CSV file.", 400

    data = Henakart(lines)
    driver_means = data.mean_per_driver()
    driver_bests = data.best_lap_driver()
    driver_count = len(data.drivers)

    return render_template(
        "race.html",
        variables=json.dumps(list(data.variables)),
        race=json.dumps(list(data.all_vars.values())),
        laps=json.dumps(data.laps_base),
        drivers=json.dumps(list(driver_means.keys())),
        mean_drivers=json.dumps(
            [mean for means in driver_means.values() for mean in means]
        ),
        best_drivers=json.dumps(
            [best for bests in driver_bests.values() for best in bests]
        ),
        best_lap=[data.best_lap_absolute[0]] * driver_count,
        mean_lap=[data.absolute_mean[0]] * driver_count,
    )
