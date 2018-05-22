import sys
import urllib.request
import json

# [CODE 1]
if __name__ == '__main__':
    client_id = "72d5f3ac83034f4084ce58a71d52fb14"
    # [code 1]
    from_date = "2018-05-14"
    to_date = "2018-05-13"
    num_statuses = "10"
    access_token = "1582036607.72d5f3a.aad4d272791f408c908017d4657e67e1"
    https: // api.instagram.com / oauth / authorize /?client_id = CLIENT - ID & redirect_uri = REDIRECT - URI & response_type = token
    url = "https://api.instagram.com/v1/tags/nofilter/media/recent?access_token=%s" \
          % (access_token)

    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            data = json.loads(response.read().decode('utf-8'))
            print(data)
    except Exception as e:
        print(e)

# def get_request_url(url):
#     req = urllib.request.Request(url)
#     req.add_header("CLIENT ID", "72d5f3ac83034f4084ce58a71d52fb14")
#     try:
#         response = urllib.request.urlopen(req)
#         if response.getcode() == 200:
#             print("[%s] Url Request Success" % datetime.datetime.now())
#             return response.read().decode('utf-8')
#     except Exception as e:
#         print(e)
#
#     # [CODE 2]
#     base = "https://www.instagram.com"
#     explore = "/explore/tags/"
#     url = base + explore
#
#     # [CODE 3]
#     req = urllib.request.Request(url)
#
#     # [CODE 4]
#     try:
#         response = urllib.request.urlopen(req)
#         if response.getcode() == 200:
#             data = json.loads(response.read().decode('utf-8'))
#             page_id = data['id']
#             print("instagram Numeric ID : %s" % (page_id))
#     except Exception as e:
#         print(e)
