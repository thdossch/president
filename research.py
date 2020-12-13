import sys
import os
from contextlib import redirect_stdout
import torch

from president import President
from heuristic_player  import HeuristicPlayer
from random_player  import RandomPlayer
from deep_q_learning_agent import DeepQLearningAgent
from big_deep_q_learning_agent import BigDeepQLearningAgent
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

def test_for_small_dqn(path):
        ai = DeepQLearningAgent("Anton", True)

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))
        
        session = President(players)
        
        torch.save(ai.network, f"{path}/0k.pt")
        # 5k
        network_name = f"{path}/5k.pt"
        session.train(5000, 1000)
        torch.save(ai.network, network_name)
        ai.training = False
        session.simulate(5000)

        # 20k
        ai.training = True 
        network_name = f"{path}/20k.pt"
        session.train(15000, 1000)
        torch.save(ai.network, network_name)
        ai.training = False
        session.simulate(5000)

        # 50k
        ai.training = True 
        network_name = f"{path}/50k.pt"
        session.train(30000, 10000)
        torch.save(ai.network, network_name)
        ai.training = False
        session.simulate(10000)

        # 70k
        ai.training = True 
        network_name = f"{path}/20k.pt"
        session.train(20000, 10000)
        torch.save(ai.network, network_name)
        ai.training = False
        session.simulate(10000)

        # 100k
        ai.training = True 
        network_name = f"{path}/100k.pt"
        session.train(50000, 10000)
        torch.save(ai.network, network_name)
        ai.training = False
        session.simulate(10000)

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

    total_results_random = []
    total_results_heuristic = []

    step = 10
    for a in range(0, step + 1):
        results_random = []
        results_heuristic = []
        for g in range(0, step + 1):
            gamma = g/step
            alpha = a/step
            print(f"Calculating for alpha = {alpha}, gamma = {gamma}")
            
            ai = TemporalDifferenceAgent("small Anton", alpha, gamma)

            amount = 10000

            players = [ai, RandomPlayer("Random 1")]
            players.append(RandomPlayer("Random 2"))
            players.append(RandomPlayer("Random 3"))

            session = President(players)
            session.train(50000)
            ai.stop_training()

            ranks = session.simulate(amount)
            results_random.append(round(ranks[ai]['p']/amount*100, 2))

            players = [ai, HeuristicPlayer("Heuristic 1")]
            players.append(HeuristicPlayer("Heuristic 2"))
            players.append(HeuristicPlayer("Heuristic 3"))

            session = President(players)
            
            ranks = session.simulate(amount)
            results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))

        total_results_random.append(results_random)
        total_results_heuristic.append(results_heuristic)

            
    with open(f'{path}/results.py', 'a') as f:
        with redirect_stdout(f):

            #imports
            print("from mpl_toolkits.mplot3d import Axes3D")
            print("import matplotlib.pyplot as plt")
            print("from matplotlib import cm")
            print("from matplotlib.ticker import LinearLocator, FormatStrFormatter")
            print("import numpy as np")

            #figure
            print("fig = plt.figure()")
            print("ax = fig.gca(projection='3d')")

            print("res_random = [")
           
            for res in total_results_random:
                print(res, end="")
                print(",")

            print("]")

            #data
            print(f"gamma = np.arange(0, {1+1/step}, {1/step})")
            print(f"alpha = np.arange(0, {1+1/step}, {1/step})")
            print("X, Y = np.meshgrid(gamma, alpha)")
            print("Z = np.array(res_random)")

            # Plot the surface.
            print("surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)")
            print("ax.set_zlim(0, 100)")
            print("ax.zaxis.set_major_locator(LinearLocator(10))")
            print("ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))")
            print("fig.colorbar(surf, shrink=0.5, aspect=5)")

            #names
            print("plt.xlabel('gamma')")
            print("plt.ylabel('alpha')")
            print("plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])")
            print("plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])")

            print("plt.show()")
            print("plt.clf()")

            # PLOT 2
            #figure
            print("fig = plt.figure()")
            print("ax = fig.gca(projection='3d')")

            print("res_heuristic = [")
            
            for res in total_results_heuristic:
                print(res, end="")
                print(",")
            print("]")

            #data
            print(f"gamma = np.arange(0, {1+1/step}, {1/step})")
            print(f"alpha = np.arange(0, {1+1/step}, {1/step})")
            print("X, Y = np.meshgrid(gamma, alpha)")
            print("Z = np.array(res_heuristic)")

            # Plot the surface.
            print("surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)")
            print("ax.set_zlim(0, 100)")
            print("ax.zaxis.set_major_locator(LinearLocator(10))")
            print("ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))")
            print("fig.colorbar(surf, shrink=0.5, aspect=5)")

            #names
            print("plt.xlabel('gamma')")
            print("plt.ylabel('alpha')")
            print("plt.xticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])")
            print("plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])")


            print("plt.show()")


