import json
import PySQLPool
import itertools

def get_connection(fn):
	with open(fn) as f:
		db_config = json.load(f)
	dbConnection = PySQLPool.getNewConnection(**db_config)
	return dbConnection

def run_query(SQL, dbConnection):
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return json.dumps(query.record)


## SNPs

def get_snpid_from_rsid(rsid, dbConnection):
	rsids = ",".join([ "'" + x + "'" for x in rsid ])
	SQL = """SELECT name,rsid from snp
		WHERE rsid IN ({0})""".format(rsids)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record

def query_snp_rsids(rsid, dbConnection, columns="*"):
	rsids = ",".join([ "'" + x + "'" for x in rsid ])
	SQL = """SELECT {0} from snp 
		WHERE rsid IN ({1})""".format(columns, rsids)
	return run_query(SQL, dbConnection)

def query_snp_name(name, dbConnection, columns="*"):
	names = ",".join([ "'" + x + "'" for x in name ])
	SQL = """SELECT {0} from snp 
		WHERE name IN ({1})""".format(columns, names)
	return run_query(SQL, dbConnection)


# def query_snp_chrpos(chrpos, dbConnection):
# 	# WARNING
# 	# EXTREMELY SLOW
# 	# chr, pos = zip(*(s.split(":") for s in chrpos))
# 	chrposs = ",".join([ "'" + x + "'" for x in chrpos ])
# 	SQL = """SELECT * FROM snp
# 		WHERE CONCAT(chr, ':', pos) IN ({0})""".format(chrposs)
# 	return run_query(SQL, dbConnection)

def query_snp_chrpos(chrpos, dbConnection, columns="*"):
	chrompos = [{"chrom":int(x[0]), "pos":int(x[1])} for x in [item.split(":") for item in chrpos]]
	# pos = list(pos)
	out = []
	for key, group in itertools.groupby(chrompos, key=lambda x:x['chrom']):
		# print key, group
		posx = ",".join([ "'" + str(x['pos']) + "'" for x in list(group)])
		SQL = """SELECT {0} from snp
			WHERE chr = {1}
			AND pos IN ({2})""".format(columns, key, posx)
		temp=run_query(SQL, dbConnection)
		print(temp)
	return out

def query_snp_range(chrrange, dbConnection, columns="*"):
	temp = chrrange.split(":")
	chr=int(temp[0])
	temp2=temp[1].split("-")
	p1=int(temp2[0])
	p2=int(temp2[1])
	SQL = """SELECT {0} from snp
		WHERE chr = {1}
		AND pos >= {2}
		AND pos <= {3}""".format(columns, chr, p1, p2)
	return run_query(SQL, dbConnection)


## Assocs

def query_assocmeta_cpgid(cpgid, dbConnection, columns="*", maxpval=0.05):
	cpgids = ",".join([ "'" + x + "'" for x in cpgid ])
	SQL = """SELECT {0} from assoc_meta
		WHERE cpg IN ({1})
		AND pval < {2}
		ORDER BY pval""".format(columns, cpgids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_snpid(snpid, dbConnection, columns="*", maxpval=0.05):
	snpids = ",".join([ "'" + x + "'" for x in snpid ])
	SQL = """SELECT {0} from assoc_meta
		WHERE snp IN ({1})
		AND pval < {2}
		ORDER BY pval""".format(columns, snpids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_rsid(rsid, dbConnection, columns="*", maxpval=0.05):
	snpids = ",".join([ "'" + x['name'] + "'" for x in get_snpid_from_rsid(rsid, dbConnection) ])
	SQL = """SELECT {0} from assoc_meta
		WHERE snp IN ({1})
		AND pval < {2}
		ORDER BY pval""".format(columns, snpids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_gene_snp(gene, dbConnection, window=250000, columns="*", maxpval=0.05):
	# get IDs
	SQL = """SELECT name,chr,start_pos,stop_pos from gene WHERE name = '{0}'""".format(gene)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	geneinfo = query.record[0]
	SQL = """SELECT name from snp
		WHERE chr = {0}
		AND pos >= {1}
		AND pos <= {2}""".format(geneinfo['chr'], geneinfo['start_pos']-window, geneinfo['start_pos']+window)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	snpid = [x['name'] for x in query.record]
	return query_assocmeta_snpid(snpid, dbConnection, columns, maxpval)

def query_assocmeta_gene_cpg(gene, dbConnection, window=250000, columns="*", maxpval=0.05):
	# get IDs
	SQL = """SELECT name,chr,start_pos,stop_pos from gene WHERE name = '{0}'""".format(gene)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	geneinfo = query.record[0]
	SQL = """SELECT name from cpg
		WHERE chr = {0}
		AND pos >= {1}
		AND pos <= {2}""".format(geneinfo['chr'], geneinfo['start_pos']-window, geneinfo['start_pos']+window)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	cpgid = [x['name'] for x in query.record]
	return query_assocmeta_cpgid(cpgid, dbConnection, columns, maxpval)

