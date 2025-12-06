# --------------------------------------------------------------------
# Script: import_jms_properties.py
# Purpose: Import JMS resources from a properties file into a cluster
# Usage:
#   wsadmin.sh -lang jython -f import_jms_properties.py <ClusterName> <propertiesFile>
# --------------------------------------------------------------------

import sys

if len(sys.argv) != 2:
    print "Usage: wsadmin.sh -lang jython -f import_jms_properties.py <ClusterName> <propertiesFile>"
    sys.exit(1)

clusterName = sys.argv[0]
propFile = sys.argv[1]

data = {}
section = None

for line in open(propFile):
    line = line.strip()
    if not line:
        continue

    if line.startswith("[") and ":" in line:
        section = line[1:-1]
        data[section] = []
    else:
        data[section].append(line)

clusterID = AdminConfig.getid('/ServerCluster:%s/' % clusterName)
members = AdminConfig.list('ClusterMember', clusterID).splitlines()

print "\nImporting JMS resources into cluster:", clusterName

for section in data:
    resType, name = section.split(":")
    attributes = data[section]

    print "Creating:", resType, name

    attrList = []
    for a in attributes:
        k, v = a.split("=", 1)
        attrList.append([k, v])

    AdminTask.createJMSResourceAtScope('ServerCluster=' + clusterName,
        ['-type', resType, '-name', name, '-attributes', attrList])

AdminConfig.save()
print "\n=== Import Completed ==="
