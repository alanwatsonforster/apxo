import apxo.aircraft
import apxo.capabilities
import apxo.geometry
import apxo.hex
import apxo.log
import apxo.rounding
import apxo.variants

##############################################################################


def gunattackrange(attacker, target, arc=False):
    """
    Return the range of an air-to-air gun attack from the attacker on the target
    or the reason the attack is forbidden.
    """

    # See rule 9.1 and the Air-to-Air Gun Attack diagram in the sheets.

    def horizontalrange(x0, y0, facing0, x1, y1, facing1):

        angleofftail, angleoffnose, r, dx, dy = apxo.geometry.relativepositions(
            x0, y0, facing0, x1, y1, facing1
        )

        if dx < 0:
            return False
        elif dx == 0:
            if dy == 0:
                return 0
            else:
                return False
        elif dx <= 1.0:
            if dy == 0:
                return 1
            else:
                return False
        elif dx < 1.5:
            if abs(dy) <= 0.5:
                return 1
            else:
                return False
        elif dx <= 2.2:
            if abs(dy) <= 0.5:
                return 2
            else:
                return False
        else:
            return False

    def verticalrange():
        return int(abs(attacker.altitude() - target.altitude()) / 2)

    if arc:

        rmin = False
        for facing in range(0, 361, 30):
            r = horizontalrange(
                attacker.x(),
                attacker.y(),
                facing,
                target.x(),
                target.y(),
                target.facing(),
            )
            if rmin is False:
                rmin = r
            elif r is not False:
                rmin = min(r, rmin)
        r = rmin

        if r is False:
            return "the target is not in the weapon range or arc."

        angleoff = apxo.geometry.angleofftail(target, attacker)
        if arc == "30-":
            allowedangleoff = ["0 line", "30 arc"]
        elif arc == "60-":
            allowedangleoff = ["0 line", "30 arc", "60 arc"]
        elif arc == "90-":
            allowedangleoff = ["0 line", "30 arc", "60 arc", "90 arc"]
        elif arc == "120-":
            allowedangleoff = ["0 line", "30 arc", "60 arc", "90 arc", "120 arc"]
        elif arc == "150-":
            allowedangleoff = [
                "0 line",
                "30 arc",
                "60 arc",
                "90 arc",
                "120 arc",
                "150 arc",
            ]
        elif arc == "180-":
            allowedangleoff = [
                "0 line",
                "30 arc",
                "60 arc",
                "90 arc",
                "120 arc",
                "150 arc",
                "180 arc",
                "180 line",
            ]
        else:
            raise RuntimeError("invalid arc %r." % arc)

        if not angleoff in allowedangleoff:
            return "the target is not in the weapon range or arc."

        r += verticalrange()
        if r > 2:
            return "the target is not in the weapon range or arc."
        else:
            return r

    else:

        # Apply the relative altitude restrictions for climbing, diving, and level flight.
        if attacker.isinclimbingflight() and attacker.altitude() > target.altitude():
            return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
        if attacker.isindivingflight() and attacker.altitude() < target.altitude():
            return (
                "aircraft in diving flight cannot fire on aircraft at higher altitudes."
            )
        if attacker.isinlevelflight():
            if (
                issamehexattack(attacker, target)
                and attacker.altitude() != target.altitude()
            ):
                return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."
            elif abs(attacker.altitude() - target.altitude()) > 1:
                return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."

        r = horizontalrange(
            attacker.x(),
            attacker.y(),
            attacker.facing(),
            target.x(),
            target.y(),
            target.facing(),
        )

        if r is False:
            return "the target is not in the arc or range of the weapon."

        r += verticalrange()
        if r > 2:
            return "the target is not in the arc or range of the weapon."
        else:
            return r


##############################################################################


def issamehexattack(attacker, target):
    """
    Return true if the attacker and target are in the same hex.
    """

    return (attacker.x() == target.x()) and (attacker.y() == target.y())


##############################################################################


