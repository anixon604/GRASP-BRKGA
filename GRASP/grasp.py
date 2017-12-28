# AMMM MIRI Project
# Semester 1: 2017
# Author: Anthony Nixon, Mathieu Chiavassa

import math
import sys
import random

# Global Params for Defining the Problem
NURSES = 20
HOURS = 24
DEMAND_PER_HOUR = [2, 2, 1, 1, 1, 2, 2, 3, 4, 6, 6, 7, 5, 8, 8, 7, 6,
                   6, 4, 3, 4, 3, 3, 3]
MINHOURS = 5
MAXHOURS = 9
MAXCONSEC = 3
MAXPRESENCE = 14

data = {'nNurses': NURSES, 'nHours': HOURS, 'minHours': MINHOURS, 'maxHours': MAXHOURS,
        'maxPresence': MAXPRESENCE, 'maxConsec': MAXCONSEC, 'demand': DEMAND_PER_HOUR}


# UTILITY FUNCTIONS
def generate_candidate_list():
    """ Generates permutations for candiate list
        input: number of nurses
        returns: initial candidate list """
# Filter candidate list with constraints and feasibility
    # a) not enough total nurses for demand -> NURSE < DEMAND_PER_HOUR_k for some k


def checkschedule(schedule):
    """ Checks a shedule against constraints
        input: a schedule as boolean list
        returns: boolean value whether schedule conforms to constraint or not

        Constraint Description:
        a) the number of provided nurses is greater or equal to the demand

        b) Each nurse should work at least minHours hours.
        c) Each nurse should work at most maxHours hours.
        d) No nurse can stay at the hospital for more than maxPresence hours
        e) No nurse can rest for more than 1 consecutive hour
        f) Each nurse should work at most maxConsec hours
    """
    test = 0
    sumhours = sum(schedule)
    if sumhours < data['minHours'] and sumhours != 0:     #Constraint minH
        test = 1
    if sumhours > data['maxHours']:                       #Constraint maxH
        test = 1
    if sumhours != 0:                                     #Constraints rests and maxPresence
        i = 0
        while schedule[i] == 0:
            i = i+1
        imin = i
        i = len(schedule)-1
        while schedule[i] == 0:
            i = i - 1
        imax = i
        for i in range(imin, imax):
            if schedule[i] == 0 and schedule[i+1] == 0:             #Constraints rests
                test = 1
        if imax-imin+1 > data['maxPresence']:                       #Constraints maxPresence
            test = 1

        compteur = 0
        for i in range(imin, imax+1):                     #Constraints maxConsec
            if schedule[i] == 1:
                compteur += 1
            else:
                if compteur > data['maxConsec']:
                    test = 1
                compteur = 0
        if compteur > data['maxConsec']:
            test = 1
    return test != True # invert the return value


def grasp_procedure(f_x, g_x, maxitr):
    """ Procedure function
        params:
            fx - optimization function
            gx - scoring function
            maxitr - number of iterations to run construct/local cycle
            returns: best solution after maxitr cycles"""
    xprime = sys.maxint # best solution
    alpha = 0.5 # greediness (0 - 1)

    # iterate through multistart construct and local search cycles
    # through each cycle, replace best solution if better found
    for i in range(maxitr):
        temporary_solutionx = construct_grasp(g_x, alpha)
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