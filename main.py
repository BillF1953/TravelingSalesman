from genetic import GA
import pickle 
from time import perf_counter, strftime, gmtime
import os 

if __name__ == "__main__":
    with open('data/djibouti.p', 'rb') as f:
        adj = pickle.load(f)

    alg = GA(adj, population_size=500)

    data = {'fitness': [], 'time': []}
    t0 = perf_counter()
    for i in range(500):
        t2 = perf_counter()
        alg.evolve(0.2, 0.8, 4)
        t3 = perf_counter()
        data['time'].append(t3-t2)

        f, top_ind = alg.find_fittest()
        data['fitness'].append(f)

        if i % 20 == 0:
            t1 = perf_counter()
            print("Elapsed Time: {}; Fitness: {}".format(t1-t0, f))

    savepath = os.path.join(os.getcwd(), "results")
    if not os.path.exists(savepath):
        os.mkdir("results")

    with open(os.path.join(savepath, 'djibouti.p'), 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

    