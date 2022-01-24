from numpy import argmin
from numpy.random import randint
from numpy.random import rand, choice
from object import *
# from data_transform import *

np.random.seed(10)

'''
objective function is to minimise KL divergence 
of the probablity distribution of the set S
'''

def objective(S):
    # return mse(S)
    return KL_Divergence(S)

'''
tournament selection returns a random selection
based on highest score of the different possible sets
'''


def selection(pop, scores, k=3):
    # first random selection
    selection_ix = randint(len(pop))
    for ix in randint(0, len(pop), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return pop[selection_ix]

'''
crossover two parents to create two children
return children sets after crossover
'''


def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    
    # check for recombination
    if rand() < r_cross:
        
        # select crossover point that is not on the end of the string
        pt = randint(1, len(p1)-2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]

'''
mutation of a single parent
randomly removes some points in a population
and randomly add new points and return new population
'''


def mutation(indiv, r_mut, S):
    for i in range(len(indiv)):
        # check for a mutation
        if rand() < r_mut:
            indiv.remove(indiv[i])
            indiv.append(choice(S))

def migration(l1,l2):
    # print(len(l1))
    ml = min([len(l1),len(l2)])
    for ix in randint(0, ml, 5):
        tmp = l1[ix]
        l1[ix] = l2[ix]
        l2[ix] = tmp 


'''
genetic_algorithm returns best representative
population along with their scores
'''

def genetic_algorithm(objective, n_obj, n_iter, n_pop, r_cross, r_mut, S):
    # initial population of random bitstring
    pop = [choice(S, n_obj).tolist() for _ in range(n_pop)]
    num_sub_pop=4
    t=4

    sub_pop_sz=[0 for _ in range(num_sub_pop)]
    sub_pops=[[] for _ in range(num_sub_pop)]
    s=0
    while(num_sub_pop>0):
        sub_pop_sz[num_sub_pop-1] = n_pop//num_sub_pop
        n_pop -= sub_pop_sz[num_sub_pop-1]
        sub_pops[num_sub_pop-1] = pop[s:s+sub_pop_sz[num_sub_pop-1]]
        s+=sub_pop_sz[num_sub_pop-1]
        num_sub_pop -= 1
    # print(sub_pop_sz)
    
    # keep track of best solution
    best = [sub_pops[i][0] for i in range(t)]
    best_eval = [objective(sub_pops[i][0]) for i in range(t)]
    overall_best_eval=min(best_eval)
    which=argmin(np.array(best_eval))
    overall_best = best[which]

    # best, best_eval = 0, objective(pop[0])
    n_c=300
    check_convg=np.zeros((n_c,1))

    # enumerate generations
    for gen in range(n_iter):
        
        # evaluate all candidates in the population
        scores = [[] for _ in range(t)]
        for i in range(t):
            scores[i] = [objective(c) for c in sub_pops[i]]
        # scores = [objective(c) for c in pop]
        # check for new best solution
        # print(scores)
        for j in range(t):
            for i in range(sub_pop_sz[j]):
                if scores[j][i] < best_eval[j]:
                    best[j], best_eval[j] = sub_pops[j][i], scores[j][i]
        overall_best_eval=min(best_eval)
        which=argmin(np.array(best_eval))
        overall_best=best[which]
        
        check_convg[gen%n_c] = overall_best_eval

        print(">%d, new best score = %.12f" % (gen, overall_best_eval))
        res = all(ele == check_convg[0] for ele in check_convg)
        if res:
            print("Converged!")
            break

        # select parents
        selected = [[selection(sub_pops[i], scores[i]) for _ in range(sub_pop_sz[i])] for i in range(t)]
        # create the next generation
        children = [list() for _ in range(t)]

        for j in range(t):
            for i in range(0, sub_pop_sz[j], 2):
                # get selected parents in pairs
                # print("debug--- ",j,i)
                if i+1 == sub_pop_sz[j]:
                    p1, p2 = selected[j][i-1], selected[j][i]
                else:
                    p1, p2 = selected[j][i], selected[j][i+1]
                # crossover and mutation
                for c in crossover(p1, p2, r_cross):
                    # mutation
                    mutation(c, r_mut, S)
                    # store for next generation
                    children[j].append(c)
        if gen%10 == 0:
            for i in range(0,t,2):
                # migration(sub_pops[i],sub_pops[i+1])
                ml = min([len(sub_pops[i]),len(sub_pops[i+1])])
                for ix in randint(0, ml, 5):
                    tmp = sub_pops[i][ix]
                    sub_pops[i][ix] = sub_pops[i+1][ix]
                    sub_pops[i+1][ix] = tmp 
        
        # replace population
        sub_pops = children
        # pop = children
    
    return [overall_best, overall_best_eval]