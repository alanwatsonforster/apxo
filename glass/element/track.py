################################################################################

import glass.hexcode
import glass.log

################################################################################


def _inittracking(self):
    self._tracking = None


################################################################################


def _track(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot track." % self.name())


def _stoptracking(self, target, *args, **kwargs):
    raise RuntimeError("%s cannot track." % self.name())


################################################################################


def track(self, target, *args, **kwargs):
    try:
        if not target.isaircraft():
            raise RuntimeError("invalid target for tracking.")
        self._track(target, *args, **kwargs)
        self._tracking = target
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################


def stoptracking(self):
    try:
        if self._tracking is None:
            raise RuntimeError("%s is not tracking" % self.name())
        self._stoptracking()
    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
