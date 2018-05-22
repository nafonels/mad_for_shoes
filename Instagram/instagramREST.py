from instagram.client import InstagramAPI

access_token = "1582036607.72d5f3a.aad4d272791f408c908017d4657e67e1"
client_secret = "a1dab8ead1f24b52928fdd1db8cef67d"
client_id = "72d5f3ac83034f4084ce58a71d52fb14"
api = InstagramAPI(access_token=access_token, client_secret=client_secret, client_id=client_id)
print(api.user())
print(api.user_recent_media())
# popular_media = api.media_popular(count=20)
# for media in popular_media:
#     print(media.images['standard_resolution'].url)
# api.user
# recent_media, next_ = api.user_recent_media(user_id="kimhyuncheol", count=10)
# for media in recent_media:
#    print(media.caption.text)
print(api.tag('신발'))
# api.tag_recent_media(count, max_tag_id, tag_name)*
# api.tag_search(q, count)*