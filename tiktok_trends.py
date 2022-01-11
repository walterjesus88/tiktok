from TikTokApi import TikTokApi
import pandas as pd
api = TikTokApi.get_instance()

count = 30

tiktoks = api.by_hashtag("python", count=count)

data = []

#for tiktok in tiktoks:
#    print(tiktok)

  
for tiktok in tiktoks:
  	#print(tiktok['id'])


	json = {'id': tiktok['id'],'descripcion':tiktok['desc'],
			'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
			'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
			'fecha':tiktok['createTime']
			}

	data.append(json)

df = pd.DataFrame(data=data)
print(df)