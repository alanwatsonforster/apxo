from glass.tests.infrastructure import *

startfile(__file__, "forward movement")

# Check basic movement.

# H movements.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 2.5, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-1315", "N", 10, 3.0, "CL")
A3 = setupaircraft("A3", "AF", "F-80C", "A1-1515", "N", 10, 3.5, "CL")
A4 = setupaircraft("A4", "AF", "F-80C", "A1-1715", "N", 10, 4.0, "CL")
endtestsetup()

A1._assert("A1-1115       N    10", 2.5)
A2._assert("A1-1315       N    10", 3.0)
A3._assert("A1-1515       N    10", 3.5)
A4._assert("A1-1715       N    10", 4.0)

startgameturn()
A1.move("LVL", "N", "H,H")
A1._assert("A1-1113       N    10", 2.5)
A2.move("LVL", "N", "H,H,H")
A2._assert("A1-1312       N    10", 3.0)
A3.move("LVL", "N", "H,H,H")
A3._assert("A1-1512       N    10", 3.5)
A4.move("LVL", "N", "H,H,H,H")
A4._assert("A1-1711       N    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H,H,H")
A1._assert("A1-1110       N    10", 2.5)
A2.move("LVL", "N", "H,H,H")
A2._assert("A1-1309       N    10", 3.0)
A3.move("LVL", "N", "H,H,H,H")
A3._assert("A1-1508       N    10", 3.5)
A4.move("LVL", "N", "H,H,H,H")
A4._assert("A1-1707       N    10", 4.0)
endgameturn()

startgameturn()
A1.move("LVL", "N", "H,H")
A1._assert("A1-1108       N    10", 2.5)
A2.move("LVL", "N", "H,H,H")
A2._assert("A1-1306       N    10", 3.0)
A3.move("LVL", "N", "H,H,H")
A3._assert("A1-1505       N    10", 3.5)
A4.move("LVL", "N", "H,H,H,H")
A4._assert("A1-1703       N    10", 4.0)
endgameturn()

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1830", "N", 12, 1.5, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-2030", "N", 12, 2.0, "CL")
endtestsetup()

for i in range(1, 10, 2):
    startgameturn()
    A1.move("LVL", 0.0, "H")
    A2.move("LVL", 0.0, "H,H")
    endgameturn()
    startgameturn()
    A1.move("LVL", 0.0, "H,H")
    A2.move("LVL", 0.0, "H,H")
    endgameturn()

A1._assert("A1-1815       N    12", 1.5)
A2._assert("A1-2010       N    12", 2.0)

# HC and HD combinations.

starttestsetup()
A1 = setupaircraft("A1", "AF", "F-80C", "A1-1115", "N", 10, 4.0, "CL")
A2 = setupaircraft("A2", "AF", "F-80C", "A1-1315", "N", 10, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("SD", "N", "H,H,H,HD")
asserterror("'HD' is not a valid action when the flight type is SD.")
startgameturn()
A1.move("UD", "N", "H,H,H,HU")
A1._assert("A1-1111       N    10", 4.0)
startgameturn()
A1.move("LVL", "N", "H,H,H,HD")
A1._assert("A1-1111       N     9", 4.0)
startgameturn()
A1.move("LVL", "N", "H,H,H,HC")
asserterror("'HC' is not a valid move.")
startgameturn()
A1.move("ZC", "N", "H,H,H,HC")
asserterror("'HC' is not a valid move.")
startgameturn()
A1.move("SC", "N", "H,H,H,HC")
asserterror("'HC' is not a valid move.")
startgameturn()
A1.move("SC", "N", "H,H,H,H")
asserterror("too few VFPs.")
startgameturn()
A2.move("SD", "N", "H,H,H,H")
asserterror("too few VFPs.")
startgameturn()
A1.move("SC", "N", "H,H,H,C")
A1._assert("A1-1112       N    11", 4.0)
A2.move("SD", "N", "H,H,H,D")
A2._assert("A1-1312       N     9", 4.0)
endgameturn()

startgameturn()
A1.move("VC", "N", "H,HC,H,C2")
asserterror("'HC' is not a valid move.")
startgameturn()
A2.move("VD", "N", "H,HD2,H,D2")
asserterror("'HD2' is not a valid move.")
startgameturn()
A1.move("VC", "N", "H,C,C,C")
A1._assert("A1-1111       N    14", 3.0)
A2.move("VD", "N", "H,D2,D2,D2")
A2._assert("A1-1311       N     3", 5.5)
endgameturn()


endfile(__file__)
