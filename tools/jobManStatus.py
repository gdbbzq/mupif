#!/usr/bin/env python


import getopt, sys
sys.path.append('..')
sys.path.append('.')
from mupif import JobManager
from mupif import PyroUtil
from mupif import APIError

import logging
import time as timeTime
import curses


def usage():
    print "Usage: jobManStatus -h hostname -p port"


def processor(win, jobman):
    win.erase()

    win.addstr(0,0, "MuPIF Remote JobMan MONITOR")
    win.addstr(1,0, "JobManager:"+jobmanName)
    win.hline(2,0,'-',80)
    win.addstr(3,jobid_col, "JobID")
    win.addstr(3,port_col, "Port")
    win.addstr(3,user_col,"user@host")
    win.addstr(3,time_col,"time")


    win.addstr(23,0,"[q]uit")
    win.refresh()

    win1 = curses.newwin (10, 80, 5, 0)

    win.nodelay(1)
    while True:
        win.addstr (0, 70, timeTime.strftime("%H:%M:%S", timeTime.gmtime()))
        win.refresh()

        win1.erase()
        c = win.getch()
        if c == ord('q'):
            break
        status=jobMan.getStatus()
        i = 0
        for rec in status:
            win1.addstr(i,jobid_col, rec[0])
            win1.addstr(i,port_col, str(rec[3]))
            win1.addstr(i,user_col, rec[2])
            mins = int(rec[1])/60
            hrs  = mins/24
            mins = mins%60
            sec  = int(rec[1])%60
            jobtime = "%02d:%02d:%02d"%(hrs, mins, sec)
            win1.addstr(i,time_col, jobtime)
            i = i+1
        win1.refresh()
        timeTime.sleep(1)
    return



#######################################################################################


logging.getLogger().setLevel(logging.WARNING)
logger = logging.getLogger()
#ssh flag (se to tru if ssh tunnel need to be established)
ssh = False

host = 'ksm.fsv.cvut.cz'
port = 9090


try:
    opts, args = getopt.getopt(sys.argv[1:], "h:j:")
except getopt.GetoptError as err: 
    # print help information and exit: 
    print str(err) # will print something like "option -a not recognized"
    usage()
    sys.exit(2)

for o, a in opts:
    if o in ("-p"):
        port = int(a)                                                                                              
    elif o in ("-h"):
        host = a                                                                                                        
    else:
        assert False, "unhandled option"

print "huhu:"+host+str(port)

jobid_col = 0
port_col  = 35
user_col = 41
time_col = 70

#locate nameserver
ns     = PyroUtil.connectNameServer(host, port, "mmp-secret-key")


print ("haha")

#extablish secure ssh tunnel connection
if ssh:
    tunnel = PyroUtil.sshTunnel(remoteHost='mech.fsv.cvut.cz', userName='bp', localPort=5353, remotePort=44382, sshClient='ssh')

# locate remote jobManager application, request remote proxy
jobMan = PyroUtil.connectApp(ns, 'Mupif.JobManager@demo')



logging.getLogger().setLevel(logging.WARNING)
logger = logging.getLogger()
#ssh flag (se to tru if ssh tunnel need to be established)
ssh = False

jobmanName = 'Mupif.JobManager@demo'


curses.wrapper(processor, jobMan)

if ssh:
    tunnel.terminate()


###########################################################
