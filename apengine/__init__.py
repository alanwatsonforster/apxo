import apengine.aircraft  as apaircraft
import apengine.azimuth   as apazimuth
import apengine.log       as aplog
import apengine.map       as apmap
import apengine.marker    as apmarker
import apengine.variants  as apvariants
import apengine.scenarios as apscenarios

################################################################################

# Turn is 0 between startsetup/endsetup, an integer greater than zero between
# startturn/endturn, and Null otherwise. It is incremented by endsetup/endturn.

_turn = None

# _savedturn holds the value of _turn outside of startsetup/endsetup and
# startturn/endturn.

_savedturn = None

def turn():
  return _turn

def _checkinstartuporturn():
  if _turn == None:
    raise RuntimeError("activity outside of setup or turn.")

def _checkinturn():
  if _turn == None or _turn == 0:
    raise RuntimeError("activity outside of turn.")

################################################################################

def startsetup(scenario, sheets=None, compassrose=None, north="up", variants=[]):

  global _turn, _savedturn

  _turn = 0
  _savedturn = _turn

  aplog.log("--- start prolog ---")
  aplog.logbreak()

  apvariants.setvariants(variants)
  aplog.logbreak()

  if scenario != None:
    sheets      = apscenarios.sheets(scenario)
    compassrose = apscenarios.compassrose(scenario)
    north       = apscenarios.north(scenario)

  apmap.setmap(sheets, compassrose)
  aplog.logbreak()

  apazimuth.setnorth(north)
  aplog.logbreak()

  apaircraft._startsetup()

def endsetup():

  global _turn, _savedturn

  apaircraft._endsetup()

  aplog.log("--- end prolog ---")
  aplog.logbreak()

  _turn += 1
  _savedturn = _turn
  _turn = None

################################################################################

def startturn():

  global _turn, _savedturn

  _turn = _savedturn

  if turn == None:
    aplog.error("startturn() called before endprolog().")

  aplog.log("--- start of turn %d ---" % _turn)
  aplog.logbreak()

  apaircraft._startturn()

def endturn():

  global _turn, _savedturn

  aplog.clearerror()
  try:

    apaircraft._endturn()

  except RuntimeError as e:
    aplog.logexception(e)

  aplog.log("--- end of turn %d ---" % _turn)
  aplog.logbreak()

  _turn += 1
  _savedturn = _turn
  _turn = None

################################################################################

def drawmap():
  apmap.startdrawmap()
  apaircraft._drawmap()
  apmarker._drawmap()
  apmap.enddrawmap()

################################################################################

from apengine.aircraft import aircraft
from apengine.marker   import marker