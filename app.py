import random

import requests
import pandas as pd


def get_countries(region):
    countries = requests.get("https://restcountries.eu/rest/v2/region/{}?fields=name;capital".format(region)).json()
    return random.sample(countries, len(countries))


def check(random_country, answer):
    return answer.lower() == random_country['capital'].lower()


def game():
    answers = []

    region = input("Choose your region: Africa, Americas, Asia, Europe, Oceania\n").lower()
    if region not in ['africa', 'americas', 'asia', 'europe', 'oceania']:
        print('Incorrect region. ')
        game()
    else:
        countries = get_countries(region)
        score = 0
        total = 0
        print("Game is starting. Enter 'EXIT' to stop the game.")
        for country in countries:
            total += 1
            print("What is the capital of {}?".format(country['name']))
            answer = input()
            if not answer.lower() == 'exit':
                if check(country, answer):
                    score += 1
                    print("Correct! Moving on.")
                else:
                    print("Incorrect! Here's the next one.")

                answers.append({
                    'Country': country['name'],
                    'Capital': country['capital'],
                    'Your Answer': answer.title(),
                })

            else:
                break

        print("You scored {} out of {}. That is a {:.0%} score.".format(score, total, score / total))

        print("The correct answers were:\n")

        print(pd.DataFrame(answers)[['Country', 'Capital', 'Your Answer']])

        print('The answers have been saved to your system')

        pd.DataFrame(answers).to_csv('game.csv')


game()
