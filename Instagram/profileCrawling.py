import json, re, requests

user = 'dhdhl'

profile = 'https://www.instagram.com/' + user

with requests.session() as s:
    s.headers['user-agent'] = 'Mozilla/5.0'

    end_cursor = ''
    for count in range(1, 3):
        print('PAGE: ', count)

        r = s.get(profile, params={'max_id': end_cursor})
        data = re.search(
            r'window._sharedData = (\{.+?});</script>', r.text).group(1)

        j = json.loads(data)

        print(j)
        media = j['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']

        for node in (x['node'] for x in media['edges']):
            if node['is_video']:
                page = 'https://www.instagram.com/p/' + node['shortcode']
                r = s.get(page)
                url = re.search(r'"display_url": ?"([^"]+)"', r.text).group(1)
                print('VIDEO:', url)
            else:
                print('TEXT:', node['edge_media_to_caption'])

        end_cursor = re.search(r'"end_cursor": ?"([^"]+)"', r.text).group(1)