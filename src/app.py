#https://github.com/davidteather/TikTok-Api/issues/750
from TikTokApi import TikTokApi
import pandas as pd
import os
import datetime
import json
from flask import Flask, request, render_template
import plotly.express as px
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask import send_file
import plotly
import plotly.express as px


from pymongo import MongoClient
import pymongo
#import ssl
import certifi

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

	count = 100
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

	directory = 'byusername'
	if not os.path.exists(directory):
		os.makedirs(directory)

	df = pd.DataFrame(data=data)
	df['id'] = df['id'].apply(str)
	df['fecha'] = df['fecha'].apply(convert_unix_date)
	df.to_excel(os.path.join(directory, cuenta + ".xlsx"),index=False)
	#df.to_excel( cuenta + ".xlsx",index=False)
	return df

def get_hashtag(cuenta):
	api = TikTokApi.get_instance(custom_verifyFp="verify_kxywv8jc_kkSTc3Ec_RPV8_4G12_AAjM_pJHR3PvDqnkl",use_test_endpoints=True)
	hashtag = api.by_hashtag(cuenta, count=100)
	#print(hashtag)
	data = []

	for tiktok in hashtag:
		json = {'id': tiktok['id'],'descripcion':tiktok['desc'],
				'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
				'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
				'fecha':tiktok['createTime'],'video':tiktok['video']['id'],'author':tiktok['author']['uniqueId'],'usuario':"https://www.tiktok.com/@" +tiktok['author']['uniqueId']+"/video/"+tiktok['video']['id']
				}
		print(json['fecha'])
		json['fecha_f']=convert_unix_date(json['fecha'])
		data.append(json)

	directory = 'hashtag'
	if not os.path.exists(directory):
		os.makedirs(directory)

	df = pd.DataFrame(data=data)
	df['id'] = df['id'].apply(str)
	df['fecha'] = df['fecha'].apply(convert_unix_date)
	df.to_excel(os.path.join(directory, "hashtag.xlsx"),index=False)
	print(data)
	return data

def get_sound(sound):
	api = TikTokApi.get_instance()
	count = 30
	#sound_id = "7044682004830702342"
	sounds = api.by_sound(sound, count=count)
	data = []

	for tiktok in sounds:
		json = {'id': tiktok['id'],'descripcion':tiktok['desc'],
				'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
				'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
				'fecha':tiktok['createTime'],'usuario':"https://www.tiktok.com/@" +tiktok['author']['uniqueId']+"/video/"+tiktok['video']['id']
				}

		data.append(json)

	directory = 'sounds'
	if not os.path.exists(directory):
		os.makedirs(directory)

	df = pd.DataFrame(data=data)
	df['id'] = df['id'].apply(str)
	df['fecha'] = df['fecha'].apply(convert_unix_date)
	df.to_excel(os.path.join(directory, "sounds.xlsx"),index=False)
	return sounds

def get_database():

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
	collections = dbname["users_items"] #list_collection_names()
	#print(collections.find({}))	
	cursor = collections.find({}).sort([("fecha", pymongo.DESCENDING)])

	if cursor:
		data = []
		for tiktok in cursor:
			print(tiktok['id'])
			json = {'user':tiktok['user'],'id': tiktok['id'],'descripcion':tiktok['descripcion'],
					'diggCount':tiktok['diggCount'],'shareCount':tiktok['shareCount'],
					'commentCount':tiktok['commentCount'],'playCount':tiktok['playCount'],
					'fecha':str(tiktok['fecha'])
					}
			data.append(json)

		directory = 'byusername'
		if not os.path.exists(directory):
			os.makedirs(directory)

		if not data==[]:
			df = pd.DataFrame(data=data)
			df['id'] = df['id'].apply(str)
			df['fecha'] = df['fecha']
			df.to_excel(os.path.join(directory, "byusername.xlsx"),index=False)
	else:
		cursor = []

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

	trendingChallenges = api.by_trending(count = 100)

	data = []
	for tiktok in trendingChallenges:
		json = {'id': tiktok['id'],'descripcion':tiktok['desc'],
				'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
				'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
				'fecha':tiktok['createTime'],'usuario':"https://www.tiktok.com/@" +tiktok['author']['uniqueId']+"/video/"+tiktok['video']['id']
				}
		data.append(json)

	directory = 'trending'
	if not os.path.exists(directory):
		os.makedirs(directory)

	if not data==[]:
		df = pd.DataFrame(data=data)
		df['id'] = df['id'].apply(str)
		df['fecha'] = df['fecha'].apply(convert_unix_date)
		df.to_excel(os.path.join(directory, "trending.xlsx"),index=False)

	return render_template("trending.html",trending=trendingChallenges)

