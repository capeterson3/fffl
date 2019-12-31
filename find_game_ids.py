import pandas as pd
from yahoo_oauth import OAuth2
import json
from json import dumps
import datetime


class Yahoo_Api:
    def __init__(self, consumer_key, consumer_secret, access_key):
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_key = access_key
        self._authorization = None

    def _login(self):
        global oauth
        oauth = OAuth2(None, None, from_file="./auth/oauth2yahoo.json")
        if not oauth.token_is_valid():
            oauth.refresh_access_token()


def UpdateLeague(year, lg_id):

    for id in range(350, 400):
        url = (
            "https://fantasysports.yahooapis.com/fantasy/v2/league/"
            + str(id)
            + ".l."
            + str(lg_id)
            + "/"
        )

        response = oauth.session.get(url, params={"format": "json"})

        if response.status_code == 200:
            # print("game ID for " + str(year) + " is " + str(id))
            r = response.json()
            if (
                r["fantasy_content"]["league"][0]["name"] == "FFFL"
                and r["fantasy_content"]["league"][0]["league_type"] == "private"
            ):
                return id
                break

        # r = response.json()
        # with open("league.json", "w") as outfile:
        #     json.dump(r, outfile)
        #     return


# Yahoo Keys
with open("./auth/oauth2yahoo.json") as json_yahoo_file:
    auths = json.load(json_yahoo_file)
yahoo_consumer_key = auths["consumer_key"]
yahoo_consumer_secret = auths["consumer_secret"]
yahoo_access_key = auths["access_token"]
# yahoo_access_secret = auths['access_token_secret']
json_yahoo_file.close()

with open("./league_id_mapping.json", "r") as m:
    league_id_doc = eval(m.read())


global yahoo_api
yahoo_api = Yahoo_Api(
    yahoo_consumer_key, yahoo_consumer_secret, yahoo_access_key
)  # , yahoo_access_secret)

yahoo_api._login()

for year in range(2016, 2020):
    league_id = league_id_doc[str(year)]["league_id"]
    print("Getting Id for " + str(year) + "...")
    game_id = UpdateLeague(year, league_id)
    print("game ID for " + str(year) + " is ***" + str(game_id))
