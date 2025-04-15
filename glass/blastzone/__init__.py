import apxo.altitude
import apxo.element
import apxo.log

##############################################################################


class Blastzone(apxo.element.Element):

    ############################################################################

    def __init__(self, name, x, y):

        self._name = ""

        if not isinstance(name, str):
            raise RuntimeError("the name argument must be a string.")

        self.logwhenwhat("", "creating blast zone %s." % name)

        super().__init__(
            name,
            x=x,
            y=y,
            azimuth=None,
            altitude=apxo.altitude.terrainaltitude(x, y) + 2,
            speed=0,
        )

        self.logwhenwhat(
            "",
            "blast zone in %s extends to altitude %d."
            % (self.hexcode(), self.altitude()),
        )

    #############################################################################

    def isblastzone(self):
        return True

    #############################################################################

    def _endgameturn(self):
        self._remove()

    ############################################################################

    from apxo.blastzone.attack import _attackaircraft
    from apxo.blastzone.draw import _draw

    ############################################################################
