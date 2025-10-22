
## Representation

- Permutation
	- Allow illegal (infinite) cycles
	- Don't allow illegal cycles
- List of cycles

## Selection

- K-tournament


## Variation

- Mutation
	- Insert
	- Swap
	- Inversion
	- Scramble
- Recombination
	- Copy overlap (use LCS algorithm)
	- Order crossover
	- Cycle crossover

## Elimination
- Lambda+mu-elimination


## Prompt

implement an evolutionary algorithm to solve the directed travelling salesman problem following this template. Use a permutation representation of the order of the cities traversed, adding a large penalty for each path with infinite distance, k-tournament selection with k=4 to select two parents until 500 children are created, scramble mutation of subset with length of 10% of number of cities with a 5% mutation rate and swap mutation with 10% mutation rate, order crossover operator, and lambda+mu elimination. Use a population size of 500, and run it for 500 generations or until the best score isn't improved for 100 generations. Dont forget to count the path from the last city to the starting city in the evaluation Write a function that converts our permutation representation to always start at city 0 to feed it to the Reporter class. 
