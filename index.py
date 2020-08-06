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

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://zack:zem1992@127.0.0.1/college_search'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# programs = []
# for program in data_p:
#     p = {}
#     p[program] = data_p[program]
#     programs.append(p)

# print(programs)

# db = SQLAlchemy(app)


# class Programs(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     program = db.Column(JSON)


# for college in programs:
#     db.session.add(Programs(program=college))
#     db.session.commit()


# alchemyEngine = create_engine(
#     'postgresql+psycopg2://zack:zem1992@127.0.0.1/college_search', pool_recycle=3600)
alchemyEngine = create_engine(
    'postgres://pmykabxshnofzn:6ad7d89187806b5a1d4e11303d66a3949639ebdc325121a485a1c2dad9570dc9@ec2-54-197-254-117.compute-1.amazonaws.com:5432/da3bms0hdo4bp7', pool_recycle=3600)
dbConnection = alchemyEngine.connect()
df_programs = pd.read_sql("select * from \"programs\"", dbConnection)
df_schools = pd.read_sql("select * from \"ma_school\"", dbConnection)
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


@app.route("/ma-schools")
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
