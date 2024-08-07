from apxo.tests.infrastructure import *

startfile(__file__, "gloc")

# GLOC Warning The check for a GLOC warning is not automated. However, the
# warnings can be seen by running the code with verbose=True.

starttestsetup(verbose=False)
A1 = aircraft("A1", "AF", "F-100A", "A1-1215", "N", 25, 6.5, "CL")
A2 = aircraft("A2", "AF", "F-100A", "A1-1415", "N", 25, 6.5, "CL")
A3 = aircraft("A3", "AF", "F-100A", "A1-1615", "N", 26, 6.5, "CL")
endtestsetup()

startgameturn()
A1.move("LVL", "AB", "ETR/HR,ETR/HR+,HR+,HR+,HR+,HR+")
A1._assert("A1-1615       S    25", 4.5)
A2.move("LVL", "AB", "BTR/H,HR+,H,HR+,H,HR+")
A2._assert("A1-1710       E    25", 6.0)
A3.move("LVL", "AB", "ETR/H,HR+,H,HR+,H,HR+")
A3._assert("A1-1910       E    26", 5.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "BTR/HR+,H/WL,H,H,H")
A1._assert("A2-1419       SSW  25", 4.0)
A2.move("LVL", "AB", "ETR/HR+,HR+,HR+,HR+,HR+,BTR/H")
A2._assert("A1-1714       WSW  25", 4.5)
A3.move("LVL", "AB", "BTR/H,H,HR+,H,H,HR+")
A3._assert("A1-2512       SSE  26", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "HTL/H,HL,HTL/H,H")
A1._assert("A2-1322       S    25", 4.0)
A2.move("LVL", "AB", "ETR/HRR+,HRR+,HRR+,HRR+,H/WL")
A2._assert("A1-1713       ESE  25", 2.0)
A3.move("LVL", "AB", "BTR/H,H,HR+,H")
A3._assert("A1-2616       S    26", 4.5)
endgameturn()

startgameturn()
A1.move("LVL", "AB", "HL+,H,HL+,H")
A1._assert("A2-1525       ESE  25", 4.0)
A2.move("ST", "AB", "")
A2._assert("A1-1713       ESE  23", 2.5)
A3.move("LVL", "AB", "BTR/H,H,HR+,H,H")
A3._assert("A2-2520       SSW  26", 4.5)
endgameturn()

endfile(__file__)
