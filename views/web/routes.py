from flask import Blueprint, render_template, request
import json
from scripts.data import Henakart

web = Blueprint("web", __name__)

@web.route("/")
def t_home():
    return render_template("index.html")

@web.route('/race', methods=['GET', 'POST'])
def plot_race():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    if file:
        print(file)
        data = Henakart(file)
        print("DATA", data.race)
        print("TYPE", type(data.race))
        drivers_list = data.drivers
        
        
        try:
            print("TRY")
            r = data.cleaning_data
        except Exception as e:
            print("EXCEPT", e)

       
        
        
        
    
        
    return render_template("race.html", drivers_list = drivers_list)
        
        