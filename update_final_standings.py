import json
import pandas as pd


def get_standings(year):

    final_standings = {}
    owner_finish = []

    with open("./standings/standings_" + str(year) + ".json", "r") as f:
        data = json.load(f)

    with open("./teams/team_numbers.json", "r") as k:
        team_nums = json.load(k)

    # owner_finish = []
    for team in range(0, 12):

        team_key = data["fantasy_content"]["league"][1]["standings"][0]["teams"][
            str(team)
        ]["team"][0][0]["team_key"]

        owner = team_nums[str(year)][team_key]
        clinched_playoffs = (
            1
            if "clinched_playoffs"
            in data["fantasy_content"]["league"][1]["standings"][0]["teams"][str(team)][
                "team"
            ][0][12]
            else 0
        )
        finish = data["fantasy_content"]["league"][1]["standings"][0]["teams"][
            str(team)
        ]["team"][2]["team_standings"]["rank"]

        try:
            playoff_seed = data["fantasy_content"]["league"][1]["standings"][0][
                "teams"
            ][str(team)]["team"][2]["team_standings"]["playoff_seed"]
        except:
            playoff_seed = 0
        tmp_dict = {
            "year": year,
            "owner": owner,
            "finish": finish,
            "clinched_playoffs": clinched_playoffs,
            "playoff_seed": playoff_seed,
        }
        # owner_finish[owner] = tmp_dict
        owner_finish.append(tmp_dict)

    return owner_finish


if __name__ == "__main__":

    final_standings_all_time = []

    for year in range(2005, 2020):
        # year = 2010
        tmp_dict = get_standings(year)
        final_standings_all_time.extend(tmp_dict)

    pd.DataFrame(final_standings_all_time).to_csv("./final_standings_all_time.csv")

    final_standings_all_time = {}

    for year in range(2005, 2020):
        # year = 2010
        final_standings_all_time[year] = get_standings(year)

    with open("./final_standings_all_time.json", "w") as outfile:
        json.dump(final_standings_all_time, outfile)