def results_small_q_table_zoomed_in():
    path = "q_table_results"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)

    try:
        file = open(f"{path}/results_zoomed.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    total_results_random = []
    total_results_heuristic = []

    for alpha in [0.05,0.1,0.15,0.2,0.25,0.3]:
        results_random = []
        results_heuristic = []
        for gamma in [0.55,0.6,0.65,0.7,0.75,0.8]:
            print(f"Calculating for alpha = {alpha}, gamma = {gamma}")
            
            ai = TemporalDifferenceAgent("small Anton", alpha, gamma)

            amount = 10000

            players = [ai, RandomPlayer("Random 1")]
            players.append(RandomPlayer("Random 2"))
            players.append(RandomPlayer("Random 3"))

            session = President(players)
            session.train(100000)
            ai.stop_training()

            ranks = session.simulate(amount)
            results_random.append(round(ranks[ai]['p']/amount*100, 2))

            players = [ai, HeuristicPlayer("Heuristic 1")]
            players.append(HeuristicPlayer("Heuristic 2"))
            players.append(HeuristicPlayer("Heuristic 3"))

            session = President(players)
            
            ranks = session.simulate(amount)
            results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))

        total_results_random.append(results_random)
        total_results_heuristic.append(results_heuristic)

            
    with open(f'{path}/results_zoomed.py', 'a') as f:
        with redirect_stdout(f):

            #imports
            print("from mpl_toolkits.mplot3d import Axes3D")
            print("import matplotlib.pyplot as plt")
            print("from matplotlib import cm")
            print("from matplotlib.ticker import LinearLocator, FormatStrFormatter")
            print("import numpy as np")

            #figure
            print("fig = plt.figure()")
            print("ax = fig.gca(projection='3d')")

            print("res_random = [")
           
            for res in total_results_random:
                print(res, end="")
                print(",")

            print("]")

            #data
            print(f"gamma = np.array([0.55,0.6,0.65,0.7,0.75,0.8])")
            print(f"alpha = np.array([0.05,0.1,0.15,0.2,0.25,0.3])")
            print("X, Y = np.meshgrid(gamma, alpha)")
            print("Z = np.array(res_random)")

            # Plot the surface.
            print("surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)")
            print("ax.set_zlim(0, 100)")
            print("ax.zaxis.set_major_locator(LinearLocator(10))")
            print("ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))")
            print("fig.colorbar(surf, shrink=0.5, aspect=5)")

            #names
            print("plt.xlabel('gamma')")
            print("plt.ylabel('alpha')")
            print("plt.xticks([0.55,0.6,0.65,0.7,0.75,0.8])")
            print("plt.yticks([0.05,0.1,0.15,0.2,0.25,0.3])")

            print("plt.show()")
            print("plt.clf()")

            # PLOT 2
            #figure
            print("fig = plt.figure()")
            print("ax = fig.gca(projection='3d')")

            print("res_heuristic = [")
            
            for res in total_results_heuristic:
                print(res, end="")
                print(",")
            print("]")

            #data
            print(f"gamma = np.array([0.55,0.6,0.65,0.7,0.75,0.8])")
            print(f"alpha = np.array([0.05,0.1,0.15,0.2,0.25,0.3])")
            print("X, Y = np.meshgrid(gamma, alpha)")
            print("Z = np.array(res_heuristic)")

            # Plot the surface.
            print("surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)")
            print("ax.set_zlim(0, 100)")
            print("ax.zaxis.set_major_locator(LinearLocator(10))")
            print("ax.zaxis.set_major_formatter(FormatStrFormatter('%.0f'))")
            print("fig.colorbar(surf, shrink=0.5, aspect=5)")

            #names
            print("plt.xlabel('gamma')")
            print("plt.ylabel('alpha')")
            print("plt.xticks([0.55,0.6,0.65,0.7,0.75,0.8])")
            print("plt.yticks([0.05,0.1,0.15,0.2,0.25,0.3])")


            print("plt.show()")

