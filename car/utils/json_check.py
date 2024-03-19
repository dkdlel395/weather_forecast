import json
def json_check():
    global roi_point_xy
    with open('C:/Users/jhp12/Desktop/park/git/weather-forecast/car/output/points.json') as f:
        roi_point_xy = json.load(f)
        f.close()