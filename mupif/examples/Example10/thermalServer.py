import thermalServerConfig as sConf
import os
from mupif import *
import logging
logger = logging.getLogger()

# required firewall settings (on ubuntu):
# for computer running daemon (this script)
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 44361 -j ACCEPT
# for computer running a nameserver
# sudo iptables -A INPUT -p tcp -d 0/0 -s 0/0 --dport 9090 -j ACCEPT


#locate nameserver
ns = PyroUtil.connectNameServer(nshost=sConf.nshost, nsport=sConf.nsport, hkey=sConf.hkey)

#Run a daemon for jobMamager on this machine
daemon = PyroUtil.runDaemon(host=sConf.daemonHost, port=sConf.jobManPort, nathost=sConf.nathost, natport=sConf.jobManNatport)
#Run job manager on a server
jobMan = JobManager.SimpleJobManager2(daemon, ns, sConf.applicationClass, sConf.jobManName, sConf.jobManPortsForJobs, sConf.jobManWorkDir, os.getcwd(), 'thermalServerConfig', sConf.jobMan2CmdPath, sConf.jobManMaxJobs, sConf.jobManSocket)

#set up daemon with JobManager
uri = daemon.register(jobMan)
#register JobManager to nameServer
ns.register(sConf.jobManName, uri)
logger.debug ("Daemon for JobManager runs at " + str(uri))
print 80*'-'
print ("Started "+sConf.jobManName)
#waits for requests
daemon.requestLoop()