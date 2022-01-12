#https://github.com/davidteather/TikTok-Api/issues/750
from TikTokApi import TikTokApi
import pandas as pd
import datetime
import json
from flask import Flask, request, render_template
import plotly.express as px
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

#app = Flask(__name__)
app = Flask(__name__,template_folder='../templates')
bootstrap = Bootstrap(app)


def inc(x):
    return x + 1
    
def convert_unix_date(date):
	ts = int(date)
	time = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	return time


def get_username(cuenta):
	print('---inicio--')
  	
	api = TikTokApi.get_instance(custom_verifyFp="verify_kxywv8jc_kkSTc3Ec_RPV8_4G12_AAjM_pJHR3PvDqnkl",use_test_endpoints=True)

	count = 30
	print('---cuenta--')
	print(cuenta)
	tiktoks = api.by_username(cuenta, count=count)
	print(tiktoks)

	#print(user)
	data = []
	for tiktok in tiktoks:
		print(tiktok['id'])
		json = {'user':cuenta,'id': tiktok['id'],'descripcion':tiktok['desc'],
				'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
				'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
				'fecha':tiktok['createTime']
				}
		data.append(json)

	df = pd.DataFrame(data=data)
	print(df)
	df['id'] = df['id'].apply(str)
	df['fecha'] = df['fecha'].apply(convert_unix_date)
	df.to_excel( cuenta + ".xlsx",index=False)
	return df

def get_database():
    from pymongo import MongoClient
    import pymongo
    #import ssl
    import certifi
    ca = certifi.where()

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://walter:B4r4th30n@cluster0.2xyrs.mongodb.net/user_shopping_list?retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING,tlsCAFile=ca)
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['user_byusername_list']
    
#from pymongo_test_insert import get_database
def insert_pymongo(cuenta,df):
		dbname = get_database()
		print(dbname)
		byusernames=[]
		# Create a new collection
		byusernames.append(cuenta)
		collection = dbname["users_items"]

		from dateutil import parser
		expiry_date = '2021-07-13T00:00:00.000Z'
		expiry = parser.parse(expiry_date)
	
		df.reset_index(inplace=True)
		data_dict = df.to_dict("records")
		#print(data_dict)
		# Insert collection
		collection.delete_many({ 'user': cuenta })
		collection.insert_many(data_dict)

		list_user = {"name" : cuenta,
		# "quantity" : 2,
		# "ingredients" : "all-purpose flour",
		"expiry_date" : expiry
		}
		users_name=dbname["users_list"]
		users_name.insert_one(list_user)

@app.route('/', methods=['GET','POST'])
def index():

	dbname = get_database()
	print('fsfffs')
	collections = dbname["users_items"] #list_collection_names()
	
	if request.method == 'POST':
		print('request')
		userfilter = request.form.get('user')
		cursor = collections.find({'user': userfilter})
	else:
		cursor = collections.find({})
	return render_template("index.html",collections=cursor)

@app.route('/trending')
def trending():
	api = TikTokApi.get_instance(custom_verifyFp="verify_kxywv8jc_kkSTc3Ec_RPV8_4G12_AAjM_pJHR3PvDqnkl",use_test_endpoints=True)

	trendingChallenges = api.by_trending(count = 30)

	#for tiktok in trendingChallenges:
  	#	print(tiktok)

	return render_template("trending.html",trending=trendingChallenges)


@app.route("/procesar" , methods=['GET','POST'])
def procesar():
    #if request.method == 'POST':
    cuenta = request.form['text']
    print(cuenta)

    df = get_username(cuenta)
    f=insert_pymongo(cuenta,df)

    return render_template('notdash2.html')

@app.route("/lista/<int:id>")
def list(id):
	return "<h2>My email is example@gmail.com</h2>"


if __name__ == '__main__':
    from gevent import monkey
    monkey.patch_all()


#flask run --without-threads


# if __name__ == "__main__":
#     app.run(debug=True)
    #web gunicorn --pythonpath src app:app


# run.py
# from gevent import monkey
# monkey.patch_all()

# from fmconsole.factory_app import create_app
# from fmconsole.factory_utils import socketio

# if __name__ == "__main__":
#     app = create_app()
#     # app.run()
#     socketio.run(app, port=5000, debug=False)