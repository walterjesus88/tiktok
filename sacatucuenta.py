from TikTokApi import TikTokApi
import pandas as pd
import datetime
api = TikTokApi.get_instance(custom_verifyFp="verify_ky4ygfmf_9UrY0ywf_ncnN_4EjM_94BZ_dFwuQuwrVk2Q",use_test_endpoints=True)

# count = 100
# cuenta = str(input("Escribe la cuenta tiktok analizar: "))
tiktoks = api.by_username('tottusperu', count=30)

# data = []


for tiktok in tiktoks:
	print(tiktok)
# 	print(tiktok['stats'])


# 	jsonx = {'id': tiktok['id'],'descripcion':tiktok['desc'],
# 			'diggCount':tiktok['stats']['diggCount'],'shareCount':tiktok['stats']['shareCount'],
# 			'commentCount':tiktok['stats']['commentCount'],'playCount':tiktok['stats']['playCount'],
# 			'fecha':tiktok['createTime']
# 			}

# 	data.append(jsonx)

# df = pd.DataFrame(data=data)
# print(df)


# def convert_unix_date(date):
# 	ts = int(date)
# 	time = datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
# 	return time

# df['id'] = df['id'].apply(str)
# df['fecha'] = df['fecha'].apply(convert_unix_date)


# df.to_excel(cuenta+ ".xlsx",index=False)

