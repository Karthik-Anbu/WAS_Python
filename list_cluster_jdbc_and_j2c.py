
# ==================================================================================
# list_cluster_jdbc_and_j2c.py
# Collects JDBC Providers, DataSources, and J2C Auth data for a given cluster
# Outputs to <clusterName>_datasource.txt
# ==================================================================================

import sys

# --- READ CLUSTER NAME FROM ARGUMENT ---
if len(sys.argv) < 1:
    print "ERROR: No cluster name provided."
    print "Usage: wsadmin.sh -lang jython -f list_cluster_jdbc_and_j2c.py <ClusterName>"
    sys.exit(1)

clusterName = sys.argv[0]

# --- OUTPUT FILE ---
outputFile = clusterName + "_datasource.txt"
f = open(outputFile, "w")

def write(line):
    print line
    f.write(line + "\n")

write("=============================================================")
write(" WebSphere Cluster JDBC, DataSource, and J2C Details")
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

# -----------------------------
# 3. JAAS-J2C AUTHENTICATION DATA
# -----------------------------
write("\n=== JAAS-J2C AUTHENTICATION ALIASES ===")
j2cEntries = AdminConfig.list("JAASAuthData").splitlines()

if len(j2cEntries) == 0:
    write("No JAAS J2C authentication entries found.\n")
else:
    for j in j2cEntries:
        write("\n--- J2C Entry ---")
        write(AdminConfig.show(j))

# -----------------------------
# 4. DATASOURCE → J2C ALIAS MAPPING
# -----------------------------
write("\n=== DATASOURCE → J2C AUTHENTICATION MAPPING ===")

if len(dataSources) == 0:
    write("No DataSources found; skipping mapping.\n")
else:
    for ds in dataSources:
        dsName = AdminConfig.showAttribute(ds, "name")
        authAlias = AdminConfig.showAttribute(ds, "authDataAlias")
        write("%s  -->  J2C Alias: %s" % (dsName, authAlias))

write("\nOutput saved to file: " + outputFile)
f.close()