def rocketattackrange(attacker, target):
    """
    Return the range of an air-to-air rocket attack from the attacker on the target
    or the reason the attack is forbidden.
    """

    # See rule 9.3.

    def verticalrange():
        return int(abs(attacker.altitude() - target.altitude()) / 2)

    # Apply the relative altitude restrictions for climbing, diving, and level flight.
    if attacker.isinclimbingflight() and attacker.altitude() > target.altitude():
        return "aircraft in climbing flight cannot fire on aircraft at lower altitudes."
    if attacker.isindivingflight() and attacker.altitude() < target.altitude():
        return "aircraft in diving flight cannot fire on aircraft at higher altitudes."
    if attacker.isinlevelflight():
        if abs(attacker.altitude() - target.altitude()) > 1:
            return "aircraft in level flight cannot fire on aircraft with more than 1 level of difference in altitude."
        if (
            issamehexattack(attacker, target)
            and attacker.altitude() != target.altitude()
        ):
            return "aircraft in level flight cannot fire at range 0 on aircraft at a different altitude."

    if not apxo.geometry.inradararc(attacker, target, "limited"):
        return "the target is not in the arc or range of the weapon."

    r = apxo.geometry.horizontalrange(attacker, target)

    r += verticalrange()
    if r == 0 or r > 4:
        return "the target is not in the arc or range of the weapon."
    else:
        return r


##############################################################################


