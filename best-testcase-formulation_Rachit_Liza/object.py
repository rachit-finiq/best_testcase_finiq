import numpy as np
from read_file import *

# Normalizing constant
C = 1

# feature types
ks = ["solve_for", "placement", "strike_shift", "issue_date", "ac_type", "ac_freq",
      "ac_from", "ac_coupon_type", "pc_type", "pc_barrier", "pc_freq", "ye_type", "ye_barrier", "ye_freq", "payoff_type"]

# dict to store actual probablity
# of true distribution
dict = {}
for k in ks:
    dict[k] = {}
    dict[k][""] = 1

# reads from the input file and
# fills dict with the prob. values
prob_file = input("Enter Probabilty File Name: ")
for line in open('data/'+str(prob_file), 'r').readlines():
    x = line.strip().split(',')
    for i in range(1, len(x)-1, 2):
        dict[x[0]][x[i]] = float(x[i+1])


'''
Object class contains the features that define prob.
distribution of a particular dataset
'''


class Object:

    def __init__(self, input):
        self.features = input.split(',')
        [self.solve_for, self.placement, self.strike_shift, self.issue_date, self.ac_type, self.ac_freq,
            self.ac_from, self.ac_coupon_type, self.pc_type, self.pc_barrier, self.pc_freq, self.ye_type, self.ye_barrier, self.ye_freq, self.payoff_type] = self.features.copy()
        self.str = input

    # defines the true distribution of the dataset
    # needs to be hardcoded for diff. dataset
    def q(self):
        prob = 1
        for i, k in enumerate(ks):
            prob *= dict[k][self.features[i]]
        return (prob+1e-12) / C


'''
S: list of Objects
empirical probability distribution of S
returns a dict prob
'''


def p(S):
    prob = {}
    sz = len(S)
    for s in S:
        if s.str not in prob.keys():
            prob[s.str] = 1/sz
        else:
            prob[s.str] += 1/sz

    return prob


''' 
calculates KL Divergence 
of a set of objects S
'''


def KL_Divergence(S):
    prob = p(S)
    div = 0

    for s in prob.keys():
        div += prob[s] * np.log(prob[s] / Object(s).q())

    return div * div


'''
calculates the normalizing constant
which is the sum of all probability
'''


def Normalize():
    e1 = 0
    for st in st_list:
        s = Object(st)
        e1 += s.q()

    return e1


C = Normalize()