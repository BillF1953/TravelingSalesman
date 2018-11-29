import numpy as np 

class GA(object):
    def __init__(self, adj_matrix, population_size=100, n_iter=100):
        self.adj = adj_matrix             # defines distances between nodes
        self.pop_size = population_size   # size of soln space
        self.n_iter = n_iter              # No. iterations to run the algorithm
        self.n = len(adj_matrix)          # number of nodes

        # create initial population
        nodes = np.arange(self.n)
        self.population = [np.random.permutation(nodes) for _ in range(self.pop_size)]

    def evolve(self, mutation_prob, crossover_prob, k):
        parents = self.select_parents(k)
        n_parents = len(parents)
        offspring = []

        for _ in range(self.pop_size):
            p1 = parents[np.random.randint(0, n_parents)]
            p2 = parents[np.random.randint(0, n_parents)]
            if np.random.uniform(0, 1) < crossover_prob:
                children = self.crossover(p1, p2)
            else:
                children = (p1, p2)

            if np.random.uniform(0, 1) < mutation_prob:
                c1 = self.mutate(children[0])
                c2 = self.mutate(children[1])
            else:
                c1 = children[0]
                c2 = children[1]
            
            offspring.append(c1)
            offspring.append(c2)
        
        self.replace(offspring)


    def select_parents(self, k=6):
        selected_individuals = []

        # tournament selection
        for _ in range(self.pop_size):
            # Perform |population| tournaments
            competitors = []
            fitness = []

            # Randomly select k individuals to compete in tournament
            for _ in range(k):
                index = np.random.randint(0, self.pop_size)
                competitors.append(self.population[index])
                fitness.append(self.get_fitness(self.population[index][0:-1]))

            # Select winner of the tournament
            winner = np.argmin(fitness)
            selected_individuals.append(competitors[winner])

        return selected_individuals

    def mutate(self, ind):
        i1 = np.random.randint(0, len(ind))
        i2 = np.random.randint(0, len(ind))

        temp = ind[i1]

        ind[i1] = ind[i2]
        ind[i2] = temp 

        return ind 

    def crossover(self, p1, p2):
        childP1 = []

        # first child
        geneA = np.random.randint(0, len(p1))
        geneB = np.random.randint(0, len(p1))
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(p1[i])
            
        childP2 = [item for item in p2 if item not in childP1]
        c1 = childP1 + childP2
        
        # second child
        childP1 = []
        geneA = np.random.randint(0, len(p1))
        geneB = np.random.randint(0, len(p1))
        
        startGene = min(geneA, geneB)
        endGene = max(geneA, geneB)

        for i in range(startGene, endGene):
            childP1.append(p1[i])
            
        childP2 = [item for item in p2 if item not in childP1]
        c2 = childP1 + childP2

        return c1, c2 
        
    def get_fitness(self, ind):
        sum = 0
        for i in range(1, len(ind)):
            sum += self.adj[ind[i-1], ind[i]]

        return sum 

    def replace(self, offspring):
        #Select the n fittest from both population and offspring
        pool = self.population + offspring
        pool_fitness = []

        for individual in pool:
            pool_fitness.append((individual, self.get_fitness(individual)))

        pool_fitness = sorted(pool_fitness, key=lambda tup: tup[1])
        temp_population = []
        for i in range(self.pop_size): 
            temp_population.append(pool_fitness[i][0])

        self.population = temp_population
    
    def find_fittest(self):
        max_fit = None 
        for ind in self.population:
            fitness = self.get_fitness(ind)

            if max_fit is None:
                max_fit = fitness 
            elif fitness > max_fit:
                max_fit = fitness 
        
        return max_fit 

        

