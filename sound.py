from TikTokApi import TikTokApi

api = TikTokApi.get_instance()

#count = 30

# You can find this from a tiktok getting method in another way or find songs from the discoverMusic method.
#sound_id = "7044682004830702342"

#tiktoks = api.by_sound(sound_id, count=count)

#for tiktok in tiktoks:
#    print(tiktok)
url='https://www.tiktok.com/@kasssinaloa1/video/7058117598390668550'
tiktok_url = api.get_tiktok_by_url(url)
print(tiktok_url)
https://github.com/cubernetes/TikTokCommentScraper