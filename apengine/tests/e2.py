from apengine.tests.infrastructure import *
startfile(__file__, "dives")

# Dives

# Steep Dives

startsetup()
A1 = aircraft("A1", "F-80C", 1815, "N"  , 20, 3.0, "CL")
endsetup()

startturn()
A1.move("SD",  "N", "H,H,H")
A1._assert("1812       N    20",  3.0)
A1.move("SD",  "N", "H,D,H")
A1._assert("1813       N    19",  3.0)
A1.move("SD",  "N", "H,D,D")
A1._assert("1814       N    18",  3.0)
A1.move("SD",  "N", "H,D3,D3")
asserterror("attempt to dive 3 levels per VFP while the flight type is SC.")
A1.move("SD",  "N", "H,D2,D2")
A1._assert("1814       N    16",  3.5)
endturn()

startturn()
A1.move("SD",  "N", "D,D,D")
asserterror("too few HFPs.")
A1.move("SD",  "N", "H,D2,H")
A1._assert("1812       N    14",  4.0)
A1.move("SD",  "N", "H,D2,D2")
A1._assert("1813       N    12",  4.5)
endturn()

startturn()
A1.move("SD",  "M", "BTR/H,H,H,H,HR")
A1._assert("1808       NNE  12",  4.5)
endturn()

# Unloaded Dives

startsetup()
A1 = aircraft("A1", "F-80C", 1815, "N"  , 20, 3.0, "CL")
endsetup()

startturn()
A1.move("UD",  "M", "HD,H,HD")
asserterror("unloaded HFPs must be continuous.")
A1.move("UD",  "N", "H,H,H")
asserterror("too few unloaded HFPs.")
A1.move("UD",  "N", "H,HD,H")
A1._assert("1812       N    19",  3.0)
endturn()

startturn()
A1.move("UD",  "N", "HD,HD,HD")
A1._assert("1809       N    16",  3.5)
endturn()

startturn()
A1.move("VD",  "N", "H,D2,D2")
A1._assert("1808       N    12",  4.5)
endturn()

startturn()
A1.move("UD",  "N", "H,H,H,H,H")
asserterror("too few unloaded HFPs.")
A1.move("UD",  "N", "HD,H,H,H,H")
asserterror("too few unloaded HFPs.")
A1.move("UD",  "N", "TTR/HD,HDR,H,H,H")
asserterror("attempt to turn faster than the declared turn rate.")
A1.move("UD",  "N", "TTR/H,HR,H,HD,HD")
A1._assert("1903/2004  NNE  10",  4.5)
A1.move("UD",  "N", "HD,HD,H,H,H")
A1._assert("1803       N    10",  4.5)
endturn()

# Verify that attacks cannot happen on unloaded FPs.

startsetup(verbose=False)
A1 = aircraft("A1", "F-80C", 2015, "N", 20, 4.0, "CL")
endsetup()

startturn()
A1.move("UD"    ,  "M", "HD,HD,HD,HD/AGN" )
asserterror("attempt to use weapons while unloaded.")
A1.move("UD"    ,  "M", "HD,HD,HD,HD"     )
A1._assert("2011       N    16",  4.5)
endturn()

# Vertical Dives

startsetup(sheets=[["A1"],["A2"]])
A1 = aircraft("A1", "F-80C", 1820, "N"  , 17, 5.0, "CL")
endsetup()

startturn()
A1.move("SD",  "N", "H,H,H,H,H")
A1._assert("1815       N    17",  5.0)
endturn()

startturn()
A1.move("VD",  "M", "H,D3,D3,D3,D3")
asserterror("too few HFPs.")
A1.move("VD",  "M", "H,H,H,D3,D3")
asserterror("too many HFPs.")
A1.move("VD",  "M", "H,H,D1,D3,D3")
asserterror("attempt to dive 1 levels per VFP while the flight type is VD.")
A1.move("VD",  "M", "H,H,D1,D3,D3")
asserterror("attempt to dive 1 levels per VFP while the flight type is VD.")
A1.move("VD",  "M", "H,H,D2,D2,D2")
A1._assert("1813       N    11",  6.5)
endturn()

startturn()
A1.move("VC",  "M", "D2,D2,D2,D2,D2,D2")
asserterror("flight type immediately after VD cannot be VC.")
A1.move("SC",  "M", "D2,D2,D2,D2,D2,D2")
asserterror("flight type immediately after VD cannot be SC.")
A1.move("ZC",  "M", "D2,D2,D2,D2,D2,D2")
asserterror("flight type immediately after VD cannot be ZC.")
A1.move("LVL",  "M", "D2,D2,D2,D2,D2,D2")
asserterror("flight type immediately after VD cannot be LVL.")
A1.move("SD",  "M", "H,H,H,H,D,D")
asserterror("too few VFPs.")
A1.move("SD",  "M", "H,H,H,D,D,D")
A1._assert("1810       N     8",  6.5)
A1.move("SD",  "M", "H,H,D,D,D,D")
A1._assert("1811       N     7",  6.5)
A1.move("SD",  "M", "H,D,D,D,D,D")
asserterror("too few HFPs.")
A1.move("UD",  "M", "H,H,H,H,HD,HD")
asserterror("too few unloaded HFPs.")
A1.move("UD",  "M", "H,H,H,HD,HD,HD")
A1._assert("1807       N     8",  6.5)
A1.move("UD",  "M", "HD,HD,HD,HD,HD,HD")
A1._assert("1807       N     5",  6.5)
endturn()

startsetup(sheets=[["A1"],["A2"]])
A1 = aircraft("A1", "F-80C", 1817, "N"  , 45, 2.5, "CL")
endsetup()

startturn()
A1.move("SD",  "N", "H,H")
A1._assert("1815       N    45",  2.5)
endturn()

startturn()
A1.move("VD",  "M", "H,D2,D2")
A1._assert("1814       N    41",  3.5)
endturn()

startturn()
A1.move("VD",  "M", "D3,D3,D3")
A1._assert("1814       N    32",  6.0)
endturn()

startturn()
A1.move("VD",  "M", "D3,D3,D3,D3,D3,D3")
A1._assert("1814       N    14",  6.5)
endturn()

# Free Descent

startsetup()
A1 = aircraft("A1", "F-80C", 1815, "N"  , 10, 4.0, "CL")
endsetup()

startturn()
A1.move("LVL",  "M", "HD2,H,H,H")
asserterror("attempt to descend 2 levels while flight type is LVL.")
A1.move("LVL",  "M", "HD,H,H,HD")
asserterror("free descent cannot only be taken once per move.")
A1.move("LVL",  "M", "H,H,H,HD")
A1._assert("1811       N     9",  4.0)
endturn()

startturn()
A1.move("LVL",  "M", "HD,H,H,H")
A1._assert("1807       N     8",  4.5)
endturn()

endfile(__file__)