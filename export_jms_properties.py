# --------------------------------------------------------------------
# Script: export_jms_properties.py
# Purpose: Export JMS resources for a cluster into a .properties file
# Usage:
#   wsadmin.sh -lang jython -f export_jms_properties.py <ClusterName>
# Output:
#   <ClusterName>_jms.properties
# --------------------------------------------------------------------

import sys

if len(sys.argv) != 1:
    print "Usage: wsadmin.sh -lang jython -f export_jms_properties.py <ClusterName>"
    sys.exit(1)

clusterName = sys.argv[0]
exportFile = "%s_jms.properties" % clusterName

print "\n=== Exporting JMS properties for cluster: %s ===\n" % clusterName

def getClusterMembers(clusterName):
    clusterID = AdminConfig.getid('/ServerCluster:%s/' % clusterName)
    if not clusterID:
        print "ERROR: Cluster not found:", clusterName
        sys.exit(1)

    members = AdminConfig.list('ClusterMember', clusterID).splitlines()
    servers = []
    for m in members:
        node = AdminConfig.showAttribute(m, 'nodeName')
        server = AdminConfig.showAttribute(m, 'memberName')
        servers.append((node, server))
    return servers

def writeResource(propFile, prefix, resourceID):
    name = AdminConfig.showAttribute(resourceID, "name")
    attrs = AdminConfig.show(resourceID)

    propFile.write("[%s:%s]\n" % (prefix, name))
    for line in attrs.splitlines():
        if line.strip() and "=" in line:
            propFile.write(line.strip() + "\n")
    propFile.write("\n")

servers = getClusterMembers(clusterName)
propFile = open(exportFile, "w")

for (node, server) in servers:
    scope = "/Node:%s/Server:%s/" % (node, server)
    print "Exporting for Node=%s  Server=%s" % (node, server)

    resources = {
        "SIBJMSConnectionFactory": AdminConfig.list("SIBJMSConnectionFactory", scope).splitlines(),
        "SIBQueue": AdminConfig.list("SIBQueue", scope).splitlines(),
        "SIBTopic": AdminConfig.list("SIBTopic", scope).splitlines(),
        "J2CActivationSpec": AdminConfig.list("J2CActivationSpec", scope).splitlines(),
        "MQQueueConnectionFactory": AdminConfig.list("MQQueueConnectionFactory", scope).splitlines(),
        "MQTopicConnectionFactory": AdminConfig.list("MQTopicConnectionFactory", scope).splitlines(),
        "MQQueue": AdminConfig.list("MQQueue", scope).splitlines(),
        "MQTopic": AdminConfig.list("MQTopic", scope).splitlines()
    }

    for resType in resources:
        for res in resources[resType]:
            if res.strip():
                writeResource(propFile, resType, res)

propFile.close()

print "\nProperties exported to:", exportFile
