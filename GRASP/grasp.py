"""
AMMM MIRI Project
Semester 1: 2017
Author: Anthony Nixon, Mathieu Chiavassa"""

import math
import sys
import random

# Global Params for Defining the Problem
# Constants used for clarity, actual program will use DATA structure below
NURSES = 20
HOURS = 3
DEMAND_PER_HOUR = [2, 2, 1, 1, 1, 2, 2, 3, 4, 6, 6, 7, 5, 8, 8, 7, 6,
                   6, 4, 3, 4, 3, 3, 3]
MINHOURS = 0
MAXHOURS = 9
MAXCONSEC = 3
MAXPRESENCE = 14
# Run Params
MAXITR = 10 # iterations of grasp
ALPHA = 0.5 # greediness of construction, range [0,1]

DATA = {'nNurses': NURSES, 'nHours': HOURS, 'minHours': MINHOURS, 'maxHours': MAXHOURS,
        'maxPresence': MAXPRESENCE, 'maxConsec': MAXCONSEC, 'demand': DEMAND_PER_HOUR}


# PROGRAM ENTRY WILL GO HERE -----------------------
# check a) not enough total nurses for demand -> NURSE < DEMAND_PER_HOUR_k for some k

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
        if checkschedule(a_schedule):
            candidate_set.append(a_schedule)
    return candidate_set

def get_bin(x_in, n_len=HOURS):
    """ Get the binary list representation of x.
    params: x - number to convert, n - number of digits
    returns: boolean list
    """
    x_str = format(x_in, 'b').zfill(n_len)
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
    test = 0 # default to fail (due to inverse at return)
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


def grasp_procedure(f_x, g_x, maxitr):
    """ Procedure function
        params:
            fx - optimization function
            gx - scoring function
            maxitr - number of iterations to run construct/local cycle
        returns: best solution after maxitr cycles"""
    xprime = sys.maxint # best solution

    # iterate through multistart construct and local search cycles
    # through each cycle, replace best solution if better found
    for i in range(maxitr):
        temporary_solutionx = construct_grasp(g_x, ALPHA) # alpha is greediness defined as initial param
        temporary_solutionx = localSearch(f_x, temporary_solutionx) # see if var name ok
        if f_x(temporary_solutionx) < f_x(xprime):
            xprime = temporary_solutionx
        i = i+1

    return xprime

# Constructor function - gene
def construct_grasp(g_x, alpha):
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
    possible_solution_x = []
    candidate_set = []

    while candidate_set != []:
        # score all elements in the candidate set
        scored_c_set = [g_x(elem) for elem in candidate_set]
        smin = min(scored_c_set)
        smax = max(scored_c_set)

        # create RCL based on top scorers
        restricted_c_list = [s for s in scored_c_set if s <= smin+alpha*(smax-smin)]
        # choose random element from RCL to add to solution
        solution_element = random.choice(restricted_c_list)
        possible_solution_x.append(solution_element)
        candidate_set.remove(solution_element)
    return possible_solution_x

def localSearch(fx, x):
    return x