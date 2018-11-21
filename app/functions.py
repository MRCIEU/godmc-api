import json
import PySQLPool
import itertools

def merge_lists(l1, l2, key):
	merged = {}
	for item in l1+l2:
		if item[key] in merged:
			merged[item[key]].update(item)
		else:
			merged[item[key]] = item
	return [val for (_, val) in merged.items()]

def get_connection(fn):
	with open(fn) as f:
		db_config = json.load(f)
	dbConnection = PySQLPool.getNewConnection(**db_config)
	return dbConnection

def run_query(SQL, dbConnection):
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record


## SNPs

def get_snpid_from_rsid(rsid, dbConnection):
	rsids = ",".join([ "'" + x + "'" for x in rsid ])
	SQL = """SELECT name,rsid from snp
		WHERE rsid IN ({0})""".format(rsids)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record


## Gene / SNP / CpG lists

def get_attribute_list(dbConnection, attribute, columns="*", limit=2147483647):
	SQL = """SELECT {0} from {1} LIMIT {2}""".format(columns, attribute, limit)
	return run_query(SQL, dbConnection)

def get_attribute_item(attribute, item, dbConnection, columns="*"):
	items = ",".join([ "'" + x + "'" for x in item ])
	if attribute == "rsid":
		table = "snp"
		col = "rsid"
	elif attribute == "snp":
		table = "snp"
		col = "name"
	elif attribute == "cpg":
		table = "cpg"
		col = "name"
	elif attribute == "gene":
		table = "gene"
		col = "name"
	else:
		return ()
	SQL = """SELECT {0} from {1}
		WHERE {2} IN ({3})""".format(columns, table, col, items)
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
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b
		WHERE a.snp=b.name
		AND a.cpg IN ({1})
		AND a.pval < {2}
		ORDER BY a.pval""".format(cols, cpgids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_snpid(snpid, dbConnection, columns="*", maxpval=0.05):
	snpids = ",".join([ "'" + x + "'" for x in snpid ])
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b
		WHERE a.snp=b.name
		AND a.snp IN ({1})
		AND a.pval < {2}
		ORDER BY a.pval""".format(cols, snpids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_rsid(rsid, dbConnection, columns="*", maxpval=0.05):
	rsids = ",".join([ "'" + x + "'" for x in rsid ])
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b
		WHERE a.snp=b.name
		AND b.rsid IN ({1})
		AND a.pval < {2}
		ORDER BY a.pval""".format(cols, rsids, maxpval)
	return run_query(SQL, dbConnection)

def query_assocmeta_gene_snp(gene, dbConnection, window=250000, columns="*", maxpval=0.05):
	# get IDs
	SQL = """SELECT name,chr,start_pos,stop_pos from gene WHERE name = '{0}'""".format(gene)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	geneinfo = query.record[0]
	if len(geneinfo) is 0:
		return ()
	print("QUERY1")
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, b.chr, b.pos, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b
		WHERE a.snp=b.name
		AND b.chr = {1}
		AND b.pos >= {2}
		AND b.pos <= {3}
		AND a.pval < {4}
		ORDER BY a.pval""".format(cols, geneinfo['chr'], geneinfo['start_pos']-window, geneinfo['stop_pos']+window, maxpval)

	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record

def query_assocmeta_gene_cpg(gene, dbConnection, window=250000, columns="*", maxpval=0.05):
	# get IDs
	SQL = """SELECT name,chr,start_pos,stop_pos from gene WHERE name = '{0}'""".format(gene)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	geneinfo = query.record[0]
	if len(geneinfo) is 0:
		return ()
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, c.chr, c.pos, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b, cpg c
		WHERE a.snp=b.name
		AND a.cpg=c.name
		AND c.chr = {1}
		AND c.pos >= {2}
		AND c.pos <= {3}
		AND a.pval < {4}
		ORDER BY a.pval""".format(cols, geneinfo['chr'], geneinfo['start_pos']-window, geneinfo['stop_pos']+window, maxpval)

	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record


def query_assocmeta_range_snp(chrrange, dbConnection, columns="*", maxpval=0.05):
	# get IDs
	temp = chrrange.split(":")
	chr=int(temp[0])
	temp2=temp[1].split("-")
	p1=int(temp2[0])
	p2=int(temp2[1])
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, b.chr, b.pos, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b
		WHERE a.snp=b.name
		AND b.chr = {1}
		AND b.pos >= {2}
		AND b.pos <= {3}
		AND a.pval < {4}
		ORDER BY a.pval""".format(cols, chr, p1, p2, maxpval)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record


def query_assocmeta_range_cpg(chrrange, dbConnection, columns="*", maxpval=0.05):
	# get IDs
	temp = chrrange.split(":")
	chr=int(temp[0])
	temp2=temp[1].split("-")
	p1=int(temp2[0])
	p2=int(temp2[1])
	cols = ",".join(["a." + x for x in columns.split(",")])
	SQL = """SELECT {0}, b.name, b.rsid, c.chr, c.pos, b.allele1 AS a1, b.allele2 AS a2 FROM assoc_meta a, snp b, cpg c
		WHERE a.snp=b.name
		AND a.cpg = c.name
		AND c.chr = {1}
		AND c.pos >= {2}
		AND c.pos <= {3}
		AND a.pval < {4}
		ORDER BY a.pval""".format(cols, chr, p1, p2, maxpval)
	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record


def complex_query(args, dbConnection):

	print(args)
	if not args['pval']:
		pval = 1
	else:
		pval = args['pval']

	if not args['cistrans']:
		cistrans = ''
	elif args['cistrans'] == 'cis':
		cistrans = 'AND a.cistrans = 0'
	elif args['cistrans'] == 'trans':
		cistrans = 'AND a.cistrans = 1'
	elif args['cistrans'] == '':
		cistrans = ''
	else:
		print( "cistrans problem")
		return ()

	if not args['clumped']:
		clumped = ''
	elif args['clumped'] == '0':
		clumped = 'AND a.clumped = 0'
	elif args['clumped'] == '1':
		clumped = 'AND a.clumped = 1'
	elif args['clumped'] == '':
		clumped = ''
	else:
		print( "clumped problem")
		return ()

	# print(clumped)

	if not args['columns']:
		cols = 'a.*'
	else:
		cols = ",".join(["a." + x for x in args['columns'].split(",")])

	if args['snps']:
		snps = ",".join([ "'" + x + "'" for x in args['snps'] ])

	if args['cpgs']:
		cpgs = ",".join([ "'" + x + "'" for x in args['cpgs'] ])

	if args['rsids']:
		rsids = ",".join([ "'" + x + "'" for x in args['rsids'] ])

	if args['snps'] and args['rsids']:
		return ()

	if args['cpgs'] and not args['snps'] and not args['rsids']:
		SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM
			assoc_meta a, snp b
			WHERE a.snp=b.name
			AND a.cpg IN ({1})
			AND a.pval < {2}
			{3}
			{4}
			ORDER BY a.pval""".format(cols, cpgs, pval, cistrans, clumped)


	if args['snps'] and not args['cpgs']:
		SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM
			assoc_meta a, snp b
			WHERE a.snp=b.name
			AND a.snp IN ({1})
			AND a.pval < {2}
			{3}
			{4}
			ORDER BY a.pval""".format(cols, snps, pval, cistrans, clumped)

	if args['snps'] and args['cpgs']:
		SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM
			assoc_meta a, snp b
			WHERE a.snp=b.name
			AND a.snp IN ({1})
			AND a.cpg IN ({2})
			AND a.pval < {3}
			{4}
			{5}
			ORDER BY a.pval""".format(cols, snps, cpgs, pval, cistrans, clumped)

	if args['rsids'] and not args['cpgs']:
		SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM
			assoc_meta a, snp b
			WHERE a.snp=b.name
			AND b.rsid IN ({1})
			AND a.pval < {2}
			{3}
			{4}
			ORDER BY a.pval""".format(cols, rsids, pval, cistrans, clumped)

	if args['rsids'] and args['cpgs']:
		SQL = """SELECT {0}, b.name, b.rsid, b.allele1 AS a1, b.allele2 AS a2 FROM
			assoc_meta a, snp b
			WHERE a.snp=b.name
			AND b.rsid IN ({1})
			AND a.cpg IN ({2})
			AND a.pval < {3}
			{4}
			{5}
			ORDER BY a.pval""".format(cols, rsids, cpgs, pval, cistrans, clumped)

	query = PySQLPool.getNewQuery(dbConnection)
	query.Query(SQL)
	return query.record






