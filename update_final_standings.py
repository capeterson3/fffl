import json
import pandas as pd


def get_standings():

    final_standings = {}
    owner_finish = []
    for year in range(2005, 2020):
        with open("./standings/standings_" + str(year) + ".json", "r") as f:
            data = json.load(f)

        with open("./teams/team_numbers.json", "r") as k:
            team_nums = json.load(k)

        # owner_finish = []
        for team in range(0,12):

            team_key = data['fantasy_content']['league'][1]['standings'][0]['teams'][str(team)]['team'][0][0]['team_key']

            owner = team_nums[str(year)][team_key]
            clinched_playoffs = (1 if 'clinched_playoffs' in data['fantasy_content']['league'][1]['standings'][0]['teams'][str(team)]['team'][0][12] else 0)
            finish = data['fantasy_content']['league'][1]['standings'][0]['teams'][str(team)]['team'][2]['team_standings']['rank']

            try:
                playoff_seed = data['fantasy_content']['league'][1]['standings'][0]['teams'][str(team)]['team'][2]['team_standings']['playoff_seed']
            except:
                playoff_seed = 0
            tmp_dict = {'year':year,'owner':owner,'finish':finish,'clinched_playoffs':clinched_playoffs, 'playoff_seed':playoff_seed}
            # owner_finish[owner] = tmp_dict
            owner_finish.append(tmp_dict)

        # df = pd.DataFrame(owner_finish)
        # df.to_csv('./test_output.csv')

    return owner_finish


def concat_team_numbers():
    team_numbers = {}
    for year in range(2005,2020):
        with open("./teams/team_numbers_" + str(year) + ".txt", "r") as f:
            team_nums = eval(f.read())

        team_numbers[year] = team_nums

    with open('./teams/team_numbers.json', 'w') as outfile:
        json.dump(team_numbers, outfile)

if __name__ == "__main__":
    final_standings_all_time = []

    # for year in range(2005,2020):
    final_standings_all_time = get_standings()

    pd.DataFrame(final_standings_all_time).to_csv('./test_output.csv')

    # with open('./final_standings_all_time.json', 'w') as outfile:
    #     json.dump(final_standings_all_time, outfile)

    # concat_team_numbers()


