#30 line ai, capable of 100% 2048s at 400 (Haven't tried many possibilies) sims per move. Runs far quicker on Linux systems with multiprocessing enabled.

from lib.Grid import *
import asyncio
import random
import multiprocessing

class AI:
    def __init__(self, multi_core=False):
        self.multi_core = multi_core
        self.init_dict()

    #Function to randomly generate 1 game
    def sim_game(self, game_state):
        temp_game = Grid(template=game_state)
        first_move = random.choice(list(Moves))
        temp_game.move(first_move)
        while True:
            if not temp_game.move(random.choice(list(Moves))): break
        return (first_move, temp_game.score())
    
    #Generates next move by simulating n games and returning highest average score per starting move
    def next_move(self, game_state, n_games):
        #Implements simple map multiprocessing, cpu_count - 1 stops from crashing on osx
        if self.multi_core == True:
            with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
                results = pool.map(self.sim_game, [copy.deepcopy(game_state) for i in range(n_games)])
                for result in results:
                    self.move_results[result[0]].append(result[1])
        else:
            results = []
            for i in range(n_games):
                results.append(self.sim_game(copy.deepcopy(game_state)))
            for result in results:
                self.move_results[result[0]].append(result[1])
        choices = []
        for i in Moves:
            if len(self.move_results[i]) == 0: continue
            choices.append((i, sum(self.move_results[i]) / len(self.move_results[i])))
        choices.sort(key=lambda x: x[1], reverse=True)
        self.init_dict()
        print(choices[0][0].name)
        #Returns next most optimal move
        return choices[0][0]
    
    #Initialises a dictionary to store average score per first move
    def init_dict(self):
        self.move_results = {}
        for i in Moves:
            self.move_results[i] = []