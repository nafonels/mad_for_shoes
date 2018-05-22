import requests
import re


def get_post(shortcode):
    with requests.session() as s:
        s.headers['user-agent'] = 'Mozilla/5.0'
        eachpost = 'https://www.instagram.com/p/' + shortcode
        r = s.get(eachpost)
        display_url = re.search(r'"display_url": ?"([^"]+)"', r.text).group(1)
        edge_media_like = re.search(r'"edge_media_preview_like": {"count":?"([0-9]+)', r.text)
        return display_url, edge_media_like

if __name__ == '__main__':
    get_post('Bi9gX6ujs5X')