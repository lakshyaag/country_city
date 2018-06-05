import random

import pandas as pd
import requests
from fuzzywuzzy import fuzz

import db


def get_countries(region):
    countries = requests.get("https://restcountries.eu/rest/v2/region/{}?fields=name;capital".format(region)).json()
    return random.sample(countries, len(countries))


def check(random_country, answer):
    return fuzz.partial_ratio(answer.lower(), random_country['capital'].lower()) >= 75


def spelling(country, answer):
    if check(country, answer):
        return fuzz.partial_ratio(answer.lower(), country['capital'].lower()) is not 100


def game():
    answers = []

    player_details = {
        'name': input("What's your name?\n"),
        'location': input("Where are you from?\n")
    }

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
                    if answer.strip() == "":
                        print("Here's the next one.")
                    else:
                        print("Incorrect! Here's the next one.")

                answers.append({
                    'Country': country['name'],
                    'Capital': country['capital'],
                    'Your Answer': answer.title(),
                    'Spelling Errors': spelling(country, answer)
                })

            else:
                break

        print("You scored {} out of {}. That is a {:.0%} score.".format(score, total, score / total))

        print("The correct answers were:\n")
        print(pd.DataFrame(answers)[['Country', 'Capital', 'Your Answer', 'Spelling Errors']])

        # print('The answers have been saved to your system')
        # pd.DataFrame(answers).to_csv('game.csv', index=False)

        player_details['score'] = score
        player_details['attempted'] = total
        player_details['pct'] = score / total

        db.create_table()
        db.add_scores(player_details)


def play():
    print("To play the game, press 'P'. To see the scoreboard, press 'S'.")
    if input().lower() == 's':
        db.get_scores()
        exit(0)

    if input().lower() == 'p':
        print("The game is now starting. Please enter your details for the scoreboard.")
        game()
        print("Thank you for playing. To see the scoreboard, press 'S'.")
        if input().lower() == 's':
            db.get_scores()
            exit(0)
        exit(0)
    else:
        print('Incorrect entry.')
        play()


if __name__ == "__main__":
    play()
