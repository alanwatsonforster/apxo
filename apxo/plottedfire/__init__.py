import apxo.altitude as apaltitude
import apxo.element as apelement
import apxo.log as aplog

##############################################################################


class plottedfire(apelement.element):

    ############################################################################

    def __init__(self, hexcode, altitude):

        self._name = ""

        self.logwhenwhat("", "creating plotted fire zone.")

        super().__init__(
            None,
            hexcode=hexcode,
            azimuth=None,
            altitude=altitude,
            speed=0,
        )

        self.logwhenwhat(
            "",
            "plotted fire zone centered on %s extending from altitude %d to %d."
            % (self.hexcode(), min(0, self.altitude() - 2), self.altitude() + 2)
        )

    ############################################################################

    from apxo.plottedfire.draw import _draw

    ############################################################################