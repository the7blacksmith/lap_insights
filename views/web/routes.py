from flask import Blueprint, render_template, request, current_app, send_file
from scripts.data import Henakart
from werkzeug.utils import secure_filename
import os, json

web = Blueprint("web", __name__)

@web.route("/")
def t_home():
    return render_template("index.html")

@web.route('/download')
def download():
    file_path= "staticFiles/test.csv"
    return send_file(file_path, as_attachment=True)



@web.route('/race', methods=['GET', 'POST'])
def plot_race():
    upload_folder = current_app.config['UPLOAD_FOLDER']
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    if file:
        save_file = os.path.join(upload_folder, secure_filename(file.filename))
        file.save(save_file)
        with open (save_file, "r", encoding = "utf-8") as file:
            data = file.readlines()
        data = Henakart(data)
        variables = json.dumps(list(data.variables))
        race = json.dumps(list(data.all_vars.values()))
        laps = json.dumps(data.laps_base)
        mean_drivers = []
        for md in data.mean_per_driver().values():
            for mt in md:
                mean_drivers.append(mt)
        mean_drivers = json.dumps(mean_drivers)
        drivers = json.dumps(list(data.mean_per_driver().keys()))
        best_drivers = []
        for bd in data.best_lap_driver().values():
            for bt in bd:
                best_drivers.append(bt)
        best_drivers = json.dumps(best_drivers)
        best_l = data.best_lap_absolute[0]
        mean_l = data.absolute_mean[0]
        best_lap = []
        mean_lap = []
        for bml in range(len(data.drivers)):
            best_lap.append(best_l)
            mean_lap.append(mean_l)

        
        return render_template("race.html", variables = variables, race = race, laps = laps, drivers = drivers, mean_drivers = mean_drivers, best_drivers = best_drivers, best_lap = best_lap, mean_lap = mean_lap)
