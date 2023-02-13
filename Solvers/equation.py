"""Module solving math problem afterwards"""
import itertools

"""Solve equation by brute force"""
if __name__ == '__main__':
    BLUE = 9
    RED = 2
    SHINY = 5
    CONCAVE = 7
    CORRODED = 3

    coins = [RED, BLUE, SHINY, CONCAVE, CORRODED]

    for (a,b,c,d,e) in itertools.permutations(coins) :
        if a + b * c**2 + d**3 - e == 399:
            print("Solution is ", [ a, b, c, d, e])
            break
