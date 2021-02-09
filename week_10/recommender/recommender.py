from random import choice, random 
MOVIES = [
    'Movie1',
    'Movie2',
    'Movie3'
]

def get_movie_reco():
    return choice(MOVIES)

if __name__=='__main__':
    print(get_movie_reco())