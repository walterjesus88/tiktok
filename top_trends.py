# Starts TikTokApi
from TikTokApi import TikTokApi


api = TikTokApi.get_instance(custom_verifyFp="verify_kxywv8jc_kkSTc3Ec_RPV8_4G12_AAjM_pJHR3PvDqnkl",use_test_endpoints=True)


# Gets array of trending music objects


# Gets array of trending challenges (hashtags)
trendingChallenges = api.by_trending(count = 30)

for tiktok in trendingChallenges:
  print(tiktok)