def _attack(attacker, attacktype, target, result, allowRK=True, allowtracking=True):
    """
    Attack and aircraft with fixed guns, articulated guns, or rockets.
    """

    if attacker._ETrecoveryfp > 0:
        raise RuntimeError("attempt to use weapons in or while recovering from an ET.")

    if target is None:
        targetdescription = ""
    else:
        targetdescription = " on %s" % target.name()

    weapon = attacktype[:2]
    attackmodifiers = attacktype[2:]

    snapshot = False
    radarranging = False
    collisioncourse = False
    rocketfactors = None

    while attackmodifiers != "":
        if weapon == "GN" and attackmodifiers[:3] == "/SS":
            snapshot = True
            attackmodifiers = attackmodifiers[3:]
        elif attackmodifiers[:3] == "/RR":
            radarranging = True
            attackmodifiers = attackmodifiers[3:]
        elif weapon == "RK" and attackmodifiers[:3] == "/CC":
            collisioncourse = True
            attackmodifiers = attackmodifiers[3:]
        elif (
            weapon == "RK"
            and attackmodifiers[0] == "/"
            and len(attackmodifiers) >= 2
            and attackmodifiers[1].isdecimal()
        ):
            attackmodifiers = attackmodifiers[1:]
            rocketfactors = 0
            while attackmodifiers != "" and attackmodifiers[0].isdecimal():
                rocketfactors *= 10
                rocketfactors += int(attackmodifiers[0])
                attackmodifiers = attackmodifiers[1:]
        else:
            raise RuntimeError("invalid attack type %r" % attacktype)

    if weapon == "GN":

        if snapshot:
            attacker.logcomment(
                "snap-shot gun air-to-air attack%s." % targetdescription
            )
            if attacker._gunammunition < 0.5:
                raise RuntimeError(
                    "available gun ammunition is %.1f." % attacker._gunammunition
                )
        else:
            attacker.logcomment("gun air-to-air attack%s." % targetdescription)
            if attacker._gunammunition < 1.0:
                raise RuntimeError(
                    "available gun ammunition is %.1f." % attacker._gunammunition
                )

    elif allowRK and weapon == "RK":

        if rocketfactors is None:
            raise RuntimeError("number of rocket factors not specified.")
        attacker.logcomment(
            "rocket air-to-air attack with %d factors%s."
            % (rocketfactors, targetdescription)
        )
        if attacker._rocketfactors < rocketfactors:
            raise RuntimeError(
                "available rocket factors are %d." % attacker._rocketfactors
            )

    else:

        raise RuntimeError("invalid weapon %r." % weapon)

    if snapshot:
        snapshotmodifier = +1
    else:
        snapshotmodifier = None

    if target is None:

        sizemodifier = None
        verticalmodifier = None
        angleofftailmodifier = None
        r = None

    else:

        if weapon == "GN":
            if apxo.capabilities.gunarc(attacker) != None:
                attacker.logcomment(
                    "gunnery arc is %s." % apxo.capabilities.gunarc(attacker)
                )
            r = gunattackrange(attacker, target, arc=apxo.capabilities.gunarc(attacker))
        else:
            r = rocketattackrange(attacker, target)
        if isinstance(r, str):
            raise RuntimeError(r)
        attacker.logcomment("range is %d." % r)

        angleofftail = apxo.geometry.angleofftail(attacker, target)
        attacker.logcomment("angle-off-tail is %s." % angleofftail)
        if angleofftail == "0 line":
            angleofftailmodifier = -2
        elif angleofftail == "30 arc":
            angleofftailmodifier = +0
        elif angleofftail == "60 arc":
            angleofftailmodifier = +2
        elif (
            angleofftail == "90 arc"
            or angleofftail == "120 arc"
            or angleofftail == "150 arc"
        ):
            angleofftailmodifier = +4
        elif angleofftail == "180 arc":
            angleofftailmodifier = +3
        elif angleofftail == "180 line":
            angleofftailmodifier = +2

        if (
            angleofftail != "0 line"
            and angleofftail != "30 arc"
            and angleofftail != "60 arc"
        ):
            allowSSGT = False

        verticalmodifier = None
        if (weapon == "GN" or weapon == "GNSS") and issamehexattack(attacker, target):
            # See rule 9.2 with errata. Note that the rules do not give a vertical
            # modifier for an attacker in level flight with a target in climbing or
            # diving flight.
            if attacker.isinclimbingflight():
                if target.isinclimbingflight():
                    verticalmodifier = +0
                elif target.isinlevelflight():
                    verticalmodifier = +1
                else:
                    verticalmodifier = +2
            elif attacker.isindivingflight():
                if target.isinclimbingflight():
                    verticalmodifier = +2
                elif target.isinlevelflight():
                    verticalmodifier = +1
                else:
                    verticalmodifier = +0
            elif (
                apxo.variants.withvariant("use house rules") and attacker.isinlevelflight()
            ):
                if target.isinclimbingflight():
                    verticalmodifier = +1
                elif target.isindivingflight():
                    verticalmodifier = +1

        sizemodifier = apxo.capabilities.sizemodifier(target)

    if allowtracking:
        attacker.logcomment(
            "SSGT for %d %s."
            % (attacker._trackingfp, apxo.log.plural(attacker._trackingfp, "FP", "FPs"))
        )
        if attacker._trackingfp >= 2 * apxo.rounding.rounddown(
            apxo.rounding.onethirdfromtable(attacker.speed())
        ):
            trackingmodifier = -2
        elif attacker._trackingfp >= 1 * apxo.rounding.rounddown(
            apxo.rounding.onethirdfromtable(attacker.speed())
        ):
            trackingmodifier = -1
        else:
            trackingmodifier = -0
    else:
        attacker.logcomment("SSGT not allowed.")
        trackingmodifier = None

    radarrangingtype = apxo.capabilities.ataradarrangingtype(attacker)
    if radarrangingtype is None:
        attacker.logcomment("attacker does not have radar ranging.")
        if radarranging:
            raise RuntimeError("attacker does not have radar ranging.")
    elif radarrangingtype == "RE" and attacker._trackingfp == 0:
        attacker.logcomment("RE radar-ranging requires SSGT.")
        if radarranging:
            raise RuntimeError("RE radar-ranging requires SSGT.")
    else:
        attacker.logcomment(
            "%s radar-ranging lock-on roll is %d."
            % (radarrangingtype, apxo.capabilities.lockon(attacker))
        )
    if radarranging:
        attacker.logcomment("%s radar-ranging succeeded." % radarrangingtype)
        if radarrangingtype == "RE":
            radarrangingmodifier = -1
        elif radarrangingtype == "CA":
            radarrangingmodifier = -2
        elif radarrangingtype == "IG":
            radarrangingmodifier = -3
    else:
        radarrangingmodifier = None

    collisioncoursemodifier = None
    if collisioncourse:
        attacker.logcomment("collision-course attack.")
        collisioncoursemodifier = -2

    if attacker._BTrecoveryfp > 0:
        attacker.logcomment("applicable turn rate is BT.")
        turnratemodifier = apxo.capabilities.gunsightmodifier(attacker, "BT")
    elif attacker._rollrecoveryfp > 0:
        attacker.logcomment("applicable turn rate is BT (for a roll).")
        turnratemodifier = apxo.capabilities.gunsightmodifier(attacker, "BT")
    elif attacker._HTrecoveryfp > 0:
        attacker.logcomment("applicable turn rate is HT.")
        turnratemodifier = apxo.capabilities.gunsightmodifier(attacker, "HT")
    elif attacker._TTrecoveryfp > 0:
        attacker.logcomment("applicable turn rate is TT.")
        turnratemodifier = apxo.capabilities.gunsightmodifier(attacker, "TT")
    else:
        attacker.logcomment("no applicable turn rate.")
        turnratemodifier = None

    if weapon == "RK":
        # See rule 9.3; attacker damage does not modify rocket attacks.
        damagemodifier = None
    elif attacker.damageatleast("C"):
        damagemodifier = +3
    elif attacker.damageatleast("H"):
        damagemodifier = +2
    elif attacker.damageatleast("L"):
        damagemodifier = +1
    else:
        damagemodifier = None

    tohitmodifier = 0
    if snapshotmodifier is not None:
        attacker.logcomment("snap-shot          modifier is %+d." % snapshotmodifier)
        tohitmodifier += snapshotmodifier
    if sizemodifier is not None:
        attacker.logcomment("target size        modifier is %+d." % sizemodifier)
        tohitmodifier += sizemodifier
    if verticalmodifier is not None:
        attacker.logcomment("same-hex vertical  modifier is %+d." % verticalmodifier)
        tohitmodifier += verticalmodifier
    if angleofftailmodifier is not None:
        attacker.logcomment(
            "angle-off-tail     modifier is %+d." % angleofftailmodifier
        )
        tohitmodifier += angleofftailmodifier
    if trackingmodifier is not None:
        attacker.logcomment("SSGT               modifier is %+d." % trackingmodifier)
        tohitmodifier += trackingmodifier
    if radarrangingmodifier is not None:
        attacker.logcomment(
            "radar-ranging      modifier is %+d." % radarrangingmodifier
        )
        tohitmodifier += radarrangingmodifier
    if collisioncoursemodifier is not None:
        attacker.logcomment(
            "collision-course   modifier is %+d." % collisioncoursemodifier
        )
        tohitmodifier += collisioncoursemodifier
    if turnratemodifier is not None:
        attacker.logcomment("attacker turn-rate modifier is %+d." % turnratemodifier)
        tohitmodifier += turnratemodifier
    if damagemodifier is not None:
        attacker.logcomment("attacker damage    modifier is %+d." % damagemodifier)
        tohitmodifier += damagemodifier
    attacker.logcomment("total to-hit       modifier is %+d." % tohitmodifier)

    if r is not None:
        if weapon == "GN":
            tohitroll = apxo.capabilities.gunatatohitroll(attacker, r)
            attacker.logcomment("to-hit roll is %d." % tohitroll)

    if (result != "A") and (result != "M") and (target is not None):
        if weapon == "GN":
            damagerating = apxo.capabilities.gunatadamagerating(attacker)
            damageratingmodifier = 0
            if snapshot:
                attacker.logcomment("snap-shot damage modifier is -1.")
                damageratingmodifier -= 1
            if target.damageatleast("L"):
                attacker.logcomment("target    damage modifier is -1.")
                damageratingmodifier += 1
            attacker.logcomment(
                "damage rating is %d + %+d = %d."
                % (
                    damagerating,
                    damageratingmodifier,
                    damagerating + damageratingmodifier,
                )
            )
            attacker.logcomment(
                "target vulnerability is %+d." % apxo.capabilities.vulnerability(target)
            )

    target._takeattackdamage(attacker, result)

    if result != "A":
        if weapon == "GN":
            if snapshot:
                attacker._gunammunition -= 0.5
            else:
                attacker._gunammunition -= 1.0
        else:
            attacker._rocketfactors -= rocketfactors

    if weapon == "GN":
        attacker.logcomment("%.1f gun ammunition remain." % attacker._gunammunition)
    else:
        attacker.logcomment(
            "%d rocket %s."
            % (
                attacker._rocketfactors,
                apxo.log.plural(
                    attacker._rocketfactors, "factor remains", "factors remain"
                ),
            )
        )


