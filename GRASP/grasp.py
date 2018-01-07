"""
AMMM MIRI Project
Semester 1: 2017
Author: Anthony Nixon, Mathieu Chiavassa"""

import time
import math
import sys
import random

# Global Params for Defining the Problem
# Constants used for clarity, actual program will use DATA structure below

# Default Custom DATA set
NURSES = 10
HOURS = 5
DEMAND_PER_HOUR = [2, 2, 1, 3, 3]
MINHOURS = 0
MAXHOURS = 9
MAXCONSEC = 3
MAXPRESENCE = 14

CUSTOM = {'nNurses': NURSES, 'nHours': HOURS, 'minHours': MINHOURS, 'maxHours': MAXHOURS,
          'maxPresence': MAXPRESENCE, 'maxConsec': MAXCONSEC, 'demand': DEMAND_PER_HOUR}


# TEST SETS - reassign to DATA from main()
SMALL = {
	   "nNurses": 30,
	   "nHours":9,
	   "minHours": 3,
	   "maxHours": 6,
	   "maxConsec": 7,
	   "maxPresence": 8,
	   "demand": [5, 3, 8, 5, 1, 7, 5, 6, 2]
}

MID = {
	   "nNurses": 200,
	   "nHours":24,
	   "minHours": 6,
	   "maxHours": 12,
	   "maxConsec": 6,
	   "maxPresence": 18,
	   "demand": [53, 24, 33, 40, 70, 12, 33, 55, 66, 12, 30, 22, 55,
               77, 88, 22, 34, 55, 22, 55, 23, 22, 11, 12]
}

LARGE = {
	   "nNurses": 1800,
	   "nHours":24,
	   "minHours": 6,
	   "maxHours": 18,
	   "maxConsec": 7,
	   "maxPresence": 24,
	   "demand": [964, 650, 966, 1021, 824, 387, 828, 952, 611, 468, 403, 561, 862,
               597, 1098, 855, 918, 1016, 897, 356, 615, 670, 826, 349]
}

# Run Params
MAXITR = 1 # iterations of grasp
ALPHA = 0.8 # greediness of construction, range [0,1]
DATA = CUSTOM # data set to use

# UTILITY FUNCTIONS
def get_candidate_list():
    """ Loads valid candidate schedule from file IF EXISTS
        OR Generates permutations for candiate list
        input: number of HOURS
        returns: initial candidate list of feasible work schedules

        NOTE: candidate list should be saved to JSON after generation
        """
    # Generate permutations of schedules from 0...2^(HOURS)-1
    # Candidates are generated from integers and traslated to bit-permutation/boolean
    # representation of a possible schedule
    # Each possible schedule is check for feasibility against the constraints using checkschedule()
    # The candidate_set is a matrix i,j where i is a feasible schedule and j is a given hour
    # position (0 = not work, 1 = work)
    candidate_set = []
    for i in range(2**DATA['nHours']):
        a_schedule = get_bin(i)
        # print(a_schedule) #DEBUG---------------
        if checkschedule(a_schedule):
            candidate_set.append(a_schedule)
    return candidate_set

def get_bin(x_in):
    """ Get the binary list representation of x.
    params: x - number to convert, n - number of digits
    returns: boolean list
    """
    x_str = format(x_in, 'b').zfill(DATA['nHours'])
    return [int(i) for i in x_str]


def checkschedule(schedule): # tested working
    """ Checks a shedule against constraints
        params: a schedule as boolean list
        returns: boolean value whether schedule conforms to constraint or not

        Constraint Description:
        a) the number of provided nurses is greater or equal to the demand

        b) Each nurse should work at least minHours hours.
        c) Each nurse should work at most maxHours hours.
        d) No nurse can stay at the hospital for more than maxPresence hours
        e) No nurse can rest for more than 1 consecutive hour
        f) Each nurse should work at most maxConsec hours
    """
    test = 0 # default to fail
    sumhours = sum(schedule)
    if sumhours == 0:
        test = 1 # automatic pass
    #Constraint minH and Constraint maxH
    elif sumhours >= DATA['minHours'] and sumhours <= DATA['maxHours']:
        i = 0
        while schedule[i] == 0:
            i = i+1
        imin = i
        i = len(schedule)-1
        while schedule[i] == 0:
            i = i - 1
        imax = i
        if imax-imin+1 <= DATA['maxPresence']:    #Constraints maxPresence
            compteur = 0
            for i in range(imin, imax+1):
                if schedule[i] == 0:              #Constraints rests and maxConsec
                    if compteur > DATA['maxConsec'] or (i < imax and schedule[i+1] == 0):
                        return 0 # automatic fail
                    compteur = 0 # reset count
                compteur += 1
            if compteur <= DATA['maxConsec']:
                test = 1 # final test passed
    return test

def f_x(solution):
    """ Objective Function for minimization of number of nurses scheduled
        params: a solution matrix of schedules for i nurses, j hours not-worked/worked
        returns: the sum of i nurses"""
    return len(solution)

def g_x(schedule, demand):
    """ Scoring Function for ranking feasible nurse schedules
        params: schedule - a schedule vector of elements 0 or 1 for h hours
                demand - a demand vector to score against
        returns: exponential scoring allows negative values in score to be
                very small penalty (positive number), while positive values
                will penalize more heavily. The case where the diff is 0
                is not added to score (hence the if statement).
    """
    score = 0 # score init to inf

    for i in range(DATA['nHours']):
        diff = demand[i] - schedule[i]
        if diff:
            score += math.exp(diff)
        # print(demand[i], '-', schedule[i], score) #DEBUG----------------
    return score

