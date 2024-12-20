################################################################################

def _damage(self):
    if self._damagelevel == 0:
        if self.issuppressed():
            return "S"
        else:
            return ""
    elif self._damagelevel == 1:
        if self.issuppressed():
            return "D+S"
        else:
            return "D"
    elif self._damagelevel == 2:
        if self.issuppressed():
            return "2D+S"
        else:
            return "2D"
    else:
        return "K"

def _takedamage(self, damage):
    self._suppressionlevel = 2
    if damage == "S":
        pass
    elif damage == "D":
        self._damagelevel += 1
    elif damage == "2D":
        self._damagelevel += 2
    elif damage == "K":
        self._damagelevel += 3
    else:
        raise RuntimeError("invalid damage %r" % damage)

def _takedamageconsequences(self):
    if self.isusingbarragefire():
        self.logwhenwhat("", "%s ceases barrage fire." % self.name())
        self._barragefiremarker._remove()
        self._barragefiremarker = None

################################################################################
