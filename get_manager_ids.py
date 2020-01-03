import json


def get_manager_ids(year):
    filename = "./weekly_scoreboard/" + str(year) + "/week_1scoreboard.json"
    with open(filename) as json_file:
        data = json.load(json_file)

    with open("./teams/email_mapping.txt", "r") as f:
        email_mapping = eval(f.read())

    league_key = data["fantasy_content"]["league"][0]["league_key"]

    team_mapping = {}

    for matchup in range(0, 6):
        matchup_num = "'" + str(matchup) + "'"

        for team in range(0, 2):
            team_num = "'" + str(team) + "'"
            manager_data = data["fantasy_content"]["league"][1]["scoreboard"]["0"][
                "matchups"
            ][eval(matchup_num)]["matchup"]["0"]["teams"][eval(team_num)]["team"][0][
                19
            ][
                "managers"
            ][
                0
            ][
                "manager"
            ]

            nickname = manager_data["nickname"]
            # team_id = manager_data["manager_id"]
            team_id = data["fantasy_content"]["league"][1]["scoreboard"]["0"][
                "matchups"
            ][eval(matchup_num)]["matchup"]["0"]["teams"][eval(team_num)]["team"][0][1][
                "team_id"
            ]

            try:
                email = manager_data["email"]
            except:
                owner = input("Who is this?: " + nickname + " :")
                team_mapping[league_key + ".t." + team_id] = owner

            if "email" in manager_data:
                print("{}, team {}, {}".format(nickname, team_id, email))
                try:
                    team_mapping[league_key + ".t." + team_id] = email_mapping[email]
                except:
                    owner = input("Who's email is " + email + "?: ")
                    email_mapping[email] = owner
                    team_mapping[league_key + ".t." + team_id] = email_mapping[email]

    with open("./teams/team_numbers_" + str(year) + ".txt", "w+") as outfile:
        json.dump(team_mapping, outfile, sort_keys=True)

    # with open("./teams/email_mapping.txt", "w") as f:
    #     json.dump(email_mapping, f, sort_keys=True)



def concat_team_numbers():
    team_numbers = {}
    for year in range(2005,2020):
        with open("./teams/team_numbers_" + str(year) + ".txt", "r") as f:
            team_nums = eval(f.read())

        team_numbers[year] = team_nums

    with open('./teams/team_numbers.json', 'w') as outfile:
        json.dump(team_numbers, outfile)

if __name__ == "__main__":

    year = 2013
    # for year in range(2005, 2020):
    get_manager_ids(year)