def results_small_q_table_epsilon():
    path = "q_table_results"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)

    try:
        file = open(f"{path}/results_epsilon.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    results_random = []
    results_heuristic = []
    eps_decs = [0.99, 0.999, 0.9999, 0.99999]
    for eps_dec in eps_decs:
        print(f"Calculating for esp_dec = {eps_dec}")
        
        ai = TemporalDifferenceAgent("small Anton", 0.1, 0.75)
        ai.epsilon_decay = eps_dec

        amount = 100000

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(100000)
        ai.stop_training()

        ranks = session.simulate(amount)
        results_random.append(round(ranks[ai]['p']/amount*100, 2))

        players = [ai, HeuristicPlayer("Heuristic 1")]
        players.append(HeuristicPlayer("Heuristic 2"))
        players.append(HeuristicPlayer("Heuristic 3"))

        session = President(players)
        
        ranks = session.simulate(amount)
        results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))

    with open(f'{path}/results_epsilon.py', 'a') as f:
        with redirect_stdout(f):
            print("\\begin{table}[H]")
            print("\\centering")
            print("\\begin{tabular}{|c|c|c|c|c|}")
            print("\hline")
            print(f"                & {'&'.join(str(x) for x in eps_decs)}\\\\")
            print("\hline")
            print(f"3 heuristieke speler  &{'&'.join(str(x) for x in results_random)}\\\\")
            print(f"3 random spelers      &{'&'.join(str(x) for x in results_heuristic)}\\\\")
            print("\hline")
            print("\end{tabular}")
            print("\caption{W/L voor Q-table agent in \% voor verschillende epsilondecay factoren}")
            print("\end{table}")



def q_table_win_in_time_results():
    path = "q_table_results"
    try:
        os.mkdir(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)

    try:
        file = open(f"{path}/results_win_in_time.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    results_random = []
    results_heuristic = []

    ai = TemporalDifferenceAgent("small Anton", 0.1, 0.75)
    amount = 100000
    for x in range(0,20):
        print(f"after {x*10000} trainings")

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(10000)
        eps_before = ai.epsilon
        ai.stop_training()

        ranks = session.simulate(amount)
        results_random.append(round(ranks[ai]['p']/amount*100, 2))

        players = [ai, HeuristicPlayer("Heuristic 1")]
        players.append(HeuristicPlayer("Heuristic 2"))
        players.append(HeuristicPlayer("Heuristic 3"))

        session = President(players)
        
        ranks = session.simulate(amount)
        results_heuristic.append(round(ranks[ai]['p']/amount*100, 2))

        ai.epsilon = eps_before
        ai.training = True

    with open(f'{path}/results_win_in_time.py', 'a') as f:
        with redirect_stdout(f):
     
            print("import matplotlib.pyplot as plt")
            print('plt.plot(', end='')
            print([(x+1)*10000 for x in range(0, 20)], end='')
            print(', ', end='')
            print(results_random, end='')
            print(', \'b\', label=\'vs random\')')

            print('plt.plot(', end='')
            print([(x+1)*10000 for x in range(0, 20)], end='')
            print(', ', end='')
            print(results_heuristic, end='')
            print(', \'r\', label=\'vs heuristic\')')

            # for plotting with matplotlib
            print()
            print('plt.xlabel("episodes")')
            print('plt.ylabel("W/L in %")')
            print('axes = plt.gca()')
            print('axes.set_ylim([0, 100])')
            print('plt.legend(loc="upper right")')
            print('plt.show()')
            print()
            print()

def normalized_input_results():
    path = "normalized_results"
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

    results_normal = []
    results_normalized = []

    for x in range(0, 8):
        print(f"Calculating for normal {x}")
        amount = 10000
        ai = BigDeepQLearningAgent("Anton", True)
        ai.normalized = False

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(80000, 20000)
        ai.training = False

        ranks = session.simulate(amount)
        results_normal.append(round(ranks[ai]['p']/amount*100, 2))

        ai = BigDeepQLearningAgent("Anton", True)

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(80000, 20000)
        ai.training = False

        ranks = session.simulate(amount)
        results_normalized.append(round(ranks[ai]['p']/amount*100, 2))
            
    with open(f'{path}/results.py', 'a') as f:
        with redirect_stdout(f):

            print("from matplotlib import pyplot as plt")
            print('plt.plot(', end='')
            print([i for i in range(1, 9)])
            print(', ', end='')
            print(results_normal, end='')
            print(', \'r\', label=\'normal\')')

            print('plt.plot(', end='')
            print([i for i in range(1, 9)])
            print(', ', end='')
            print(results_normalized, end='')
            print(', \'b\', label=\'normalized\')')

            # for plotting with matplotlib
            print()
            print('plt.xlabel("Network")')
            print('plt.ylabel("W/L in %")')
            print('axes = plt.gca()')
            print('axes.set_ylim([0, 100])')
            print('plt.legend(loc="upper right")')
            print('plt.xticks([1,2,3,4,5,6,7,8])')
            print('plt.show()')
            print()
            print()

def normalized_input_results():
    path = "normalized_results"
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

    results_normal = []
    results_normalized = []

    for x in range(0, 8):
        print(f"Calculating for normal {x}")
        amount = 10000
        ai = BigDeepQLearningAgent("Anton", True)
        ai.normalized = False

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(80000, 20000)
        ai.training = False

        ranks = session.simulate(amount)
        results_normal.append(round(ranks[ai]['p']/amount*100, 2))

        ai = BigDeepQLearningAgent("Anton", True)

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)
        session.train(80000, 20000)
        ai.training = False

        ranks = session.simulate(amount)
        results_normalized.append(round(ranks[ai]['p']/amount*100, 2))
            
    with open(f'{path}/results.py', 'a') as f:
        with redirect_stdout(f):

            print("from matplotlib import pyplot as plt")
            print('plt.plot(', end='')
            print([i for i in range(1, 9)])
            print(', ', end='')
            print(results_normal, end='')
            print(', \'r\', label=\'normal\')')

            print('plt.plot(', end='')
            print([i for i in range(1, 9)])
            print(', ', end='')
            print(results_normalized, end='')
            print(', \'b\', label=\'normalized\')')

            # for plotting with matplotlib
            print()
            print('plt.xlabel("Network")')
            print('plt.ylabel("W/L in %")')
            print('axes = plt.gca()')
            print('axes.set_ylim([0, 100])')
            print('plt.legend(loc="upper right")')
            print('plt.xticks([1,2,3,4,5,6,7,8])')
            print('plt.show()')
            print()
            print()

