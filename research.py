import sys
import os
from contextlib import redirect_stdout
import torch

from president import President
from heuristic_player  import HeuristicPlayer
from random_player  import RandomPlayer
from deep_q_learning_agent import DeepQLearningAgent
from temporal_difference_learning_agent  import TemporalDifferenceAgent

def results_for_gamma_0_100_small_dqn_training(path):
    for g in range(0, 11):
        gamma = g/10
        
        ai = DeepQLearningAgent("Anton", True)
        ai.GAMMA = gamma

        random_players = True
        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))
        
        session = President(players)
        
        print(f"Training network with gamma = {gamma}")

        # 5k
        network_name = f"{path}/trained_for_5k/gamma_{g}.pt"
        session.train(5000, 10000)
        torch.save(ai.network, network_name)

        # 20k
        network_name = f"{path}/trained_for_20k/gamma_{g}.pt"
        session.train(15000, 10000)
        torch.save(ai.network, network_name)

        # 50k
        network_name = f"{path}/trained_for_50k/gamma_{g}.pt"
        session.train(30000, 10000)
        torch.save(ai.network, network_name)

        # 100k
        network_name = f"{path}/trained_for_100k/gamma_{g}.pt"
        session.train(50000, 10000)
        torch.save(ai.network, network_name)

def results_for_gamma_0_100_small_dqn_simulation(path):

    network_dirs = [
        "trained_for_5k", 
        "trained_for_20k", 
        "trained_for_50k", 
        "trained_for_100k"
    ]
    for network_dir in network_dirs:
        results_random = []
        results_heuristic = []

        for random_players in [True, False]:
            for g in range(0, 11):
                gamma = g/10
                network_name = f"{path}/{network_dir}/gamma_{g}.pt"
                
                ai = DeepQLearningAgent("Anton", False, network_name)

                amount = 10000

                if random_players: 
                    players = [ai, RandomPlayer("Random 1")]
                    players.append(RandomPlayer("Random 2"))
                    players.append(RandomPlayer("Random 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, vs random player")
                    ranks = session.simulate(amount)
                    results_random.append(round(ranks[ai]['p']/amount*100, 2))
                else:
                    players = [ai, HeuristicPlayer("Heuristic 1")]
                    players.append(HeuristicPlayer("Heuristic 2"))
                    players.append(HeuristicPlayer("Heuristic 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, vs heuristic player")
                    ranks = session.simulate(amount)
                    results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))
                

        with open(f'{path}/results.py', 'a') as f:
            with redirect_stdout(f):
         
                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_random, end='')
                print(', \'r\', label=\'vs random\')')

                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_heuristic, end='')
                print(', \'b\', label=\'vs heuristic\')')

                # for plotting with matplotlib
                print()
                print('plt.xlabel("Gamma")')
                print('plt.ylabel("W/L in %")')
                print(f'plt.title("Win/lose percentage after training {network_dir.split("_")[-1]} times")')
                print('axes = plt.gca()')
                print('axes.set_ylim([0, 100])')
                print('plt.legend(loc="upper right")')
                print('plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])')
                print('plt.show()')
                print()
                print()

def results_for_gamma_0_100_small_dqn():
    path = "./small_dqn_results"

    network_dirs = [
        "trained_for_5k", 
        "trained_for_20k", 
        "trained_for_50k", 
        "trained_for_100k"
    ]

    try:
            os.mkdir(path)
    except OSError:
            print ("Creation of the directory %s failed" % path)
            exit()

    for network_dir in network_dirs:
        try:
                os.mkdir(f"{path}/{network_dir}")
        except OSError:
                print ("Creation of the directory %s failed" % f"{path}/{network_dir}")
                exit()


    try:
        file = open(f"{path}/results.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    results_for_gamma_0_100_small_dqn_training(path)
    results_for_gamma_0_100_small_dqn_simulation(path)



def results_for_gamma_0_100_big_dqn_training(path):
    for g in range(0, 11):
        gamma = g/10
        
        ai = BigDeepQLearningAgent("Anton", True)
        ai.GAMMA = gamma

        random_players = True
        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))
        
        session = President(players)
        
        print(f"Training network with gamma = {gamma}")

        # 5k
        network_name = f"{path}/trained_for_5k/gamma_{g}.pt"
        session.train(5000, 10000)
        torch.save(ai.network, network_name)

        # 20k
        network_name = f"{path}/trained_for_20k/gamma_{g}.pt"
        session.train(15000, 10000)
        torch.save(ai.network, network_name)

        # 50k
        network_name = f"{path}/trained_for_50k/gamma_{g}.pt"
        session.train(30000, 10000)
        torch.save(ai.network, network_name)

        # 100k
        network_name = f"{path}/trained_for_100k/gamma_{g}.pt"
        session.train(50000, 10000)
        torch.save(ai.network, network_name)


