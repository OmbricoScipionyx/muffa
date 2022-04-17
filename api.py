from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine, text
import datetime

app = Flask(__name__)
api = Api(app)
engine = create_engine("mysql+pymysql://pizza:pizza@localhost/temp_hum?charset=utf8")



class HelloWorld(Resource):
    def get(self):
        date = str(datetime.datetime.now())
        date = date.split(".")
        date = date[0]

        date1 = str(datetime.datetime.now()-datetime.timedelta(minutes=60))
        date1 = date1.split(".")
        date1 = date1[0]
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM t_h where d_t between '{date1}' and '{date}';"))
            response = {"temperature":[], "humidity":[]}
            for row in result:
                date, temperature, humidity = row
                timestamp = date.timestamp()*1000
                response["temperature"].append([timestamp, temperature])
                response["humidity"].append([timestamp, humidity])
            print(response)
        return response

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
