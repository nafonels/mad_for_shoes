# ModuleNotFoundError: No module named 'clarifai' 오류로 막힘

#if you don't provide arguments, the script will look for INSTA_USER and INSTA_PW in the environment
from InstaPy.instapy import InstaPy

session = InstaPy(username='test', password='test')
session.login()

#likes specified amount of posts for each hashtag in the array (the '#' is optional)
#in this case: 100 dog-posts and 100 cat-posts
session.like_by_tags(['#dog', 'cat'], amount=100)

#likes specified amount of posts for each location in the array
#in this case: 100 posts geotagged at the chrysler building and 100 posts geotagged at the salton sea
session.like_by_locations(['26429/chrysler-building/', '224442573/salton-sea/'], amount=100)

#gets tags from image passed as instagram-url and likes specified amount of images for each tag
session.like_from_image(url='www.instagram.com/p/BSrfITEFUAM/', amount=100)

#likes 100 posts for each tag of your latest image
session.like_from_image(amount=100)

#likes 50 photos of other animals

session.like_by_tags(['#animals'], amount=50, media='Photo')
session.like_from_image(url='www.instagram.com/image', amount=50, media='Photo')

#likes 15 videos of cats

session.like_by_tags(['#cat'], amount=15, media='Video')
session.like_from_image(url='www.instagram.com/image', amount=15, media='Video')

session.end()