from builtins import str
from builtins import range
import os,sys
sys.path.append('..')
import conf as cfg
from mupif import *
import mupif
import time as timeTime


tunnel = None
#use numerical IP values only (not names, sometimes they do not work)
try:#tunnel must be closed at the end, otherwise bound socket may persist on system
    tunnel = PyroUtil.sshTunnel(cfg.server, cfg.serverUserName, cfg.serverNatport, cfg.serverPort, cfg.sshClient, cfg.options)

    time  = 0
    dt    = 1
    expectedValue = 4.5

    start = timeTime.time()
    #locate nameserver
    ns = PyroUtil.connectNameServer(cfg.nshost, cfg.nsport, cfg.hkey)

    # locate remote PingServer application, request remote proxy
    serverApp = PyroUtil.connectApp(ns, cfg.appName)

    try:
        appsig=serverApp.getApplicationSignature()
        mupif.log.debug("Working application on server " + appsig)
    except Exception as e:
        mupif.log.error("Connection to server failed, exiting")
        mupif.log.exception(e)
        sys.exit(1)

    mupif.log.info("Generating test sequence ...")

    for i in range (10):
        time = i
        timestepnumber = i
        # create a time step
        istep = TimeStep.TimeStep(time, dt, timestepnumber)
        try:
            serverApp.setProperty (Property.Property(i, PropertyID.PID_Concentration, ValueType.Scalar, i, None, 0))
            serverApp.solveStep(istep)

        except APIError.APIError as e:
            mupif.log.exception("Following API error occurred:" + e)
            break

    mupif.log.debug("Done")
    prop = serverApp.getProperty(PropertyID.PID_CumulativeConcentration, i)
    mupif.log.debug("Received " + str(prop.getValue()) + " expected " + str(expectedValue) )
    if (prop.getValue() == expectedValue):
        mupif.log.info("Test PASSED")
    else:
        mupif.log.error("Test FAILED")
        sys.exit(1)

    serverApp.terminate();
    mupif.log.debug("Time consumed %f s" % (timeTime.time()-start))
    mupif.log.debug("Ping test finished")

finally:
    mupif.log.debug("Closing ssh tunnel")
    if tunnel:
        tunnel.terminate()

