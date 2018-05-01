#!flask/bin/python

import functions
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

# functions.query_assocmeta_cpgid(["cg00000029"], dbConnection, "snp, cpg, pval", 1e-30)
# functions.query_assocmeta_snpid(["chr10:100003302:SNP", "chr10:10000018:SNP"], dbConnection, "pval")

# functions.query_assocmeta_rsid(["rs6602381", "rs72828459"], dbConnection, "pval")
# functions.query_assocmeta_gene_snp("A1BG", dbConnection)

assoc_meta_fields = {
	'cpg': fields.String,
	'snp': fields.String,
	'rsid': fields.String,
	'beta_a1': fields.Float,
	'se': fields.Float,
	'pval': fields.Float,
	'samplesize': fields.Integer,
	'a1': fields.String,
	'a2': fields.String,
	'freq_a1': fields.Float,
	'freq_se': fields.Float,
	'cistrans': fields.Boolean,
	'num_studies': fields.Integer,
	'direction': fields.String,
	'hetisq': fields.Float,
	'hetchisq': fields.Float,
	'hetpval': fields.Float,
	'tausq': fields.Float,
	'beta_are_a1': fields.Float,
	'se_are': fields.Float,
	'pval_are': fields.Float,
	'se_mre': fields.Float,
	'pval_mre': fields.Float,
	'chunk': fields.Integer
}

AssocMetaRsid_fields = assoc_meta_fields
AssocMetaRsid_fields['uri'] = fields.Url('AssocMetaRsid')

AssocMetaCpg_fields = assoc_meta_fields
AssocMetaCpg_fields['uri'] = fields.Url('AssocMetaRsid')

AssocMetaGeneCpg_fields = assoc_meta_fields
AssocMetaGeneCpg_fields['uri'] = fields.Url('AssocMetaGeneCpg')

AssocMetaGeneSnp_fields = assoc_meta_fields
AssocMetaGeneSnp_fields['uri'] = fields.Url('AssocMetaGeneSnp')

dbConnection = functions.get_connection("db.conf")

class AssocMetaRsid(Resource):
	def __init__(self):
		super(AssocMetaRsid, self).__init__()

	def get(self, rsid):
		out = functions.query_assocmeta_rsid([rsid], dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, AssocMetaRsid_fields)}, 200


class AssocMetaCpg(Resource):
	def __init__(self):
		super(AssocMetaCpg, self).__init__()

	def get(self, cpg):
		out = functions.query_assocmeta_cpgid([cpg], dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, AssocMetaCpg_fields)}, 200

class AssocMetaGeneCpg(Resource):
	def __init__(self):
		super(AssocMetaGeneCpg, self).__init__()

	def get(self, gene):
		out = functions.query_assocmeta_gene_cpg(gene, dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, AssocMetaGeneCpg_fields)}, 200

class AssocMetaGeneSnp(Resource):
	def __init__(self):
		super(AssocMetaGeneSnp, self).__init__()

	def get(self, gene):
		out = functions.query_assocmeta_gene_Snp(gene, dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, AssocMetaGeneSnp_fields)}, 200


api.add_resource(AssocMetaRsid, '/godmc/api/v0.1/assoc_meta/rsid/<rsid>', endpoint='AssocMetaRsid')
api.add_resource(AssocMetaCpg, '/godmc/api/v0.1/assoc_meta/cpg/<cpg>', endpoint='AssocMetaCpg')
api.add_resource(AssocMetaGeneCpg, '/godmc/api/v0.1/assoc_meta/cpg_gene/<gene>', endpoint='AssocMetaGeneCpg')
api.add_resource(AssocMetaGeneSnp, '/godmc/api/v0.1/assoc_meta/Snp_gene/<gene>', endpoint='AssocMetaGeneSnp')

if __name__ == '__main__':
	app.run(debug=True)
