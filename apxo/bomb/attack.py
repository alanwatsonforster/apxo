################################################################################

import apxo.blastzone as apblastzone
import apxo.geometry as apgeometry
import apxo.log as aplog

################################################################################


def _attackgroundunit(self, target, result=None, blastzone=True):

    self.logwhenwhat("", "attacks %s." % target.name())
    if not apgeometry.samehorizontalposition(self, target):
        raise RuntimeError("the bombs are not at the position of the target.")

    target._takeattackdamage(self, result)

    self._remove()


################################################################################


def _secondaryattackgroundunit(self, target, result=None):

    self.logwhenwhat("", "attacks %s (secondary)." % target.name())

    target._takeattackdamage(self, result)


################################################################################


def blastzone(self, name, note=None):

    try:
        blastzone = apblastzone.blastzone(name, *self.xy())
        aplog.lognote(note)
    except RuntimeError as e:
        aplog.logexception(e)
    self.logbreak()
    return blastzone


################################################################################
