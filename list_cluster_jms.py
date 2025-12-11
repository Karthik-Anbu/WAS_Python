# ==================================================================================
# list_cluster_jms.py
# Collects JMS Providers, Queues, Topics, and Connection Factories for a given cluster
# Outputs to <clusterName>_jms.txt
# ==================================================================================

import sys

# --- READ CLUSTER NAME FROM ARGUMENT ---
if len(sys.argv) < 1:
    print "ERROR: No cluster name provided."
    print "Usage: wsadmin.sh -lang jython -f list_cluster_jms.py <ClusterName>"
    sys.exit(1)

clusterName = sys.argv[0]

# --- OUTPUT FILE ---
outputFile = clusterName + "_jms.txt"
f = open(outputFile, "w")

def write(line):
    print line
    f.write(line + "\n")

write("=============================================================")
write(" WebSphere Cluster JMS Resources")
write(" Cluster: " + clusterName)
write("=============================================================\n")

# --- GET CLUSTER ID ---
clusterID = AdminConfig.getid("/ServerCluster:" + clusterName + "/")
if clusterID == "":
    write("ERROR: Cluster not found: " + clusterName)
    f.close()
    sys.exit(1)

# -----------------------------
# 1. JMS PROVIDERS
# -----------------------------
write("=== JMS PROVIDERS ===")
jmsProviders = AdminConfig.list("JMSProvider", clusterID).splitlines()

if len(jmsProviders) == 0:
    write("No JMS Providers found under cluster scope.\n")
else:
    for jp in jmsProviders:
        write("\n--- JMS Provider ---")
        write(AdminConfig.show(jp))

# -----------------------------
# 2. JMS QUEUES
# -----------------------------
write("\n=== JMS QUEUES ===")
jmsQueues = AdminConfig.list("Queue", clusterID).splitlines()

if len(jmsQueues) == 0:
    write("No JMS Queues found under cluster scope.\n")
else:
    for q in jmsQueues:
        write("\n--- JMS Queue ---")
        write(AdminConfig.show(q))

# -----------------------------
# 3. JMS TOPICS
# -----------------------------
write("\n=== JMS TOPICS ===")
jmsTopics = AdminConfig.list("Topic", clusterID).splitlines()

if len(jmsTopics) == 0:
    write("No JMS Topics found under cluster scope.\n")
else:
    for t in jmsTopics:
        write("\n--- JMS Topic ---")
        write(AdminConfig.show(t))

# -----------------------------
# 4. CONNECTION FACTORIES
# -----------------------------
write("\n=== CONNECTION FACTORIES ===")
connFactories = AdminConfig.list("ConnectionFactory", clusterID).splitlines()

if len(connFactories) == 0:
    write("No Connection Factories found under cluster scope.\n")
else:
    for cf in connFactories:
        write("\n--- Connection Factory ---")
        write(AdminConfig.show(cf))

write("\nOutput saved to file: " + outputFile)
f.close()