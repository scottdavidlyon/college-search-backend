
from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import create_engine
import pandas as pd
import json

app = Flask(__name__)
CORS(app)

alchemyEngine = create_engine(
    'postgres://telbfierjjqges:5fbcf8bb02daf595e0d47d9b366265cf64af7543ddbcd061f365bb138bb179dc@ec2-52-1-95-247.compute-1.amazonaws.com:5432/datbtt39dmvo1o', pool_recycle=3600)
dbConnection = alchemyEngine.connect()
df_programs = pd.read_sql("select * from \"programs\"", dbConnection)
df_schools = pd.read_sql("select * from \"ma_schools\"", dbConnection)
df_fields = pd.read_sql("select * from \"fields\"", dbConnection)
pd.set_option('display.expand_frame_repr', False)

schools = []
for index, row in df_schools.iterrows():
    schools.append(row['school'])

progs = []
for index, row in df_programs.iterrows():
    progs.append(row['program'])

fields = []
for index, row in df_fields.iterrows():
    fields.append(row['field'])


@app.route("/ma-schools", methods=['GET'])
def ma_schools():
    return json.dumps(schools)


@app.route("/ma-schools/<name>", methods=['GET'])
def school(name):
    found = next((x for x in schools if '-'.join(x['INSTNM'].split(
        ' ')) == name), None)
    return found


@app.route("/fields")
def fieldlookup():
    return json.dumps(fields)


@app.route("/programs")
def programs():
    return json.dumps(progs)


if __name__ == '__main__':
    app.run(debug=True)
