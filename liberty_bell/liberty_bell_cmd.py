from __future__ import print_function
from machine import Liberty_Bell_Machine

if __name__ == '__main__':

    print("Welcome to the casino\n")

    n = int(raw_input("How many times would you like to spin? "))

    machine = Liberty_Bell_Machine("Liberty Bell Machine")

    total_won = 0

    for i in range(n):

        result = machine.spin(bet=1)
        total_won += result.winner_paid

        print(result)

    print("Total won: %i in %i bets" % (total_won, n))
