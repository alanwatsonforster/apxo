import glass.altitude
import glass.speed
import glass.variants


def power(A, powersetting):
    return A._aircraftdata.power(A._configuration, powersetting)


def speedbrake(A):
    return A._aircraftdata.speedbrake(A._configuration)


def fuelrate(A):
    return A._aircraftdata.fuelrate(A._powersetting)


def engines(A):
    return A._aircraftdata.engines()


def powerfade(A):
    return A._aircraftdata.powerfade(A.speed(), A.altitude())


def lowspeedliftdevicename(A):
    return A._aircraftdata.lowspeedliftdevicename()


def lowspeedliftdevicelimit(A):
    """
    Return the maximum speed at which the low-speed lift devices operate.
    """
    if A._aircraftdata.lowspeedliftdevicelimittype() is None:
        return None
    elif A._aircraftdata.lowspeedliftdevicelimittype() == "absolute":
        return A._aircraftdata.lowspeedliftdevicelimit()
    else:
        return A._aircraftdata.lowspeedliftdevicelimit() + rawminspeed(A)


def lowspeedliftdeviceselectable(A):
    return A._aircraftdata.lowspeedliftdeviceselectable()


def turndrag(A, turnrate):

    def rawturndrag(turnrate):
        lowspeedliftdevicelimit = A._aircraftdata.lowspeedliftdevicelimit()
        if lowspeedliftdevicelimit == None:
            return A._aircraftdata.turndrag(A._configuration, A._geometry, turnrate)
        elif A._lowspeedliftdeviceextended:
            return A._aircraftdata.turndrag(
                A._configuration, A._geometry, turnrate, lowspeedliftdevice=True
            )
        else:
            return A._aircraftdata.turndrag(A._configuration, A._geometry, turnrate)

    # See rule 6.6
    if A.hasproperty("PSSM") and A.speed() >= glass.speed.m1speed(A.altitudeband()):
        # The aircraft has its maximum the turn rate reduced by one level, but not
        # to less than HT.
        if turnrate == "ET":
            return None
        if turnrate == "BT" and rawturndrag("ET") == None:
            return None

    if turnrate == "EZ":
        return 0.0
    elif rawturndrag(turnrate) == None:
        return None
    else:
        return rawturndrag(turnrate)


def rawminspeed(A):

    minspeed = A._aircraftdata.minspeed(A._configuration, A._geometry, A.altitudeband())

    if minspeed == None:
        # The aircraft is temporarily above its ceiling, so take the speed from the
        # highest band in the table.
        for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
            minspeed = A._aircraftdata.minspeed(
                A._configuration, A._geometry, altitudeband
            )
            if minspeed != None:
                break

    return minspeed


def minspeed(A):

    if A.hasproperty("SPFL"):
        return 0.0

    minspeed = rawminspeed(A)

    # See rule 7.6 in version 2.4.
    if (
        A._lowspeedliftdeviceextended
        and A._aircraftdata.lowspeedliftdeviceminspeedchange() is not None
    ):
        minspeed -= A._aircraftdata.lowspeedliftdeviceminspeedchange()

    return minspeed


def maxspeed(A):

    maxspeed = A._aircraftdata.maxspeed(A._configuration, A._geometry, A.altitudeband())

    if maxspeed == None:
        # The aircraft is temporarily above its ceiling, so take the speed from the
        # highest band in the table.
        for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
            maxspeed = A._aircraftdata.maxspeed(
                A._configuration, A._geometry, altitudeband
            )
            if maxspeed != None:
                break

    if A.hasproperty("ABSF"):
        if A._powersetting != "AB":
            maxspeed -= A._aircraftdata.ABSFamount(A._geometry)

    return maxspeed


def cruisespeed(A):
    return A._aircraftdata.cruisespeed(A._configuration)


def climbspeed(A):
    return A._aircraftdata.climbspeed()


def blindarcs(A):
    return A._aircraftdata.blindarcs()


def restrictedarcs(A):
    return A._aircraftdata.restrictedarcs()


def visibility(A):
    return A._aircraftdata.visibility()


def sizemodifier(A):
    return A._aircraftdata.sizemodifier()


def vulnerability(A):
    return A._aircraftdata.vulnerability()


def maxdivespeed(A):
    raw = A._aircraftdata.maxdivespeed(A.altitudeband())
    if raw != None:
        return raw
    # The aircraft is temporarily above its ceiling, so take the speed from the
    # highest band in the table.
    for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
        raw = A._aircraftdata.maxdivespeed(altitudeband)
        if raw != None:
            return raw


def ceiling(A):
    return A._aircraftdata.ceiling(A._configuration)


def rollhfp(A):
    # See rule 7.4.
    fp = A._aircraftdata.rollhfp()
    if A.hasproperty("LRR"):
        fp += 1
    return fp


def rolldrag(A, rolltype):
    return A._aircraftdata.rolldrag(rolltype)


def climbcapability(A):
    climbcapability = A._aircraftdata.climbcapability(
        A._configuration, A.altitudeband(), A._powersetting
    )
    if climbcapability == None:
        # The aircraft is temporarily above its ceiling, so take the speed from the
        # highest band in the table.
        for altitudeband in ["UH", "EH", "VH", "HI", "MH", "ML", "LO"]:
            climbcapability = A._aircraftdata.climbcapability(
                A._configuration, altitudeband, A._powersetting
            )
            if climbcapability != None:
                break
    return climbcapability


def specialclimbcapability(A):
    return A._aircraftdata.specialclimbcapability()


def gunatatohitroll(A, range):
    return A._aircraftdata.gunatatohitroll(range)


def gunatadamagerating(A):
    return A._aircraftdata.gunatadamagerating()


def gunarc(A):
    return A._aircraftdata.gunarc()


def gunsightmodifier(A, turnrate):
    return A._aircraftdata.gunsightmodifier(turnrate)


def ataradarrangingtype(A):
    return A._aircraftdata.ataradarrangingtype()


def lockon(A):
    return A._aircraftdata.radar("lockon")


def bombsystem(A):
    return A._aircraftdata.bombsystem()


def geometries(A):
    return A._aircraftdata.geometries()


def properties(A):
    return A._aircraftdata.properties(A._geometry)
