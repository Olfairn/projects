import gym
import time
import numpy as np
from sklearn.ensemble import RandomForestClassifier

env = gym.make('CartPole-v1')

# GRUNDLEGENDE BEFEHLE

#make a new environment
env.reset()

#display the environmemt
env.render()
time.sleep(5)

# close the gui
env.close()

env.step(0) #move cart left
env.step(1) #move cart right


# AUFBAU EINES POLICY SPACE

def collect_training_data(env):
    """build a policy space, linking of states to actions and associated rewards"""
    
    number_of_games = 200
    last_moves = 25
    observations = []
    actions = []

    for i in range(number_of_games):
        game_obs = []
        game_acts = []
        
        obs = env.reset()
        # Initiale Daten über das environment

        for j in range(1000):
            action = env.action_space.sample()
            # Der Wagen machr einen zufälligen Schritt
            obs, reward, done, _ = env.step(action)
            # obs: position of the cart, velocity of the cart, angle of the pole, rotation of the pole
            # reward: in diesem Beispiel immer 1 für jeden weiteren Zeitschritt, der geschafft wird
            # done: boolean that tells us if we've failed
            game_obs.append(obs)
            game_acts.append(action)

            if done:
                observations += game_obs[:-(last_moves+1)]
                actions += game_acts[1:-last_moves]
                # actions und observations sind um eins verschoben; so kann das Modell Beobachtungen und Aktionen zusammenbringen und daraus lernen
                # Zusammen sind: Die Beobachtung und die darauf folgende Aktion. D.h. wir wollen, dass wir nur "gute" Kombinationen aus Beobachtung und Aktion haben, damit das Modell diese lernt.
                # Die Aktionen sollen auf die vorhergehende Beobachtung angepasst werden
                # die letzten 25 moves vor dem "Crash" werden verworfen
                break

    observations = np.array(observations)
    actions = np.array(actions)

    return observations, actions

# FUNCTION TO PLAY THE GAME

def smart_rl(env, m):
    """now play the game with a trained rl agent"""
    # setup the game
    obs = env.reset()

    for i in range(1000):
        # start to play the game
        # model, tell me what to do next please
        obs = obs.reshape(-1,4)
        action = int(m.predict(obs))

        # take an according step
        obs,reward,done,_ = env.step(action)
        # visusalise my results
        env.render()
        # print(obs, reward)
        time.sleep(0.1)
        # find out if i died
        if done:
            print(f'iterations survived {i}')
            env.close()
            break
        
# PLAY THE GAME

env = gym.make('CartPole-v1')

# collect training data
X,y = collect_training_data(env) 

# instantiate our agent, and fit on the data
m = RandomForestClassifier()
m.fit(X,y) # X = observations, y = actions
# Das Modell soll lernen, von gegebenen observations eine action abzuleiten
# ! HIER FEHLT NOCH DAS VERSTÄNDNIS, WARUM DAS FUNKTIONIERT

# now play the game
smart_rl(env,m)