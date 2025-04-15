################################################################################

import glass.airtoair
import glass.bomb
import glass.flight
import glass.geometry
import glass.log

################################################################################


def _attackaircraft(self, target, attacktype, result=None, returnfire=False, note=None):

    if not returnfire and glass.flight.useofweaponsforbidden(self):
        raise RuntimeError(
            "attempt to use weapons %s." % glass.flight.useofweaponsforbidden(self)
        )

    glass.airtoair.attack(self, attacktype, target, result, returnfire=returnfire)

    self.lognote(note)


################################################################################


def _attackgroundunit(self, target, attacktype, result=None, stores=None, note=None):

    def checkGNattack():

        self.logcomment(
            "relative altitude of attacker is %+d levels." % relativealtitude
        )
        if self.isinlevelflight():
            if relativealtitude > 1:
                raise RuntimeError("attacker too high.")
            if relativealtitude < 0:
                raise RuntimeError("attacker too low.")
        else:
            if relativealtitude < 0:
                raise RuntimeError("attacker too low.")

        self.logcomment("range is %d." % range)
        if range > 4:
            raise RuntimeError("attacker out of range.")

    def checkRKattack():

        self.logcomment(
            "release point is %d hexes and %+d levels."
            % (horizontalrange, relativealtitude)
        )
        if self.isinlevelflight():
            if horizontalrange > 10:
                raise RuntimeError("invalid release point.")
            minrelativealtitude = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            maxrelativealtitude = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        else:
            if horizontalrange == 0 or horizontalrange > 8:
                raise RuntimeError("invalid release point.")
            minrelativealtitude = [None, 0, 1, 2, 2, 3, 4, 4, 4]
            maxrelativealtitude = [None, 4, 8, 12, 10, 10, 9, 7, 5]
        if (
            relativealtitude < minrelativealtitude[horizontalrange]
            or relativealtitude > maxrelativealtitude[horizontalrange]
        ):
            raise RuntimeError("invalid release point.")

        self.logcomment("range is %d." % range)
        if range > 10:
            raise RuntimeError("attacker out of range.")

    def checkRPattack():
        checkRKattack()

    attacktype = attacktype.split("/")

    weapon = attacktype[0]
    if weapon not in ["GN", "RK", "RP"]:
        raise RuntimeError("invalid weapon.")

    if weapon == "GN":
        if stores is not None:
            raise RuntimeError("stores cannot be specified for GN attacks.")
        for s in attacktype[1:]:
            if s not in ["SS"]:
                raise RuntimeError("invalid attack type.")
        if "SS" in attacktype:
            if self._gunammunition < 0.5:
                raise RuntimeError("insuffient gun ammunition.")
            self._gunammunition -= 0.5
        else:
            if self._gunammunition < 1.0:
                raise RuntimeError("insuffient gun ammunition.")
            self._gunammunition -= 1.0
    else:
        if stores is None:
            raise RuntimeError("stores must be specified for %s attacks." % weapon)

    self.logwhenwhat("", "attacks %s with %s." % (target.name(), weapon))
    if not target.isgroundunit():
        raise RuntimeError("invalid target.")
    if target is not self._aimingtarget:
        raise RuntimeError("%s is not aiming at %s." % (self.name(), target.name()))

    if self.isinlevelflight():
        self.logcomment("level attack.")
    elif self.isindivingflight():
        self.logcomment("diving attack.")
    else:
        raise RuntimeError("attack in climbing flight.")

    range = glass.geometry.range(self, target)
    horizontalrange = glass.geometry.horizontalrange(self, target)
    relativealtitude = self.altitude() - target.altitude()

    if weapon == "GN":
        checkGNattack()
    elif weapon == "RK":
        checkRKattack()
    elif weapon == "RP":
        checkRPattack()

    if weapon == "GN":
        self.logwhenwhat("", "gun ammunition is now %.1f." % self._gunammunition)
    else:
        self._release(stores)
        self._stopaiming()

    target._takeattackdamage(self, result)

    self.lognote(note)


################################################################################


def _secondaryattackgroundunit(self, target, attacktype, result=None, note=None):

    attacktype = attacktype.split("/")

    weapon = attacktype[0]
    if weapon not in ["GN", "RK", "RP"]:
        raise RuntimeError("invalid weapon.")

    self.logwhenwhat("", "attacks %s with %s (secondary)." % (target.name(), weapon))

    target._takeattackdamage(self, result)

    self.lognote(note)


################################################################################


def bomb(self, name, target, stores=None, highdrag=False, note=None):

    try:

        self.logwhenwhat("", "bombs %s." % target.name())

        if not target.isgroundunit():
            raise RuntimeError("invalid target.")
        if target is not self._aimingtarget:
            raise RuntimeError("%s is not aiming at %s." % (self.name(), target.name()))

        if self.isinlevelflight():
            if highdrag:
                self.logcomment("level bombing with high-drag bombs.")
            else:
                self.logcomment("level bombing with low-drag bombs.")
        elif self.isindivingflight():
            if highdrag:
                self.logcomment("dive bombing with high-drag bombs.")
            else:
                self.logcomment("dive bombing with low-drag bombs.")
        else:
            raise RuntimeError("bomber is in climbing flight.")

        range = glass.geometry.range(self, target)
        horizontalrange = glass.geometry.horizontalrange(self, target)
        relativealtitude = self.altitude() - target.altitude()
        self.logcomment(
            "release point is %d hexes and %+d levels."
            % (horizontalrange, relativealtitude)
        )
        if self.isinlevelflight():
            if highdrag:
                if horizontalrange > 9:
                    raise RuntimeError("invalid release point.")
                minrelativealtitude = [0, 3, 7, 11, 15, 19, 25, 25, 33, 33]
                maxrelativealtitude = [2, 6, 10, 14, 18, 24, 32, 32, 40, 40]
            else:
                if horizontalrange == 0 or horizontalrange > 12:
                    raise RuntimeError("invalid release point.")
                minrelativealtitude = [None, 1, 3, 5, 7, 9, 11, 11, 16, 16, 26, 26, 26]
                maxrelativealtitude = [None, 2, 4, 6, 8, 10, 15, 15, 25, 25, 40, 40, 40]
        else:
            if highdrag:
                minrelativealtitude = [1, 4, 9, 14]
                maxrelativealtitude = [3, 8, 14, 20]
                if horizontalrange > 3:
                    raise RuntimeError("invalid release point.")
            else:
                minrelativealtitude = [1, 4, 7, 11, 13, 16]
                maxrelativealtitude = [3, 6, 10, 12, 15, 20]
                if horizontalrange > 5:
                    raise RuntimeError("invalid release point.")
        if (
            relativealtitude < minrelativealtitude[horizontalrange]
            or relativealtitude > maxrelativealtitude[horizontalrange]
        ):
            raise RuntimeError("invalid release point.")
        self.logcomment("release point is valid.")

        self._release(stores)
        bomb = glass.bomb.Bomb(name, self.hexcode(), self.facing(), self.altitude())
        self._stopaiming()
        self.lognote(note)
        return bomb

    except RuntimeError as e:
        glass.log.logexception(e)
    self.logbreak()


################################################################################
