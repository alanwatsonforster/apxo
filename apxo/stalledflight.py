"""
Stalled flight for aircraft.
"""

import math
import re

import apxo.altitude      as apaltitude
import apxo.capabilities  as apcapabilities
import apxo.configuration as apconfiguration
import apxo.stores        as apstores

def checkflight(A):

  if apcapabilities.hasproperty(A, "SPFL"):
    raise RuntimeError("special-flight aircraft cannot perform stalled flight.")

  # See rule 6.3.

  if A._speed >= apcapabilities.minspeed(A):
      raise RuntimeError("flight type cannot be ST as aircraft is not stalled.")

  A._logstart("speed is below the minimum of %.1f." % apcapabilities.minspeed(A))
  A._logstart("aircraft is stalled.")

def doflight(A, action, note=False):

  """
  Carry out stalled flight.
  """

  def dojettison(m):

    # See rule 4.4.   
    # We implement the delay of 1 FP by making this an other element.
    
    previousconfiguration = A._configuration

    for released in m[1].split("+"):
      A._stores = apstores._release(A._stores, released,
        printer=lambda s: A._logevent(s)
      )

    apconfiguration.update(A)

    if A._configuration != previousconfiguration:
      A._logevent("configuration changed from %s to %s." % (
        previousconfiguration, A._configuration
      ))
  
  # See rule 6.4.
      
  A._logevent("is carrying %+.2f APs." % A._apcarry)

  A._logposition("start")   

  altitudechange = math.ceil(A._speed + A._turnsstalled)

  initialaltitude = A._altitude    
  initialaltitudeband = A._altitudeband
  A._altitude, A._altitudecarry = apaltitude.adjustaltitude(A._altitude, A._altitudecarry, -altitudechange)
  A._altitudeband = apaltitude.altitudeband(A._altitude)
  altitudechange = initialaltitude - A._altitude
    
  if A._turnsstalled == 0:
    A._altitudeap = 0.5 * altitudechange
  else:
    A._altitudeap = 1.0 * altitudechange

  A._lognote(note)

  A._logposition("end")

  if initialaltitudeband != A._altitudeband:
    A._logevent("altitude band changed from %s to %s." % (initialaltitudeband, A._altitudeband))

  A.checkforterraincollision()
  if A._destroyed:
    return

  # The only valid actions are to do nothing or to jettison stores.

  fullaction = action
  while action != "":
    m = re.compile(r"J\(([^)]*)\)").match(action)
    if not m:
      raise RuntimeError("invalid action %r for stalled flight." % fullaction)
    dojettison(m)  
    action = action[len(m.group()):]


  A._logline()
