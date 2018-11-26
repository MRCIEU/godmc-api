from functions import *

dbConnection = get_connection("db.conf")

def test_cpgquery():
    result = query_assocmeta_cpgid(["cg24851651"],dbConnection, columns="*", maxpval=1e-250)
    assert result[0]["clumped"] >= 0

def test_rsidquery():
    result = query_assocmeta_rsid(["rs7105015"],dbConnection, columns="*", maxpval=1e-250)
    assert result[0]["clumped"] >= 0

