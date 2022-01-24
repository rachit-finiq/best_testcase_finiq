from genetic_algorithm import *
from read_file import *
import matplotlib.pyplot as plt

# create list of all testcases
# st_list defined in read_file.py
for st in st_list:
    s = Object(st)
    S.append(s)

print("Press Enter to use default values.")

# define the total iterations
n_iter = input("Enter no. of total iterations: ")
if n_iter == '':
    n_iter = 1000
n_iter = int(n_iter)

# define the population size
n_pop = input("Enter size of population: ")
if n_pop == '':
    n_pop = 100
n_pop = int(n_pop)

# crossover rate
r_cross = input("Enter Crossover Rate: ")
if r_cross == '':
    r_cross = 0.9
r_cross = float(r_cross)

t1=5
t2=250
print("Varying Bucket Size from {} to {}.".format(t1,t2))

# store results
best_scores = []
best_populations = []

for obj in range(t1, t2, 5):
    print("Objects in a Population: ", obj)

    # mutation rate
    r_mut = 0.5 / float(obj)

    # perform the genetic algorithm search
    best, score = genetic_algorithm(
        objective, obj, n_iter, n_pop, r_cross, r_mut, S)
    best_scores.append(score)
    best_populations.append(best)

print("Generated Best Testcases for all Bucket Size.")

with open('result.txt', 'w') as f:
    for i, best_pop in enumerate(best_populations):
        f.write("Bucket Size: "+str(10+5*i)+"\n")
        f.write("Best Score: "+str(best_scores[i])+"\n")
        for p in best_pop:
            f.write(p.str+"\n")

x = list(range(t1, t2, 5))

plt.plot(x, best_scores)
plt.title("Variation of KL-Divergence with Basket Size")
plt.xlabel("Basket Size")
plt.ylabel("KL-Divergence Score")
plt.show()