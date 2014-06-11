# -*- coding: latin-1 -*-
import sys
import subprocess

#~ Variablen (übergeben von Kommandozeile)
host = sys.argv[1]
port = sys.argv[2]
password = sys.argv[3]

#~ Konstanten
sdeuser = "sde"

#~ Liste mit Connections (sde_id aus sde.process_information)
conns = [1,2]
for c in conns:
	cmd = "sdemon -o kill -i " + port + " -s " + host + " -u " + sdeuser + " -p " + password + " -N -t " + str(c)
	subprocess.call(cmd)
	print cmd