def simulate_heuristic_vs_random():

    players = []
    players.append(HeuristicPlayer("HeuristicPlayer"))
    players.append(RandomPlayer("Random 1"))
    players.append(RandomPlayer("Random 2"))
    players.append(RandomPlayer("Random 3"))


    session = President(players)
    session.simulate(50000)

    players = []
    players.append(HeuristicPlayer("HeuristicPlayer 1"))
    players.append(HeuristicPlayer("HeuristicPlayer 2"))
    players.append(HeuristicPlayer("HeuristicPlayer 3"))
    players.append(RandomPlayer("RandomPlayer"))

    session = President(players)
    session.simulate(50000)

def epsilon_decay_plot():
    try:
        file = open(f"epsilon_decay_plot.py", "x")
        file.close()
    except FileExistsError:
        print ("Creation of the outputfile failed")
        exit()

    with open(f'epsilon_decay_plot.py', 'a') as f:
        with redirect_stdout(f):
            print("from matplotlib import pyplot as plt")
            print("eps_stop = 0.05")
            print("for eps_dec, color in zip([0.99, 0.999, 0.9999, 0.99999], ['y', 'g', 'b', 'r']) :")
            print("\tplt.plot([1000*x for x in range(0, 350)], [max(1*eps_dec**(1000*x), eps_stop) for x in range(0, 350)], color, label=f'$\epsilon-decay = {eps_dec}$')")
            print("plt.xlabel('iterations')")
            print("plt.ylabel('$\epsilon$')")
            print("plt.yticks([0.,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1])")
            print("plt.legend(loc='upper right') ")
            print("plt.savefig('images/epsilon_decay.png')")
            print("plt.show()")





if __name__ == '__main__':
    #results_small_q_table_epsilon()
    #q_table_win_in_time_results()
    #exit()
    if False:
        ai = BigDeepQLearningAgent("Anton", True, "test.pt")

        players = [ai, RandomPlayer("Random 1")]
        players.append(RandomPlayer("Random 2"))
        players.append(RandomPlayer("Random 3"))

        session = President(players)

        network_name = "test.pt"
        session.train(50000, 1000)
        torch.save(ai.network, network_name)
        
        ai.training = False
        session.simulate(10000)
        exit()

    #results_for_gamma_0_100_small_dqn()
    ai = TemporalDifferenceAgent("mini Anton", 0.1, 0.75)

    players = [ai]
    players.append(RandomPlayer("Random 1"))
    players.append(RandomPlayer("Random 2"))
    players.append(RandomPlayer("Random 3"))

#    players = [ai]
#    players.append(HeuristicPlayer("Heuristic 1"))
#    players.append(HeuristicPlayer("Heuristic 2"))
#    players.append(HeuristicPlayer("Heuristic 3"))

    session = President(players)

    #session.train(1000000, 10000)
    ai.stop_training()

    session.simulate(100000)

    players = [ai]
    players.append(HeuristicPlayer("Heuristic 1"))
    players.append(HeuristicPlayer("Heuristic 2"))
    players.append(HeuristicPlayer("Heuristic 3"))

    session = President(players)
    session.simulate(100000)
