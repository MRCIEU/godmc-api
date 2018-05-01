#!flask/bin/python

import functions
from flask import Flask, jsonify, abort, make_response, send_from_directory
from flask_restful import Api, Resource, reqparse, fields, marshal

app = Flask(__name__, static_url_path="")
api = Api(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
@app.errorhandler(405)
def not_found(error):
    return make_response(jsonify({'error': 'This is too big. Download the complete data'}), 405)



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

# AssocMetaRsid_fields = assoc_meta_fields
# AssocMetaRsid_fields['uri'] = fields.Url('temp1')

# AssocMetaCpg_fields = assoc_meta_fields
# AssocMetaCpg_fields['uri'] = fields.Url('AssocMetaRsid')

# AssocMetaGeneCpg_fields = assoc_meta_fields
# AssocMetaGeneCpg_fields['uri'] = fields.Url('AssocMetaGeneCpg')

# AssocMetaGeneSnp_fields = assoc_meta_fields
# AssocMetaGeneSnp_fields['uri'] = fields.Url('AssocMetaGeneSnp')

dbConnection = functions.get_connection("db.conf")

class AssocMetaRsid(Resource):
	def __init__(self):
		super(AssocMetaRsid, self).__init__()

	def get(self, rsid):
		out = functions.query_assocmeta_rsid([rsid], dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200


class AssocMetaSnp(Resource):
	def __init__(self):
		super(AssocMetaSnp, self).__init__()

	def get(self, snp):
		out = functions.query_assocmeta_snpid([snp], dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200


class AssocMetaCpg(Resource):
	def __init__(self):
		super(AssocMetaCpg, self).__init__()

	def get(self, cpg):
		out = functions.query_assocmeta_cpgid([cpg], dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200

class AssocMetaGene(Resource):
	def __init__(self):
		super(AssocMetaGene, self).__init__()

	def get(self, attribute, gene):
		if attribute == "cpg":
			out = functions.query_assocmeta_gene_cpg(gene, dbConnection)
		elif attribute == "snp":
			out = functions.query_assocmeta_gene_snp(gene, dbConnection)
		else:
			abort(404)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200

class AssocMetaGeneSnp(Resource):
	def __init__(self):
		super(AssocMetaGeneSnp, self).__init__()

	def get(self, gene):
		out = functions.query_assocmeta_gene_snp(gene, dbConnection)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200

class AssocMetaRange(Resource):
	def __init__(self):
		super(AssocMetaRange, self).__init__()

	def get(self, attribute, chrrange):
		if attribute == "snp":
			print("snp")
			out = functions.query_assocmeta_range_snp(chrrange, dbConnection)
		elif attribute == "cpg":
			print("cpg")
			out = functions.query_assocmeta_range_cpg(chrrange, dbConnection)
		else:
			abort(404)
		if len(out) == 0:
			abort(404)
		return {'assoc_meta': marshal(out, assoc_meta_fields)}, 200


# class InfoAttribute(Resource):
# 	def __init__(self):
# 		super(ListAttribute, self).__init__()

# 	def get(self, attribute):
# 		out = functions.get_attribute_list(dbConnection, attribute)
# 		if len(out) == 0:
# 			abort(404)
# 		return out

class InfoAttribute(Resource):
	def __init__(self):
		super(InfoAttribute, self).__init__()

	def get(self, attribute):
		out = functions.get_attribute_list(dbConnection, attribute, limit=10)
		if len(out) == 0:
			abort(404)
		return out


class InfoAttributeItem(Resource):
	def __init__(self):
		super(InfoAttributeItem, self).__init__()

	def get(self, attribute, item):
		out = functions.get_attribute_item(attribute, [item], dbConnection)
		if len(out) == 0:
			abort(404)
		return out


class GetAttributeList(Resource):
	def __init__(self):
		super(GetAttributeList, self).__init__()

	def get(self, attribute):
		if attribute == 'rsid':
			out = functions.get_attribute_list(dbConnection, "snp", "rsid AS name")
		else:
			out = functions.get_attribute_list(dbConnection, attribute, "name")
		if len(out) == 0:
			abort(404)
		return [x['name'] for x in out]










###


class Readme(Resource):
	def __init__(self):
		super(Readme, self).__init__()
	
	def get(self):
		return send_from_directory(".", "index.html")



api.add_resource(Readme, 
	'/godmc/api/v0.1/', endpoint='readme')

api.add_resource(AssocMetaRsid,
	'/godmc/api/v0.1/assoc_meta/rsid/<rsid>', endpoint='AssocMetaRsid')
api.add_resource(AssocMetaSnp,
	'/godmc/api/v0.1/assoc_meta/snp/<snp>', endpoint='AssocMetaSnp')
api.add_resource(AssocMetaCpg, 
	'/godmc/api/v0.1/assoc_meta/cpg/<cpg>', endpoint='AssocMetaCpg')
api.add_resource(AssocMetaGene, 
	'/godmc/api/v0.1/assoc_meta/gene/<attribute>/<gene>', endpoint='AssocMetaGene')
api.add_resource(AssocMetaRange,
	'/godmc/api/v0.1/assoc_meta/range/<attribute>/<chrrange>', endpoint='AssocMetaRange')
api.add_resource(InfoAttribute, 
	'/godmc/api/v0.1/info/<attribute>', endpoint='InfoAttribute')
api.add_resource(InfoAttributeItem, 
	'/godmc/api/v0.1/info/<attribute>/<item>', endpoint='InfoAttributeItem')



if __name__ == '__main__':
	app.run(debug=True)
