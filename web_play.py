import random

import requests
from fuzzywuzzy import fuzz


def get_countries(region):
    countries = requests.get(
        "https://restcountries.eu/rest/v2/region/{}?fields=name;capital;flag".format(region)).json()
    return random.sample(countries, len(countries))


def check(random_country, answer):
    return fuzz.partial_ratio(answer.lower(), random_country['capital'].lower()) >= 75


def spelling(country, answer):
    if check(country, answer):
        return fuzz.partial_ratio(answer.lower(), country['capital'].lower()) != 100


def get_country(countries):
    return next(countries)


def game(countries):
    answers = []

    score = 0
    total = 0

    for country in countries:
        total += 1
        print(f"What is the capital of {country['name']}?")
        answer = input()
        if not answer.lower() == 'exit':
            if check(country, answer):
                score += 1
                print("Correct! Moving on.")
            else:
                if answer.strip() == "":
                    print("Here's the next one.")
                else:
                    print("Incorrect! Here's the next one.")

    #         answers.append({
    #             'Country': country['name'],
    #             'Capital': country['capital'],
    #             'Your Answer': answer.title(),
    #             'Spelling Errors': spelling(country, answer)
    #         })
    #
    #     else:
    #         break
    #
    # print(f"You scored {score} out of {total}. That is a {score/total:.0%} score.")
    #
    # print("The correct answers were:\n")
    # print(pd.DataFrame(answers)[['Country', 'Capital', 'Your Answer', 'Spelling Errors']])

    # print('The answers have been saved to your system')
    # pd.DataFrame(answers).to_csv('game.csv', index=False)

    # player_details['score'] = score
    # player_details['attempted'] = total
    # player_details['pct'] = score / total
    #
    # db.create_table()
    # db.add_scores(player_details)
