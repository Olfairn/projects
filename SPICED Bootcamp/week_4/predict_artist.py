"""
This is the primary main program for predicting new song inputs
"""

import time
import pickle
from pyfiglet import Figlet


def welcome():
    """CLI visuals for the start of the program"""
    banner = Figlet()
    print(banner.renderText('GUESS THE ARTIST!!\n'))
    time.sleep(1)
    print(" Please enter some song lyrics.")
    time.sleep(1)
    print(" I will try to predict")
    time.sleep(1)
    print(" who wrote the song!")
    time.sleep(1)


def guess_artist(guess, model):
    """accepts unseen text and returns a probability distribution"""
    #guess = [guess]
    prediction = model.predict_proba([guess])
    return prediction


def output(prediction, model):
    """Fancy output"""
    print("\n ------------------------------------------------------------")
    print('\n This looks like a song from:')
    artists = model.steps[-1][1].classes_   
    print(Figlet().renderText(artists[prediction.argmax()]))
    print(f'probability: {prediction.max():.3f}')

if __name__ == '__main__':
    welcome()

    model = pickle.load(open('lyrics_model.pickle', 'rb'))

    guess = input(f"\n your lyrics:\n\n ")
    prediction = guess_artist(guess, model)
    output(prediction, model)
