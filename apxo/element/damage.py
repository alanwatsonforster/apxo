################################################################################

import apxo.log

################################################################################

# These procedures can be implemented in subclasses that take damage.


def _initdamage(self):
    pass


def _damage(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _damageatleast(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _damageatmost(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _takedamage(self):
    raise RuntimeError("%s cannot take damage." % self.name())


def _takedamageconsequences(self):
    pass


def _isssupressed(self):
    raise RuntimeError("%s cannot be suppresed." % self.name())


################################################################################


def damage(self):
    return self._damage()


def damageatleast(self, damage):
    return self._damageatleast(damage)


def damageatmost(self, damage):
    return self._damageatmost(damage)


def takedamage(self, damage, note=None):
    try:
        self.logwhenwhat("", "takes %s damage." % damage)
        if self.killed():
            self.logwhenwhat("", "is already killed.")
            return
        previousdamage = self.damage()
        if previousdamage == "":
            previousdamage = "none"
        self._takedamage(damage)
        if previousdamage == self.damage():
            self.logwhenwhat("", "damage is unchanged at %s." % previousdamage)
        else:
            self.logwhenwhat(
                "",
                "damage changes from %s to %s." % (previousdamage, self.damage()),
            )
            if self.damage() == "K":
                self._kill()
                self.logwhenwhat("", "is killed.")
            else:
                self._takedamageconsequences()
        self.lognote(note)
    except RuntimeError as e:
        apxo.log.logexception(e)
    self.logbreak()


def issuppressed(self):
    return self._issuppressed()


################################################################################


def _takeattackdamage(self, attacker, result):
    """
    Take damage from an attack.
    """
    if result is None:
        attacker.logcomment("unspecified result.")
        attacker._unspecifiedattackresult += 1
    elif result == "A":
        attacker.logwhenwhat("", "aborts.")
    elif result == "M":
        attacker.logwhenwhat("", "misses.")
    elif result == "-":
        if self.isaircraft():
            attacker.logwhenwhat("", "hits but inflicts no damage.")
        else:
            attacker.logwhenwhat("", "inflicts no damage.")
    else:
        if self.isaircraft():
            attacker.logwhenwhat("", "hits and inflicts %s damage." % result)
        else:
            attacker.logwhenwhat("", "inflicts %s damage." % result)
        self.logwhenwhat("", "takes %s damage." % result)
        if self.killed():
            self.logwhenwhat("", "%s is already killed." % self.name())
            return
        previousdamage = self.damage()
        if previousdamage == "":
            previousdamage = "none"
        self._takedamage(result)
        if previousdamage == self.damage():
            self.logwhenwhat("", "damage is unchanged at %s." % previousdamage)
        else:
            self.logwhenwhat(
                "",
                "damage changes from %s to %s." % (previousdamage, self.damage()),
            )
            if self.damage() == "K":
                self._kill()
                self.logwhenwhat("", "is killed.")
            self._takedamageconsequences()


################################################################################
