from glass.tests.infrastructure import *

startfile(__file__, "attacks after rolls")

# Attacks after Rolls

starttestsetup(verbose=False)
A1 = setupaircraft("A1", "AF", "F-80C", 2015, "N", 20, 4.0, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "M", "DRR/H,HR,H,H")
A1._assert("A1-2111       N    20", 4.0)
A1.move("LVL", "M", "DRR/H,HR,H/AGN,H")
asserterror("attempt to use weapons on the FP immediately after rolling.")
A1.move("HRD/VD", "M", "H,D2,D2,D2/AGN")
asserterror("attempt to use weapons during the turn after an HRD.")
A1.move("HRD/VD", "M", "H,D2,D2,D2")
A1._assert("A1-2014       N    14", 5.5)
endgameturn()

startgameturn()
A1.move("VD", "M", "D2,D2,VRR/D2/R,D2/AGN,D2")
asserterror("attempt to use weapons on the FP immediately after rolling.")
A1.move("VD", "M", "D2,D2,VRR/D2/R,D2,D2")
A1._assert("A1-2014       NNE   4", 6.5)
endgameturn()

endfile(__file__)