@app.route('/hashtag',methods=['GET','POST'])
def hashtag():
    df= []
    graph=[]
    cuenta=''
    if request.method == 'POST':
        cuenta = request.form['text']
        df = get_hashtag(cuenta)
            
        df1 = pd.DataFrame(data=df)     
        fig = px.line(df1, x='fecha_f', y='playCount',color='usuario',markers=True)
        graph = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("hashtag.html",hashtag=df,graphJSON=graph, header=cuenta,description='Grafico play - Usuario')

@app.route('/sound',methods=['GET','POST'])
def sound():
	df= []
	if request.method == 'POST':
		sound = request.form['text']
		df = get_sound(sound)

	
	print('sounds')
	print(df)
	return render_template("sound.html",sound=df)


@app.route("/getDownloadHashtag")
def getDownloadHashtag():
	return send_file('../hashtag/hashtag.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename='hashtag.xlsx',
                     as_attachment=True)

@app.route("/getDownloadByusername")
def getDownloadByusername():
	return send_file('../byusername/byusername.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename='byusername.xlsx',
                     as_attachment=True)

@app.route("/getDownloadTrending")
def getDownloadTrending():
	return send_file('../trending/trending.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename='trending.xlsx',
                     as_attachment=True)

@app.route("/getDownloadSound")
def getDownloadSound():
	return send_file('../sounds/sounds.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename='sounds.xlsx',
                     as_attachment=True)


@app.route("/procesar" , methods=['GET','POST'])
def procesar():
    #if request.method == 'POST':
    cuenta = request.form['text']
    print(cuenta)

    df = get_username(cuenta)
    f=insert_pymongo(cuenta,df)

    return send_file('../byusername/'+ cuenta + '.xlsx',
                     mimetype='text/xlsx',
                     attachment_filename=cuenta+'.xlsx',
                     as_attachment=True)

    #return render_template('notdash2.html')


@app.route('/chart1')
def chart1():
    dbname = get_database()
    collections = dbname["users_items"]
    cursor = collections.find({})
    data = []
    for tiktok in cursor:
        #print(tiktok['id'])
        dat = {'user':tiktok['user'],'id': tiktok['id'],'descripcion':tiktok['descripcion'],
                'diggCount':float(tiktok['diggCount']),'shareCount':tiktok['shareCount'],
                'commentCount':tiktok['commentCount'],'playCount':tiktok['playCount'],
                'fecha':str(tiktok['fecha'])}
        data.append(dat)

    df = pd.DataFrame(data=data)
    df['id'] = df['id'].apply(str)
    df=df.sort_values(by=['fecha'])
    print(df)
    df2 = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })
    print(df2)

    #fig = px.bar(df2, x="Fruit", y="Amount", color="City", barmode="group")
    #fig = px.bar(df, x="user", y="playCount", color="user", barmode="group")
    #print(fig)

    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    header="Estadísticas Diggcount por Usuario"
    description = """
    Número de Diggcount sobre las fechas de publicación de una determinada cuenta
    """

    #import plotly.express as px
	#df = px.data.gapminder().query("continent == 'Oceania'")
    fig = px.line(df, x='fecha', y='diggCount',color='user',markers=True)
	#fig.show()
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html', graphJSON=graphJSON, header=header,description=description)



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