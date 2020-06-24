import pyodbc 
import json
import math
from geographiclib.geodesic import Geodesic
geod = Geodesic.WGS84
from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
app     = Flask(__name__)
cors    = CORS(app,resources={r"/*": {"origins": "*"}})
print("HTTP/1.0 200 OK\n");

__connStr = 'Driver={SQL Server};Server=YOUR_SERVER;Database=YOUR_DATABASE;UID=YOUR_USER;PWD=YOUR_PASSWORD;'
 

@app.route('/api/getFlightLatLonAndMidpoint', methods=['GET'])
@cross_origin()
def getFlightLatLonAndMidpoint():
    data        = []
    json_result = ""
    fromCity    = request.args.get('fromCity')
    toCity      = request.args.get('toCity')
    viaCity     = request.args.get('viaCity')
    if(not fromCity):
        return jsonify({"error": "fromCity required"}), 400
    elif(not toCity):
        return jsonify({"error": "toCity required"}), 400
    try:
        conn = pyodbc.connect(__connStr)
        conn.autocommit = True
        cursor = conn.cursor()
        if(not viaCity):
            cursor.execute("exec spGetFlightLatLonAndMidpoint ?,?",fromCity, toCity)
        else:
            cursor.execute("exec spGetFlightLatLonAndMidpointVia ?,?,?",fromCity, toCity, viaCity)
        rows = cursor.fetchall();
        idx     = 0
        lon1    = 0
        lat1    = 0
        lon2    = 0
        lat2    = 0
        lon3    = 0
        lat3    = 0
        for row in rows:
            if(idx == 0):
                if(row[1] != None):
                    lon1 = float(row[1])
                if(row[2] != None):
                    lat1 = float(row[2])
            elif(idx == 1):
                if(row[1] != None):
                    lon2 = float(row[1])
                if(row[2] != None):
                    lat2 = float(row[2])
            else:
                if(row[1] != None):
                    lon3 = float(row[1])
                if(row[2] != None):
                    lat3 = float(row[2])
            idx = idx + 1
        
        if(not viaCity):
            g = geod.Inverse(lat1, lon1, lat2, lon2)
        else:
            g = geod.Inverse(lat1, lon1, lat3, lon3)
        h = geod.Inverse(lat1, lon1, lat2, lon2)
        l = geod.InverseLine(lat1, lon1, lat2, lon2, 32671)
        m = l.Position(0.5 * l.s13)
        if(not viaCity):
            json_result = '{"from": [' + str(lon1) + ',' + str(lat1) + ']' + ', "to" : [' + str(lon2) + ',' + str(lat2) + ']' + ', "mp" : [' + str(m['lon2']) + ',' + str(m['lat2']) + ']' + ', "distance" :' + str(g['s12']/1000) + ', "geometry1":{"type":"Point","coordinates" : [' + str(lon1) + ',' + str(lat1) + ']}' + ', "geometry2":{"type":"Point","coordinates" : [' + str(lon2) + ',' + str(lat2) + ']}}'
        else:
            h = geod.Inverse(lat3, lon3, lat2, lon2)
            json_result = '{"from": [' + str(lon1) + ',' + str(lat1) + ']' + ', "to" : [' + str(lon2) + ',' + str(lat2) + ']' + ', "via" : [' + str(lon3) + ',' + str(lat3) + ']' + ', "mp" : [' + str(m['lon2']) + ',' + str(m['lat2']) + ']' + ', "distance" :' + str(g['s12']/1000) + ', "distance2" :' + str(h['s12']/1000) + ', "geometry1":{"type":"Point","coordinates" : [' + str(lon1) + ',' + str(lat1) + ']}' + ', "geometry2":{"type":"Point","coordinates" : [' + str(lon2) + ',' + str(lat2) + ']}' + ', "geometry3":{"type":"Point","coordinates" : [' + str(lon3) + ',' + str(lat3) + ']}}'
    except pyodbc.ProgrammingError as ex:
        Msg = str(ex)
        data.append("error")
        data.append(Msg)
        return jsonify(data), 400
    except (pyodbc.Error) as ex:
        Msg = str(ex)
        data.append("error")
        data.append(Msg)
        return jsonify(data), 400
    except:
        Msg = str(sys.exc_info()[0])
        data.append("error")
        data.append(Msg)
        return jsonify(data), 400
    finally:
        conn.close();
        if(json_result):
            return json_result, 200
        else:
            Msg = "There is a null value in data!"
            data.append("error")
            data.append(Msg)
            return jsonify(data), 400
