from apengine._tests.infrastructure import *
startfile(__file__, "damage effects")

# Turn rate.

starttestsetup()
A1 = aircraft("A1", "F-100C"  , "2025", "N", 5, 5.0, "CL")
endtestsetup()
startturn()
A1.move("LVL", "M", "HBKR,ETR/H,H,H,H")
A1._assert("2020       N     5", 4.5)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-100C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
endtestsetup()
startturn()
A1.move("LVL", "M", "HBKR,ETR/H,H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
startturn()
A1.move("LVL", "M", "HBKR,BTR/H,H,H,H")
A1._assert("2020       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-100C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
endtestsetup()
startturn()
A1.move("LVL", "M", "HBKR,BTR/H,H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
startturn()
A1.move("LVL", "M", "HBKR,HTR/H,H,H,H")
A1._assert("2020       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-100C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
endtestsetup()
startturn()
A1.move("LVL", "M", "HBKR,BTR/H,H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
startturn()
A1.move("LVL", "M", "HBKR,HTR/H,H,H,H")
A1._assert("2020       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-100C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
endtestsetup()
startturn()
A1.move("LVL", "M", "HBKR,HTR/H,H,H,H")
asserterror("attempt to declare a turn rate tighter than allowed by the damage, speed, or flight type.")
startturn()
A1.move("LVL", "M", "HBKR,TTR/H,H,H,H")
A1._assert("2020       N     5", 5.0)
endturn()

# HPR

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
assert A1.hasproperty("HPR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
assert not A1.hasproperty("HPR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
assert not A1.hasproperty("HPR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
assert not A1.hasproperty("HPR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
assert not A1.hasproperty("HPR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F7U-3"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("K")
assert not A1.hasproperty("HPR")
endtestsetup()

# HRR and LRR

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
assert A1.hasproperty("HRR")
assert not A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-5A"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("K")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
assert not A1.hasproperty("HRR")
assert not A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("K")
assert not A1.hasproperty("HRR")
assert A1.hasproperty("LRR")
endtestsetup()

# NRM

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
assert not A1.hasproperty("NRM")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
assert not A1.hasproperty("NRM")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
assert not A1.hasproperty("NRM")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
assert A1.hasproperty("NRM")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
assert A1.hasproperty("NRM")
endtestsetup()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("K")
assert A1.hasproperty("NRM")
endtestsetup()

# Preparatory FPs.

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
endtestsetup()
startturn()
A1.move("LVL", "M", "SLL/H,HL,H,H,H")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startturn()
A1.move("LVL", "M", "SLL/H,H,HL,H,H")
A1._assert("1920       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("L")
endtestsetup()
startturn()
A1.move("LVL", "M", "SLL/H,HL,H,H,H")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startturn()
A1.move("LVL", "M", "SLL/H,H,HL,H,H")
A1._assert("1920       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("2L")
endtestsetup()
startturn()
A1.move("LVL", "M", "SLL/H,H,HL,H,H")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startturn()
A1.move("LVL", "M", "SLL/H,H,H,HL,H")
A1._assert("1920       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("H")
endtestsetup()
startturn()
A1.move("LVL", "M", "SLL/H,H,HL,H,H")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startturn()
A1.move("LVL", "M", "SLL/H,H,H,HL,H")
A1._assert("1920       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-80C"  , "2025", "N", 5, 5.0, "CL")
A1.takedamage("C")
endtestsetup()
startturn()
A1.move("LVL", "M", "SLL/H,H,HL,H,H")
asserterror("attempt to slide without sufficient preparatory HFPs.")
startturn()
A1.move("LVL", "M", "SLL/H,H,H,HL,H")
A1._assert("1920       N     5", 5.0)
endturn()

# Power

starttestsetup()
A1 = aircraft("A1", "F-104A"  , "2030", "N", 5, 5.0, "CL")
endtestsetup()
startturn()
A1.move("UD", "AB", "H,H,H,H,HD")
A1._assert("2025       N     4", 6.0)
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
A1._assert("2025       N     5", 5.5)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-104A"  , "2030", "N", 5, 5.0, "CL")
A1.takedamage("L")
endtestsetup()
startturn()
A1.move("UD", "AB", "H,H,H,H,HD")
A1._assert("2025       N     4", 6.0)
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
A1._assert("2025       N     5", 5.5)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-104A"  , "2030", "N", 5, 5.0, "CL")
A1.takedamage("2L")
endtestsetup()
startturn()
A1.move("UD", "AB", "H,H,H,H,HD")
A1._assert("2025       N     4", 6.0)
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
A1._assert("2025       N     5", 5.5)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-104A"  , "2030", "N", 5, 5.0, "CL")
A1.takedamage("H")
endtestsetup()
startturn()
A1.move("UD", "AB", "H,H,H,H,HD")
A1._assert("2025       N     4", 5.5)
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
A1._assert("2025       N     5", 5.0)
endturn()

starttestsetup()
A1 = aircraft("A1", "F-104A"  , "2030", "N", 5, 5.0, "CL")
A1.takedamage("C")
endtestsetup()
startturn()
A1.move("UD", "AB", "H,H,H,H,HD")
asserterror("aircraft does not have an AB power setting.")
startturn()
A1.move("LVL", "M", "H,H,H,H,H")
A1._assert("2025       N     5", 5.0)
endturn()

endfile(__file__)