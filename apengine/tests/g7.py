from apengine.tests.infrastructure import *
startfile(__file__, "attacks after rolls")

# Attacks after Rolls

startsetup(verbose=False)
A1 = aircraft("A1", "F-80C", 2015, "N", 20, 4.0, "CL")
endsetup()

startturn()
A1.move("LVL"   ,  "M", "DRR/H,HR,H,H"    )
A1._assert("2111       N    20",  4.0)
A1.move("LVL"   ,  "M", "DRR/H,HR,H/AGN,H")
asserterror("attempt to use weapons on the FP immediately after rolling.")
A1.move("VD/HRD",  "M", "H,D2,D2,D2/AGN"  )
asserterror("attempt to use weapons during the turn after an HRD.")
A1.move("VD/HRD",  "M", "H,D2,D2,D2"      )
A1._assert("2014       N    14",  5.5)
endturn()

startturn()
A1.move("VD"    ,  "M", "D2,D2,VRR/D2/R,D2/AGN,D2")
asserterror("attempt to use weapons on the FP immediately after rolling.")
A1.move("VD"    ,  "M", "D2,D2,VRR/D2/R,D2,D2"    )
A1._assert("2014       NNE   4",  6.5)
endturn()

endfile(__file__)