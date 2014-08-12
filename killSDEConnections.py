# -*- coding: latin-1 -*-
#~ killSDEConnections.py
import sys
import subprocess
import cx_Oracle
import ConfigParser

#~ Variablen (übergeben von Kommandozeile)
db = sys.argv[1].upper()
pw = sys.argv[2]
configFile = "sdeConfig.ini"

def getConfiguration(filename):
	config = ConfigParser.ConfigParser()
	config.read(filename)
	c = {
		'oracledb' : config.get(db, 'oracledb'),
		'sdehost' : config.get(db, 'sdehost'),
		'sdeport' : config.get(db, 'sdeport'),
		'sdeuser' : config.get(db, 'sdeuser'),
		'ARCGISSERVERHOSTS' : config.get('GENERAL', 'ARCGISSERVERHOSTS').split(','),
		'sdepw' : pw
	}
	return c

def executeSQL(db, user, pw, sql):
	connection = cx_Oracle.connect(user + "/" + pw + "@" + db)
	cursor = connection.cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	cursor.close()
	connection.close()
	return results

def getConnectionsToKill(configuration):
	result = []
	inClause = "('" + "','".join(configuration['ARCGISSERVERHOSTS']) + "')"
	sql = "select sde_id, owner, nodename, start_time from SDE.PROCESS_INFORMATION where START_TIME < (select sysdate - interval '1' day from dual) and nodename in " + inClause
	print sql
	connections = executeSQL(configuration['oracledb'], configuration['sdeuser'], configuration['sdepw'], sql)
	
	print "SDE-Connections to kill:"
	for c in connections:
		print c[0]
		result.append(c[0])
	return result

def killConnections(connections, configuration):
	for c in connections:
		cmd = "sdemon -o kill -i " + configuration['sdeport'] + " -s " + configuration['sdehost'] + " -u " + configuration['sdeuser'] + " -p " + configuration['sdepw'] + " -N -t " + str(c)
		subprocess.call(cmd)
		print cmd
	
if __name__ == '__main__':
	configuration = getConfiguration(configFile)
	connections = getConnectionsToKill(configuration)
	killConnections(connections, configuration)