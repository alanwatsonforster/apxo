import apxo.variants as apvariants

import os.path
import json
import re


def _checkconfiguration(configuration):
    assert configuration in ["CL", "1/2", "DT"]


def _checkpowersetting(powersetting):
    assert powersetting in ["AB", "M", "N", "I", "FT", "HT"]


def _checkturnrate(turnrate):
    assert turnrate in ["EZ", "TT", "HT", "BT", "ET"]


def _checkaltitudeband(altitudeband):
    assert altitudeband in ["LO", "ML", "MH", "HI", "VH", "EH", "UH"]


def _configurationindex(configuration):
    return ["CL", "1/2", "DT"].index(configuration)


class aircraftdata:

    def __init__(self, name):

        def loadfile(name):

            # TODO: Handle errors.

            filename = os.path.join(
                os.path.dirname(__file__), "aircraftdata", name + ".json"
            )
            with open(filename, "r", encoding="utf-8") as f:
                s = f.read(-1)
                # Strip whole-line // comments.
                r = re.compile("^[ \t]*//.*$", re.MULTILINE)
                s = re.sub(r, "", s)
                return json.loads(s)

        self._name = name

        data = loadfile(name)
        while "base" in data:
            base = data["base"]
            del data["base"]
            basedata = loadfile(base)
            basedata.update(data)
            data = basedata
        self._data = data

    def name(self):
        return self._data["name"]

    def crew(self):
        return self._data["crew"]

    def power(self, configuration, powersetting):
        _checkconfiguration(configuration)
        _checkpowersetting(powersetting)
        if not powersetting in self._data["powertable"]:
            return None
        elif powersetting == "I":
            if apvariants.withvariant("use first-edition ADCs"):
                return self._data["powertable"][powersetting][
                    _configurationindex(configuration)
                ]
            else:
                return (
                    self._data["powertable"][powersetting][
                        _configurationindex(configuration)
                    ]
                    * 2
                )
        else:
            return self._data["powertable"][powersetting][
                _configurationindex(configuration)
            ]

    def powerfade(self, speed, altitude):
        if (
            not "powerfadespeedtable" in self._data
            and not "poweraltitudefadetable" in self._data
        ):
            return None
        fadespeed = 0
        fadealtitude = 0
        if "powerfadespeedtable" in self._data:
            for p in self._data["powerfadespeedtable"]:
                if speed > p[0]:
                    fadespeed = p[1]
        if "poweraltitudefadetable" in self._data:
            for p in self._data["poweraltitudefadetable"]:
                if altitude > p[0]:
                    fadealtitude = p[1]
        return fadespeed + fadealtitude

    def speedbrake(self, configuration):
        _checkconfiguration(configuration)
        raw = self._data["powertable"]["SPBR"][_configurationindex(configuration)]
        if raw == "-":
            return None
        elif apvariants.withvariant("use first-edition ADCs"):
            return raw
        else:
            return raw * 2.0

    def fuelrate(self, powersetting):
        _checkpowersetting(powersetting)
        if not powersetting in self._data["powertable"]:
            return None
        else:
            return self._data["powertable"][powersetting][3]

    def internalfuelcapacity(self):
        if not "internalfuel" in self._data:
            raise RuntimeError(
                "the internal fuel capacity is not specified for this aircraft type."
            )
        return self._data["internalfuel"]

    def engines(self):
        return self._data["engines"]

    def lowspeedliftdeviceselectable(self):
        if "lowspeedliftdeviceselectable" in self._data:
            return self._data["lowspeedliftdeviceselectable"]
        else:
            return False

    def lowspeedliftdevicelimittype(self):
        if "lowspeedliftdevicelimittype" in self._data:
            return self._data["lowspeedliftdevicelimittype"]
        else:
            return None

    def lowspeedliftdevicelimit(self):
        if "lowspeedliftdevicelimit" in self._data:
            return self._data["lowspeedliftdevicelimit"]
        else:
            return None

    def lowspeedliftdevicename(self):
        if "lowspeedliftdevicename" in self._data:
            return self._data["lowspeedliftdevicename"]
        else:
            return None

    def turndrag(self, configuration, turnrate, lowspeedliftdevice=False):
        _checkconfiguration(configuration)
        _checkturnrate(turnrate)
        if lowspeedliftdevice:
            table = "lowspeedliftdeviceturndragtable"
        else:
            table = "turndragtable"
        if not turnrate in self._data[table]:
            return None
        raw = self._data[table][turnrate][_configurationindex(configuration)]
        if raw == "-":
            return None
        else:
            return raw

    def minspeed(self, configuration, altitudeband):
        _checkconfiguration(configuration)
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        raw = self._data["speedtable"][altitudeband][
            _configurationindex(configuration)
        ][0]
        if raw == "-":
            return None
        else:
            return raw

    def maxspeed(self, configuration, altitudeband):
        _checkconfiguration(configuration)
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        raw = self._data["speedtable"][altitudeband][
            _configurationindex(configuration)
        ][1]
        if raw == "-":
            return None
        else:
            return raw

    def maxdivespeed(self, altitudeband):
        _checkaltitudeband(altitudeband)
        if altitudeband == "UH":
            altitudeband = "EH"
        raw = self._data["speedtable"][altitudeband][3]
        if raw == "-":
            return None
        else:
            return raw

    def ceiling(self, configuration):
        _checkconfiguration(configuration)
        return self._data["ceilingtable"][_configurationindex(configuration)]

    def cruisespeed(self, configuration):
        basecruisespeed = self._data["cruisespeed"]
        if configuration == "CL":
            return basecruisespeed
        elif configuration == "1/2":
            return basecruisespeed - 0.5
        else:
            return basecruisespeed - 1.0

    def climbspeed(self):
        return self._data["climbspeed"]

    def sizemodifier(self):
        return self._data["sizemodifier"]

    def vulnerability(self):
        return self._data["vulnerability"]

    def visibility(self):
        return self._data["visibility"]

    def blindarcs(self):
        if self._data["blindarcs"] == "":
            return []
        else:
            return self._data["blindarcs"].split("/")

    def restrictedarcs(self):
        if self._data["restrictedarcs"] == "":
            return []
        else:
            return self._data["restrictedarcs"].split("/")

    def visibility(self):
        return self._data["visibility"]

    def atarefuel(self):
        return self._data["atarefuel"]

    def ejectionseat(self):
        return self._data["ejectionseat"]

    def rollhfp(self):
        raw = self._data["maneuvertable"]["LR/DR"][0]
        if raw == "-":
            return None
        else:
            return raw

    def rolldrag(self, rolltype):
        assert rolltype in ["VR", "LR", "DR"]
        if rolltype != "VR":
            rolltype = "LR/DR"
        raw = self._data["maneuvertable"][rolltype][1]
        if raw == "-":
            return None
        else:
            return raw

    def properties(self):
        return set(self._data["properties"])

    def hasproperty(self, p):
        return p in self.properties()

    def climbcapability(self, configuration, altitudeband, powersetting):
        _checkaltitudeband(altitudeband)
        _checkpowersetting(powersetting)
        if altitudeband == "UH":
            altitudeband = "EH"
        if powersetting == "AB":
            powersettingindex = 0
        else:
            powersettingindex = 1
        raw = self._data["climbcapabilitytable"][altitudeband][
            _configurationindex(configuration)
        ][powersettingindex]
        if raw == "-":
            return None
        else:
            return raw

    def specialclimbcapability(self):
        if "specialclimbcapability" in self._data:
            return self._data["specialclimbcapability"]
        else:
            return 1

    def radar(self, what=None):
        if "radar" not in self._data or self._data["radar"] is False:
            return None
        elif what is None:
            return True
        else:
            return self._data["radar"][what]

    def gun(self):
        if "gun" in self._data and self._data["gun"] != "":
            return self._data["gun"]
        else:
            return None

    def gunarc(self):
        if "gunarc" in self._data:
            return self._data["gunarc"]
        else:
            return None

    def gunammunition(self):
        if "gunammunition" in self._data:
            return self._data["gunammunition"]
        else:
            return 0

    def gunsightmodifier(self, turnrate):
        if "gunsightmodifiers" not in self._data:
            return None
        elif turnrate not in self._data["gunsightmodifiers"]:
            return None
        else:
            return self._data["gunsightmodifiers"][turnrate]

    def gunatatohitroll(self, range):
        if "gunatatohitrolls" in self._data:
            tohitroll = self._data["gunatatohitrolls"].split("/")[range]
            if tohitroll == "-":
                tohitroll = None
            else:
                tohitroll = int(tohitroll)
            return tohitroll
        else:
            return None

    def ataradarrangingtype(self):
        if "ataradarranging" not in self._data:
            return None
        elif self._data["ataradarranging"] == "-":
            return None
        else:
            assert self._data["ataradarranging"] in ["RE", "CA", "IG"]
            return self._data["ataradarranging"]

    def gunatadamagerating(self):
        if "gundamagerating" in self._data:
            return int(self._data["gundamagerating"].split("/")[0])
        else:
            return None

    def gunatgdamagerating(self):
        if "gundamagerating" in self._data:
            return self._data["gundamagerating"].split("/")[1]
        else:
            return None

    def lockon(self):
        if "lockon" not in self._data:
            return None
        elif self._data["lockon"] == "-":
            return None
        else:
            return self._data["lockon"]

    def bombsystem(self):
        if "bombsystem" in self._data:
            return self._data["bombsystem"]
        else:
            return "Manual"

    def ecm(self, what):
        if "ecm" not in self._data or self._data["ecm"] is False:
            return None
        elif what not in self._data["ecm"]:
            return None
        else:
            return self._data["ecm"][what]

    def technology(self):
        if (
            "technology" not in self._data
            or self._data["technology"] is False
            or len(self._data["technology"]) == 0
        ):
            return None
        else:
            return self._data["technology"]

    def ABSFamount(self):
        if "ABSF" in self.properties():
            return self._data["ABSFamount"]
        else:
            return None

    def NDRHSlimit(self):
        if "NDRHS" in self.properties():
            return self._data["NDRHSlimit"]
        else:
            return None

    def NLRHSlimit(self):
        if "NLRHS" in self.properties():
            return self._data["NLRHSlimit"]
        else:
            return None

    def rocketfactors(self):
        if "rocketfactors" in self._data:
            return self._data["rocketfactors"]
        else:
            return 0

    def hasstoreslimits(self):
        """
        Return True if the aircraft data has a stores limit configured.
        """
        return "storeslimits" in self._data

    def storeslimit(self, configuration):
        """
        Return the stores limit for the given configuration. If
        configuration is "CL" or "1/2", return the load point limit. If
        configuration is "DT", return the weight limit.
        """

        assert configuration in ["CL", "1/2", "DT"]
        assert self.hasstoreslimits()

        if configuration == "CL":
            return self._data["storeslimits"][0]
        elif configuration == "1/2":
            return self._data["storeslimits"][1]
        elif configuration == "DT":
            return self._data["storeslimits"][2]

    def wikiurl(self):
        if "wikiurl" in self._data:
            return self._data["wikiurl"]
        else:
            return None

    def variantnotes(self):
        if "variantnotes" in self._data:
            return self._data["variantnotes"]
        else:
            return []

    def notes(self):
        if "notes" in self._data:
            return self._data["notes"]
        else:
            return []

    ##############################################################################

    def __str__(self):
        """
        Return a string representation of an aircraft data object. The format
        follows that of the Aircraft Data Cards in TSOH.
        """

        global _result
        _result = ""

        def str(s):
            global _result
            _result += s + "\n"

        def f1(x):
            if x == None:
                return "---"
            else:
                return "%.1f" % x

        def f2(x):
            if x == None:
                return "----"
            else:
                return "%.2f" % x

        def f1z(x):
            if x == 0:
                return "---"
            else:
                return "%.1f" % x

        def f0(x):
            if x == None:
                return "--"
            else:
                return "%2.0f" % x

        str("Type: %s" % self._name)
        str("")

        str("Crew           : %d %s" % (len(self.crew()), ", ".join(self.crew())))
        str("Ejection Seat  : %s" % self.ejectionseat())

        if not self.hasproperty("SPFL"):

            str("Power:")
            str("")
            str("       CL    1/2   DT    Fuel")
            if self.power("CL", "M") != None:
                str(
                    "AB     %-4s  %-4s  %-4s  %-4s"
                    % (
                        f1(self.power("CL", "AB")),
                        f1(self.power("1/2", "AB")),
                        f1(self.power("DT", "AB")),
                        f1(self.fuelrate("AB")),
                    )
                )
            if self.power("CL", "M") != None:
                str(
                    "M      %-4s  %-4s  %-4s  %-4s"
                    % (
                        f1(self.power("CL", "M")),
                        f1(self.power("1/2", "M")),
                        f1(self.power("DT", "M")),
                        f1(self.fuelrate("M")),
                    )
                )
            if self.power("CL", "FT") != None:
                str(
                    "FT     %-4s  %-4s  %-4s  %-4s"
                    % (
                        f2(self.power("CL", "FT")),
                        f2(self.power("1/2", "FT")),
                        f2(self.power("DT", "FT")),
                        f1(self.fuelrate("FT")),
                    )
                )
            if self.power("CL", "HT") != None:
                str(
                    "HT     %-4s  %-4s  %-4s  %-4s"
                    % (
                        f2(self.power("CL", "HT")),
                        f2(self.power("1/2", "HT")),
                        f2(self.power("DT", "HT")),
                        f1(self.fuelrate("HT")),
                    )
                )
            str(
                "N      %-4s  %-4s  %-4s  %-4s"
                % (
                    f1(self.power("CL", "N")),
                    f1(self.power("1/2", "N")),
                    f1(self.power("DT", "N")),
                    f1(self.fuelrate("N")),
                )
            )
            str(
                "I      %-4s  %-4s  %-4s  %-4s"
                % (
                    f1(self.power("CL", "I")),
                    f1(self.power("1/2", "I")),
                    f1(self.power("DT", "I")),
                    f1(self.fuelrate("I")),
                )
            )
            str(
                "SPBR   %-4s  %-4s  %-4s"
                % (
                    f1(self.speedbrake("CL")),
                    f1(self.speedbrake("1/2")),
                    f1(self.speedbrake("DT")),
                )
            )
            str("")

            if (
                "powerfadespeedtable" in self._data
                or "poweraltitudefadetable" in self._data
            ):
                if "powerfadespeedtable" in self._data:
                    for p in self._data["powerfadespeedtable"]:
                        str(
                            "- If the speed is more than %.1f, the power is reduced by %s."
                            % (p[0], p[1])
                        )
                if "poweraltitudefadetable" in self._data:
                    for p in self._data["poweraltitudefadetable"]:
                        str(
                            "- If the altitude is more than %d, the power is reduced by %s."
                            % (p[0], p[1])
                        )
                str("")

            str("Engines        : %d" % self.engines())
            str("Cruise Speed   : %.1f" % self.cruisespeed("CL"))
            str("Climb  Speed   : %.1f" % self.climbspeed())
            str("Visibility     : %d" % self.visibility())
            str("Size Modifier  : %+d" % self.sizemodifier())
            str("Vulnerability  : %+d" % self.vulnerability())
            str("Restricted arcs: %s" % (" ".join(self.restrictedarcs())))
            str("Blind arcs     : %s" % (" ".join(self.blindarcs())))
            str("Internal Fuel  : %.1f" % self.internalfuelcapacity())
            str("ATA Refuel     : %s" % self.atarefuel())
            str("")

            str("Roll Costs:")
            str("")
            str("LR/DR  %s  %s" % (f1(self.rollhfp()), f1(self.rolldrag("LR"))))
            str("VR     %s  %s" % (f1(None), f1(self.rolldrag("VR"))))
            str("")

            str("Turn Drag:")
            str("")
            if self.lowspeedliftdevicelimit() != None:
                str(
                    "Low-speed lift device           : %s"
                    % self.lowspeedliftdevicename()
                )
                str(
                    "Low-speed lift device limit     : %.1f"
                    % self.lowspeedliftdevicelimit()
                )
                str(
                    "Low-speed lift device selectable: %r"
                    % self.lowspeedliftdeviceselectable()
                )
                str("")
                if self.lowspeedliftdeviceselectable():
                    str(
                        "For speed <= %.1f and selected."
                        % self.lowspeedliftdevicelimit()
                    )
                else:
                    str("For speed <= %.1f." % self.lowspeedliftdevicelimit())
                str("       CL   1/2  DT")
                for turnrate in ["TT", "HT", "BT", "ET"]:
                    str(
                        "%s     %s  %s  %s"
                        % (
                            turnrate,
                            f1(self.turndrag("CL", turnrate, lowspeedliftdevice=True)),
                            f1(self.turndrag("1/2", turnrate, lowspeedliftdevice=True)),
                            f1(self.turndrag("DT", turnrate, lowspeedliftdevice=True)),
                        )
                    )
                str("")
                if self.lowspeedliftdeviceselectable():
                    str(
                        "For speed > %.1f or not selected."
                        % self.lowspeedliftdevicelimit()
                    )
                else:
                    str("For speed > %.1f." % self.lowspeedliftdevicelimit())
                str("       CL   1/2  DT")
                for turnrate in ["TT", "HT", "BT", "ET"]:
                    str(
                        "%s     %s  %s  %s"
                        % (
                            turnrate,
                            f1(self.turndrag("CL", turnrate)),
                            f1(self.turndrag("1/2", turnrate)),
                            f1(self.turndrag("DT", turnrate)),
                        )
                    )
            else:
                str("       CL   1/2  DT")
                for turnrate in ["TT", "HT", "BT", "ET"]:
                    str(
                        "%s     %s  %s  %s"
                        % (
                            turnrate,
                            f1(self.turndrag("CL", turnrate)),
                            f1(self.turndrag("1/2", turnrate)),
                            f1(self.turndrag("DT", turnrate)),
                        )
                    )
            str("")

            str("Speed and Ceiling:")
            str("")
            str("      CL       1/2      DT")
            str(
                "      %s       %s       %s"
                % (
                    f0(self.ceiling("CL")),
                    f0(self.ceiling("1/2")),
                    f0(self.ceiling("DT")),
                )
            )
            for band in ["EH", "VH", "HI", "MH", "ML", "LO"]:
                str(
                    "%s    %s-%s  %s-%s  %s-%s  %s"
                    % (
                        band,
                        f1(self.minspeed("CL", band)),
                        f1(self.maxspeed("CL", band)),
                        f1(self.minspeed("1/2", band)),
                        f1(self.maxspeed("1/2", band)),
                        f1(self.minspeed("DT", band)),
                        f1(self.maxspeed("DT", band)),
                        f1(self.maxdivespeed(band)),
                    )
                )
            str("")

            str("Climb Capability:")
            str("")
            str("      CL         1/2        DT")
            for band in ["EH", "VH", "HI", "MH", "ML", "LO"]:
                str(
                    "%s    %s %s  %s %s  %s %s"
                    % (
                        band,
                        f2(self.climbcapability("CL", band, "AB")),
                        f2(self.climbcapability("CL", band, "M")),
                        f2(self.climbcapability("1/2", band, "AB")),
                        f2(self.climbcapability("1/2", band, "M")),
                        f2(self.climbcapability("DT", band, "AB")),
                        f2(self.climbcapability("DT", band, "M")),
                    )
                )
            str("")

        if self.gun() != None:
            str("Gun: %s" % self.gun())
            str("Gun ammunition: %.1f" % self._data["gunammunition"])
            str(
                "ATA To-Hit: %d %d %r"
                % (
                    self.gunatatohitroll(0),
                    self.gunatatohitroll(1),
                    self.gunatatohitroll(2),
                )
            )
            if "gunarc" in self._data:
                str("Gun arc: %s" % self._data["gunarc"])

        if "rocketfactors" in self._data:
            str("Rocket factors: %.0f" % self._data["rocketfactors"])

        if "gunammunition" in self._data or "rocketfactors" in self._data:
            str("Gunsight modifiers: ")
            for turnrate in ["TT", "HT", "BT"]:
                if self.gunsightmodifier(turnrate) is not None:
                    str("  %s %+d" % (turnrate, self.gunsightmodifier(turnrate)))
        if self.ataradarrangingtype() is not None:
            str("ATA Radar-ranging: %s" % self.ataradarrangingtype())
        if self.lockon() is not None:
            str("ATA Lock-On: %d" % self.lockon())

        str("")

        s = ""
        for p in self._data["properties"]:
            s += " %s" % p
        str("Properties:%s" % s)
        str("")
        str("Origin: %s" % self._data["origin"])
        str("")
        str("Notes:")
        str("")

        if self.hasproperty("LRRHS"):
            str("- LRRHS: LRR if speed is %.1f or more." % self._data["LRRHSlimit"])

        if self.hasproperty("HRRCL"):
            str("- HRRCL: HRR when CL.")

        if self.hasproperty("ABSF"):
            str(
                "- Maximum speed is reduced by %.1f unless AB is used."
                % self._data["ABSFamount"]
            )

        if "variantnotes" in self._data:
            for note in self._data["variantnotes"]:
                str("- %s" % note)

        if "notes" in self._data:
            for note in self._data["notes"]:
                str("- %s" % note)

        return _result


##############################################################################
