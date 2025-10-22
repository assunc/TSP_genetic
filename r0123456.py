import Reporter
import numpy as np
import random

class r0123456:

    def __init__(self):
        self.reporter = Reporter.Reporter(self.__class__.__name__)

    def evaluate(self, tour, distanceMatrix):
        total_distance = 0
        for i in range(len(tour) - 1):
            dist = distanceMatrix[tour[i]][tour[i + 1]]
            if np.isinf(dist):
                total_distance += 1e6  # Large penalty for infinite distance
            else:
                total_distance += dist
        # Add distance from last city back to start
        dist = distanceMatrix[tour[-1]][tour[0]]
        if np.isinf(dist):
            total_distance += 1e6
        else:
            total_distance += dist
        return total_distance

    def k_tournament_selection(self, population, scores, k=4):
        selected = random.sample(list(zip(population, scores)), k)
        selected.sort(key=lambda x: x[1])
        return selected[0][0]

    def scramble_mutation(self, individual, rate):
        if random.random() < rate:
            size = len(individual)
            subset_len = max(2, int(0.1 * size))
            start = random.randint(0, size - subset_len)
            subset = individual[start:start + subset_len]
            random.shuffle(subset)
            individual[start:start + subset_len] = subset
        return individual

    def swap_mutation(self, individual, rate):
        if random.random() < rate:
            i, j = random.sample(range(len(individual)), 2)
            individual[i], individual[j] = individual[j], individual[i]
        return individual

    def order_crossover(self, parent1, parent2):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [-1] * size
        child[start:end] = parent1[start:end]
        p2_index = 0
        for i in range(size):
            if child[i] == -1:
                while parent2[p2_index] in child:
                    p2_index += 1
                child[i] = parent2[p2_index]
        return child

    def normalize_to_zero(self, tour):
        idx = tour.index(0)
        return tour[idx:] + tour[:idx]

    def optimize(self, filename):
        file = open(filename)
        distanceMatrix = np.loadtxt(file, delimiter=",")
        file.close()

        num_cities = len(distanceMatrix)
        population_size = 500
        generations = 500
        mutation_rate_scramble = 0.05
        mutation_rate_swap = 0.10

        population = [random.sample(range(num_cities), num_cities) for _ in range(population_size)]
        scores = [self.evaluate(ind, distanceMatrix) for ind in population]

        best_score = min(scores)
        best_solution = population[scores.index(best_score)]
        no_improvement = 0

        for gen in range(generations):
            children = []
            while len(children) < population_size:
                p1 = self.k_tournament_selection(population, scores)
                p2 = self.k_tournament_selection(population, scores)
                child = self.order_crossover(p1, p2)
                child = self.scramble_mutation(child, mutation_rate_scramble)
                child = self.swap_mutation(child, mutation_rate_swap)
                children.append(child)

            child_scores = [self.evaluate(ind, distanceMatrix) for ind in children]
            combined = population + children
            combined_scores = scores + child_scores

            sorted_combined = sorted(zip(combined, combined_scores), key=lambda x: x[1])
            population = [x[0] for x in sorted_combined[:population_size]]
            scores = [x[1] for x in sorted_combined[:population_size]]

            meanObjective = np.mean(scores)
            current_best_score = scores[0]
            current_best_solution = population[0]

            if current_best_score < best_score:
                best_score = current_best_score
                best_solution = current_best_solution
                no_improvement = 0
            else:
                no_improvement += 1

            normalized_best = self.normalize_to_zero(best_solution)
            timeLeft = self.reporter.report(meanObjective, best_score, np.array(normalized_best))
            if timeLeft < 0 or no_improvement >= 100:
                break
        return 0

if __name__ == "__main__":
    r0123456().optimize("problems/tour50.csv")
