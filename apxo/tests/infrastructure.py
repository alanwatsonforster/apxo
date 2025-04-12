import apxo as ap
import apxo.log as aplog

from apxo import aircraft, groundunit, drawmap

import os.path


def startfile(file, description):
    print("running tests in file %s: %s." % (os.path.basename(file), description))
    aplog.setprint(False)
    aplog.setwritefiles(False)


def endfile(file):
    aplog.setprint(True)
    aplog.setwritefiles(True)


def asserterror(error):
    if aplog._error != error:
        print("expected error: %r" % error)
        print("actual   error: %r" % aplog._error)
        assert aplog._error == error


def starttestsetup(
    sheets=[["A1"], ["A2"]],
    north="up",
    variants=[],
    verbose=False,
    **kwargs
):
    ap.startgamesetup(
        None,
        sheets=sheets,
        north=north,
        variants=variants,
        writelogfiles=False,
        printlog=verbose,
        **kwargs
    )


def endtestsetup():
    ap.endgamesetup()


def startgameturn():
    ap.startgameturn()


def endgameturn():
    ap.endgameturn()