##############################################################################


def attack(attacker, attacktype, target, result, returnfire=False):
    """
    Attack an aircraft, with fixed guns, articulated guns, or rockets.
    """

    if returnfire:
        _attack(
            attacker, attacktype, target, result, allowtracking=False, allowRK=False
        )
    else:
        _attack(attacker, attacktype, target, result)


##############################################################################


def trackingforbidden(attacker, target):
    """
    Check that the attacker can carry out SSGT on the target.
    """

    # The check on the ability to use weapons (necessary for tracking) is
    # carried out elsewhere.

    if not apxo.geometry.horizontalrange(attacker, target) <= 6:
        return "%s is more than 6 hexes from %s." % (target.name(), attacker.name())
    if not apxo.geometry.inarc(target, attacker, "60-"):
        return "%s is not in its 60- arc of %s." % (attacker.name(), target.name())
    if apxo.geometry.horizontalrange(attacker, target) > 0 and not apxo.geometry.inarc(
        attacker, target, "limited"
    ):
        return "%s is not in the limited arc of %s." % (target.name(), attacker.name())
    if apxo.variants.withvariant("require limited radar arc for SSGT"):
        if apxo.geometry.horizontalrange(
            attacker, target
        ) > 0 and not apxo.geometry.inradararc(attacker, target, "limited"):
            return "%s is not in the limited radar arc of %s." % (
                target.name(),
                attacker.name(),
            )

    return False
