import apxo.geometry as apgeometry

#############################################################################


def _attackaircraft(self, target, result=None):

   if not apgeometry.samehorizontalposition(self, target):
        raise RuntimeError("target not at the position of the blast zone.")
   if target.altitude() > self.altitude() + 2:
            raise RuntimeError("target is above blast zone.")
   self.logwhenwhat(
        "", "%s attacks %s with blast." % (self.name(), target.name())
   )

   target._takeattackdamage(self, result)


#############################################################################