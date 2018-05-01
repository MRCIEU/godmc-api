# godmc-api

This is an API which is used to pull down results from the GoDMC meta analysis of genetic influences on DNA methylation levels. 

Most methods are using `get` - you put in a specific query and the result is returned

There are also more complex queries that can be obtained using `post`. Here a json file needs to be built that describes the query

All results are json format

## Get CpGs associated with a specific SNP

```
/godmc/api/v0.1/assoc_meta/cpg/<cpgid>
```

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/cpg/cg17242362](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/cpg/cg17242362)

## Get SNPs that influence a specific CpG

```
/godmc/api/v0.1/assoc_meta/rsid/<rsid>
```

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/rsid/rs6602381](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/rsid/rs6602381)

## Get all mQTLs where a SNP or CpG is within some range

```
/godmc/api/v0.1/assoc_meta/range/<attribute>/<chrrange>
```

Note: this is a bit slow due to database, needs to be improved

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/range/cpg/10:10000018-10100020](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/range/cpg/10:10000018-10100020)

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/range/snp/10:10000018-10100020](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/range/snp/10:10000018-10100020)


## Get all mQTLs where a SNP or CpG is within 25kb of a gene start site

```
/godmc/api/v0.1/assoc_meta/gene/<attribute>/<gene>
```

Note: this is a bit slow due to database, needs to be improved

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/gene/cpg/A1BG](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/gene/cpg/A1BG)

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/gene/snp/A1BG](http://127.0.0.1:5000/godmc/api/v0.1/assoc_meta/gene/snp/A1BG)

## Get a list of all genes

```
/godmc/api/v0.1/list/gene
```

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/list/gene](http://127.0.0.1:5000/godmc/api/v0.1/list/gene)


## Get information about a SNP, CpG or gene

```
/godmc/api/v0.1/info/<attribute>/<item>
```

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/info/cpg/cg26866020](http://127.0.0.1:5000/godmc/api/v0.1/info/cpg/cg26866020)

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/info/gene/A1BG](http://127.0.0.1:5000/godmc/api/v0.1/info/gene/A1BG)

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/info/rsid/rs234](http://127.0.0.1:5000/godmc/api/v0.1/info/rsid/rs234)

e.g. [http://127.0.0.1:5000/godmc/api/v0.1/info/snp/chr7:105561135:SNP](http://127.0.0.1:5000/godmc/api/v0.1/info/snp/chr7:105561135:SNP)


## More complex queries

```
curl -i -H "Content-Type: application/json" -X POST -d @test.json http://localhost:5000/godmc/api/v0.1/query
```

Query multiple SNPs, json:

```
{
    "snps": ["chr10:100003302:SNP", "chr10:99954538:INDEL", "chr10:99981275:SNP"]
}
```

Query multiple rsids, json:

```
{
    "rsids": ["rs6602381", "rs72828459", "rs234"]
}
```

Query multiple CpGs, json:

```
{
    "cpgs": ["cg14380065", "cg12715136"]
}
```

Query rsids and CpGs, json:

```
{
    "rsids": ["rs6602381", "rs72828459", "rs234"],
    "cpgs": ["cg14380065", "cg12715136"]
}
```

As in test 2 but set pval threshold, trans only, and which columns to return, json:

```
{
    "cpgs": ["cg14380065", "cg12715136"],
    "pval": 1e-10,
    "cistrans": "cis",
    "columns": "pval, cpg, cistrans"
}
```