def results_for_gamma_0_100_big_dqn_simulation(path):

    network_dirs = [
        "trained_for_5k", 
        "trained_for_20k", 
        "trained_for_50k", 
        "trained_for_100k"
    ]
    for network_dir in network_dirs:
        results_random = []
        results_heuristic = []

        for random_players in [True, False]:
            for g in range(0, 11):
                gamma = g/10
                network_name = f"{path}/{network_dir}/gamma_{g}.pt"
                
                ai = BigDeepQLearningAgent("Anton", False, network_name)

                amount = 10000

                if random_players: 
                    players = [ai, RandomPlayer("Random 1")]
                    players.append(RandomPlayer("Random 2"))
                    players.append(RandomPlayer("Random 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, vs random player")
                    ranks = session.simulate(amount)
                    results_random.append(round(ranks[ai]['p']/amount*100, 2))
                else:
                    players = [ai, HeuristicPlayer("Heuristic 1")]
                    players.append(HeuristicPlayer("Heuristic 2"))
                    players.append(HeuristicPlayer("Heuristic 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, vs heuristic player")
                    ranks = session.simulate(amount)
                    results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))
                

        with open(f'{path}/results.py', 'a') as f:
            with redirect_stdout(f):
         
                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_random, end='')
                print(', \'r\', label=\'vs random\')')

                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_heuristic, end='')
                print(', \'b\', label=\'vs heuristic\')')

                # for plotting with matplotlib
                print()
                print('plt.xlabel("Gamma")')
                print('plt.ylabel("W/L in %")')
                print(f'plt.title("Win/lose percentage after training {network_dir.split("_")[-1]} times")')
                print('axes = plt.gca()')
                print('axes.set_ylim([0, 100])')
                print('plt.legend(loc="upper right")')
                print('plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])')
                print('plt.show()')
                print()
                print()


