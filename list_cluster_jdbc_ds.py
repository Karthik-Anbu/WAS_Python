
# ==================================================================================
# list_cluster_jdbc_ds.py
# Collects JDBC Providers and DataSources for a given cluster
# Outputs to <clusterName>_datasource.txt
# ==================================================================================

import sys

# --- READ CLUSTER NAME FROM ARGUMENT ---
if len(sys.argv) < 1:
    print "ERROR: No cluster name provided."
    print "Usage: wsadmin.sh -lang jython -f list_cluster_jdbc_ds.py <ClusterName>"
    sys.exit(1)

clusterName = sys.argv[0]

# --- OUTPUT FILE ---
outputFile = clusterName + "_datasource.txt"
f = open(outputFile, "w")

def write(line):
    print line
    f.write(line + "\n")

write("=============================================================")
write(" WebSphere Cluster JDBC Providers and DataSources")
write(" Cluster: " + clusterName)
write("=============================================================\n")

# --- GET CLUSTER ID ---
clusterID = AdminConfig.getid("/ServerCluster:" + clusterName + "/")
if clusterID == "":
    write("ERROR: Cluster not found: " + clusterName)
    f.close()
    sys.exit(1)

# -----------------------------
# 1. JDBC PROVIDERS
# -----------------------------
write("=== JDBC PROVIDERS ===")
jdbcProviders = AdminConfig.list("JDBCProvider", clusterID).splitlines()

if len(jdbcProviders) == 0:
    write("No JDBC Providers found under cluster scope.\n")
else:
    for jp in jdbcProviders:
        write("\n--- JDBC Provider ---")
        write(AdminConfig.show(jp))

# -----------------------------
# 2. DATASOURCES
# -----------------------------
write("\n=== DATASOURCES ===")
dataSources = AdminConfig.list("DataSource", clusterID).splitlines()

if len(dataSources) == 0:
    write("No DataSources found under cluster scope.\n")
else:
    for ds in dataSources:
        write("\n--- DataSource ---")
        write(AdminConfig.show(ds))

write("\nOutput saved to file: " + outputFile)
f.close()