def euclidian(x, y):
    """ euclidean distance of two lists 
        params: x - diff vector, y - comparison vector
        returns: number score
    """
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(x, y)]))

def grasp_procedure(f_xp, g_xp, maxitr):
    """ Procedure function
        params:
            fx - optimization function
            gx - scoring function
            maxitr - number of iterations to run construct/local cycle
        returns: best solution after maxitr cycles"""

    # quick check that there are enough nurses to probably meet demand
    if DATA['nNurses'] < max(DATA['demand']):
        raise Warning('Not enough nurses!')

    candidate_set = get_candidate_list()
    xprime = [] # best solution init

    # iterate through multistart construct and local search cycles
    # through each cycle, replace best solution if better found
    for _ in range(maxitr):
        # alpha is greediness defined as initial param
        current_solutionx = construct_grasp(g_xp, ALPHA, candidate_set)
        current_solutionx = local_search(f_xp, current_solutionx, candidate_set)

        # when xprime has len 0 it initializes the first solution
        if (len(xprime) == 0) or (f_xp(current_solutionx) < f_xp(xprime)):
            xprime = current_solutionx
    return xprime

# Constructor function - gene
def construct_grasp(g_xp, alpha, candidate_set):
    """ Constructor function for GRASP
        params:
            gx - scoring function
            alpha - greediness
        returns: a valid solution (not necessarily optimal)

        Notes:
            Building a solution consists of adding nurses in sequence 1..NURSES
            - calculate the score of nurse(i,j) j E all feasible schedules for nurse i.
            - create RCL of n highest scores
            - Select j from RCL for nurse i using relative probability based on scores
            - Update the solution
            - subtrack j values from DEMAND_PER_HOUR
            - repeat, if (i > NURSES) OR (|DEMAND_PER_HOUR| == 0) then break

            SCORING:
                - BEFORE scoring discard all possible schedules that don't satisfy constraints
                g_x =
                sum([DEMAND_PER_HOUR_k - j_k]^2)/HOURS
                    How CLOSELY the nurse's schedule j satisfies the remaining demand

        """
    possible_solution_x = [] # init empty solution
    demand = DATA['demand'] # initial demand
    solved = False

    # print('demand: ', demand) #DEBUG------------------
    # print(candidate_set)

    for _ in range(DATA['nNurses']):
        # score all elements in the candidate set
        scored_c_set = [g_xp(sched, demand) for sched in candidate_set]
        smin = min(scored_c_set)
        smax = max(scored_c_set)

        # create RCL based on top scorers
        restricted_c_list = [c for s, c in zip(scored_c_set, candidate_set)
                             if s <= smin+alpha*(smax-smin)]
        # choose random element from RCL to add to solution
        solution_element = random.choice(restricted_c_list)
        # add selected schedule to solution
        possible_solution_x.append(solution_element)
        # remove element's work hours from demand
        demand = [a - b for a, b in zip(demand, solution_element)]

        #print('scored set', scored_c_set) #DEBUG------------
        #print('RCL', restricted_c_list) #DEBUG---------
        #print('selected', solution_element) #DEBUG--------
        #print('demand', demand) #DEBUG----------

        # check if there is any more demand - if demand is satisfied mark solved
        # otherwise continue loop until solved or out of nurses
        if max(demand) == 0:
            solved = True
            print("solved")
            break

    if solved:
        return possible_solution_x
    else:
        raise Warning('No feasible solution')

def get_num_negs(list):
    return len([i for i, a in enumerate(list) if a < 0])

def print_sol(solution):
    print "\n" # blank line
    for i in solution:
        print(i)
    demand = DATA['demand']
    totals = [sum(x) for x in zip(*solution)]
    tvd_diff = [a - b for a, b in zip(totals, demand)]
    print("\nTotals: " + str(totals))
    print("Demand: " + str(demand))
    print("Diff: " + str(tvd_diff))

def local_search(f_xp, current_solutionx, candidate_set):
    neighbor_set = [a for a in N_x(current_solutionx, candidate_set) if f_xp(a) < f_xp(current_solutionx)]

    x_elem = []
    if len(neighbor_set) == 0:
        x_elem = current_solutionx
    while len(neighbor_set) > 0:
        # select a random x from neighbor_set and then make sub list
        x_elem = random.choice(neighbor_set)
        neighbor_set = [a for a in N_x(current_solutionx, candidate_set) if f_xp(a) < f_xp(x_elem)]

    return x_elem


def N_x(solution, candidate_set):
    # Neighbor set will be all combinations of row removals where demand diff vector has NO NEGS
    neighbor_set = []
    demand = DATA['demand']
    totals = [sum(x) for x in zip(*solution)]
    tvd_diff = [a - b for a, b in zip(totals, demand)]

    for _, row_i in enumerate(solution):
        temp_solution = solution
        row_diff = [a-b for a, b in zip(tvd_diff, row_i)] # calculate new diff with row removal
        negs_count = get_num_negs(row_diff) # gets negs

        if(negs_count) == 0:
            temp_solution.remove(row_i)
            neighbor_set.append(temp_solution)

    return neighbor_set

def main():
    """ Program entry point """

    # execution
    try:
        t_init = time.time()
        solution = grasp_procedure(f_x, g_x, MAXITR)
        t_end = time.time()
        total = t_end-t_init
        print_sol(solution)
        print('Time: ' + str(total))
    except Warning as warn:
        print(warn.args)

if __name__ == "__main__":
    main()