def results_for_gamma_0_100_big_dqn():
    path = "./big_dqn_results"

    network_dirs = [
        "trained_for_5k", 
        "trained_for_20k", 
        "trained_for_50k", 
        "trained_for_100k"
    ]

    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        exit()

    for network_dir in network_dirs:
        try:
            os.mkdir(f"{path}/{network_dir}")
        except OSError:
            print ("Creation of the directory %s failed" % f"{path}/{network_dir}")
            exit()


    try:
        file = open(f"{path}/results.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    results_for_gamma_0_100_small_dqn_training(path)
    results_for_gamma_0_100_small_dqn_simulation(path)



def results_for_big_vs_small(path):
    path = "./big_vs_small"
    path_small = "./small_dqn_results"
    path_big = "./big_dqn_results"

    try:
        file = open(f"{path}/results.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    network_dirs = [
        "trained_for_5k", 
        "trained_for_20k", 
        "trained_for_50k", 
        "trained_for_100k"
    ]
    for network_dir in network_dirs:
        results_small = []
        results_big = []

        for small in [True, False]:
            for g in range(0, 11):
                gamma = g/10

                amount = 10000
                if small: 
                    network_name = f"{path_small}/{network_dir}/gamma_{g}.pt"
                    ai = DeepQLearningAgent("Anton", False, network_name)
                    players = [ai, RandomPlayer("Random 1")]
                    players.append(RandomPlayer("Random 2"))
                    players.append(RandomPlayer("Random 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, for small network")
                    ranks = session.simulate(amount)
                    results_small.append(round(ranks[ai]['p']/amount*100, 2))
                else:
                    network_name = f"{path_big}/{network_dir}/gamma_{g}.pt"
                    ai = BigDeepQLearningAgent("Anton", False, network_name)
                    players = [ai, RandomPlayer("Random 1")]
                    players.append(RandomPlayer("Random 2"))
                    players.append(RandomPlayer("Random 3"))

                    session = President(players)
                    
                    print(f"Start simulating for gamma = {gamma}, for big network")
                    ranks = session.simulate(amount)
                    results_big.append(round(ranks[ai]['p']/amount*100, 2))
                

        with open(f'{path}/results.py', 'a') as f:
            with redirect_stdout(f):
         
                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_small, end='')
                print(', \'b\', label=\'small network\')')

                print('plt.plot(', end='')
                print([g/10 for g in range(0, 11)], end='')
                print(', ', end='')
                print(results_big, end='')
                print(', \'r\', label=\'big network\')')

                # for plotting with matplotlib
                print()
                print('plt.xlabel("Gamma")')
                print('plt.ylabel("W/L in %")')
                print(f'plt.title("Win/lose percentage vs random player after training {network_dir.split("_")[-1]} times")')
                print('axes = plt.gca()')
                print('axes.set_ylim([0, 100])')
                print('plt.legend(loc="upper right")')
                print('plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])')
                print('plt.show()')
                print()
                print()


def results_small_q_table():
    path = "q_table_results"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
        exit()

    try:
        file = open(f"{path}/results.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()


    results_random = []
    results_heuristic = []
    for g in range(0, 11):
        gamma = g/10
        print(f"Calculating for gamma = {gamma}")
        
        ai = TemporalDifferenceAgent("small Anton", gamma, 0.7, 0.1)

        amount = 10000

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(100000)

        ranks = session.simulate(amount)
        results_random.append(round(ranks[ai]['p']/amount*100, 2))

        players = [ai, HeuristicPlayer("Heuristic 1")]
        players.append(HeuristicPlayer("Heuristic 2"))
        players.append(HeuristicPlayer("Heuristic 3"))

        session = President(players)
        
        ranks = session.simulate(amount)
        results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))
            

    with open(f'{path}/results.py', 'a') as f:
        with redirect_stdout(f):
     
            print('plt.plot(', end='')
            print([g/10 for g in range(0, 11)], end='')
            print(', ', end='')
            print(results_random, end='')
            print(', \'r\', label=\'vs random\')')

            print('plt.plot(', end='')
            print([g/10 for g in range(0, 11)], end='')
            print(', ', end='')
            print(results_heuristic, end='')
            print(', \'b\', label=\'vs heuristic\')')

            # for plotting with matplotlib
            print()
            print('plt.xlabel("Gamma")')
            print('plt.ylabel("W/L in %")')
            print('axes = plt.gca()')
            print('axes.set_ylim([0, 100])')
            print('plt.legend(loc="upper right")')
            print('plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])')
            print('plt.show()')
            print()
            print()

if __name__ == '__main__':
    #results_small_q_table()
    #exit()
    #results_for_gamma_0_100_small_dqn()
    ai = TemporalDifferenceAgent("mini Anton", 0.2, 0.75, 1)

    players = [ai]
    players.append(RandomPlayer("Random 1"))
    players.append(RandomPlayer("Random 2"))
    players.append(RandomPlayer("Random 3"))

#    players = [ai]
#    players.append(HeuristicPlayer("Random 1"))
#    players.append(HeuristicPlayer("Random 2"))
#    players.append(HeuristicPlayer("Random 3"))

    session = President(players)
    session.train(200000, 10000)
    ai.epsilon = 0

    session.simulate(10000)

