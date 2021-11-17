import jaydebeapi
conn = jaydebeapi.connect("com.ibm.db2.jcc.DB2Driver",
                          "jdbc:db2://1935517f-2e89-4967-afed-33dfb6132c62.bv7e8rbf0shslbo0krsg.databases.appdomain.cloud:32652/bludb:user=996c9fac;password=dLdh5Y6x4N6kN2El;sslConnection=true;"
                          ,None,
                          "/Users/annaistomina/Documents/python_projects/db2jcc4.jar")
curs = conn.cursor()
curs.execute("SELECT * FROM DB2_ORANGE.TOP5")
print(curs.fetchall())
curs.close()
conn.close()