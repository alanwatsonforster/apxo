from apengine._tests.infrastructure import *
startfile(__file__, "ABSF aircraft")

from apengine._tests.infrastructure import *

# The F-89D has a different max speed with AB and M power.

starttestsetup()
A1 = aircraft("A1", "F-89D", "2030", "N", 30, 6.0, "CL", fuel="60%", bingofuel="40%")
A2 = aircraft("A2", "F-89D", "2030", "N", 30, 6.0, "CL", fuel="60%", bingofuel="40%")
endtestsetup()

startturn()
A1.move("LVL", "AB", "H,H,H,H,H,H")
A1._assert("2024       N    30", 6.0)
A2.move("LVL", "M" , "H,H,H,H,H,H")
A2._assert("2024       N    30", 5.5)
endturn()

endfile(__file__)