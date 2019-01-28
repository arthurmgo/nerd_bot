from urllib.request import urlopen
import json


class Giphy:

    def __init__(self, token):
        self.token = token

    def search(self, query):
        data = json.loads(
            urlopen("http://api.giphy.com/v1/gifs/search?q="+query+"&api_key="+self.token+"&limit=1").read())
        return data['data'][0]['bitly_url']


