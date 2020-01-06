import json
import pandas as pd
from postgres_functions import bulkInsert, return_table


def parse_scores(year):
    # load team number and names references as a dictionary
    team_numbers = {}
    with open("./teams/team_numbers.json", "r") as f:
        team_numbers = json.load(f)

    records_to_insert = []

    # Loop through 13 regular season weeks
    for i in range(0, 13):
        filename = (
            "./weekly_scoreboard/"
            + str(year)
            + "/week_"
            + str(i + 1)
            + "scoreboard.json"
        )
        with open(filename) as json_file:
            data = json.load(json_file)

        season = data["fantasy_content"]["league"][0]["season"]
        week = data["fantasy_content"]["league"][1]["scoreboard"]["week"]
        data = data["fantasy_content"]["league"][1]["scoreboard"]["0"]["matchups"]

        # Pad week number with leading 0 if less than 10
        week = week.zfill(2)

        # Loop through 6 matchups each week
        for i in range(0, 6):
            matchup_num = "'" + str(i) + "'"

            for j in range(1, 3):
                matchup_switch = "'" + str(j % 2) + "'"

                team = data[eval(matchup_num)]["matchup"]["0"]["teams"][
                    eval("'" + str(j - 1) + "'")
                ]["team"][0][0]["team_key"]
                team = team_numbers[str(year)][team]

                pts_for = data[eval(matchup_num)]["matchup"]["0"]["teams"][
                    eval("'" + str(j - 1) + "'")
                ]["team"][1]["team_points"]["total"]

                opponent = data[eval(matchup_num)]["matchup"]["0"]["teams"][
                    eval(matchup_switch)
                ]["team"][0][0]["team_key"]
                opponent = team_numbers[str(year)][opponent]

                pts_against = data[eval(matchup_num)]["matchup"]["0"]["teams"][
                    eval(matchup_switch)
                ]["team"][1]["team_points"]["total"]

                matchup = (
                    int(str(season) + str(week) + str(i) + str(j)),
                    season,
                    week,
                    team,
                    pts_for,
                    opponent,
                    pts_against,
                )
                records_to_insert.append(matchup)

    return records_to_insert


def create_csv_from_table(table):

    df = pd.DataFrame(return_table(table))
    # df = pd.DataFrame(tmp, index="id")
    print(df.head())

    df.loc[df["pts_for"] > df["pts_against"], "wins"] = 1
    df.loc[df["pts_for"] < df["pts_against"], "wins"] = 0
    df = df.sort_values(["team", "year", "week"])
    df["cum_season_wins"] = df.groupby(["team", "year"])["wins"].cumsum()

    print(df.head())
    df.to_csv("all_time_scores.csv")


if __name__ == "__main__":
    # for year in range(2005, 2020):
    #     print("Pulling scores from {}".format(year))
    #     records_to_insert = parse_scores(year)
    #     bulkInsert(records_to_insert)

    create_csv_from_table("scores")
