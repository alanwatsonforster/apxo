from apxo.tests.infrastructure import *
startfile(__file__, "air-to-air attack elements")

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "Tu-4"   , "2023", "E", 5, 4.0, "CL")
A3 = aircraft("A3", "F-80C"  , "2025", "N", 5, 4.0, "CL", gunammunition=3.5)
A4 = aircraft("A4", "Tu-4"   , "2023", "E", 5, 4.0, "CL", gunammunition=11.0)
A5 = aircraft("A5", "F-89D"  , "2023", "E", 5, 4.0, "CL")
A6 = aircraft("A6", "F-102A" , "2023", "E", 5, 4.0, "CL", rocketfactors=0)
A7 = aircraft("A7", "F-100C" , "2025", "N", 5, 6.0, "CL")
endtestsetup()

startturn()

A1.move("LVL", "M", "TTR/H/AA(GN)(A2)(L)")
A2.react("AA(GN)(A1)(L)")
A1.continuemove("H/AA(GNSS)(A2)(M)")
A2.react("AA(GNSS)(A1)(L)")
A1.continuemove("H,H")
A2.move("LVL", "N", "H,H,H,H")

A1._assert("2021       N     5", 4.0)
A2._assert("2423       E     5", 3.5)
assert A1._gunammunition == 6.5
assert A2._gunammunition == 18.5

assert A3._gunammunition == 3.5
assert A4._gunammunition == 11.0

assert A5._rocketfactors == 9
A5.move("LVL", "M", "H/AA(RK3)(A2)()")
assert A5._rocketfactors == 6

assert A6._rocketfactors == 0

# Check recovery after ET.

startturn()
A7.move("LVL", "M", "ETR/H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H,H/AA(GN)()()")
asserterror("attempt to use weapons in or while recovering from an ET.")
startturn()
A7.move("LVL", "M", "ETR/HR,H,H,H,H/AA(GN)()()")
A7._assert("2221       NNE   5", 6.0)

# Check error if attack results are not specified at end of turn.
starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 4.0, "CL")
A2 = aircraft("A2", "Tu-4"   , "2024", "N", 5, 3.0, "CL")
endtestsetup()

startturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H,H/AA(GN)(A2)()")
endturn()
asserterror("aircraft A1 has 1 unspecified attack result.")

startturn()
A2.move("LVL", "FT", "H,H,H")
A1.move("LVL", "M", "H,H,H/AA(GN)(A2)(),H/AA(GN)(A2)()")
endturn()
asserterror("aircraft A1 has 2 unspecified attack results.")