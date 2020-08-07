import psycopg2
from flask import Flask, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSON
import pandas as pd
import json
import csv


with open('ma_schools.json') as f:
    data_ms = json.load(f)

with open('programs.json') as f:
    data_p = json.load(f)

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://telbfierjjqges:5fbcf8bb02daf595e0d47d9b366265cf64af7543ddbcd061f365bb138bb179dc@ec2-52-1-95-247.compute-1.amazonaws.com:5432/datbtt39dmvo1o'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# programs = []
# for program in data_ms:
#     programs.append(program)

# print(programs)

# db = SQLAlchemy(app)


# class MASchools(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     school = db.Column(JSON)


# for college in programs:
#     db.session.add(MASchools(school=college))
#     db.session.commit()


# alchemyEngine = create_engine(
#     'postgresql+psycopg2://zack:zem1992@127.0.0.1/college_search', pool_recycle=3600)

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

data_ms = json.dumps(data_ms)
data_p = json.dumps(data_p)


@app.route("/ma-schools")
def ma_schools():
    return json.dumps(schools.headers.add('Access-Control-Allow-Origin', '*'))


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
