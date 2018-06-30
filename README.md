---
title: "GoDMC results API"
output:
  html_document:
    toc: true
    theme: united
---

---

This is an API which is used to pull down results from the GoDMC meta analysis of genetic influences on DNA methylation levels. 

Most methods are using `get` - you put in a specific query and the result is returned

There are also more complex queries that can be obtained using `post`. Here a json file needs to be built that describes the query

All results are json format

---

## Get a list of all cohorts

```
/v0.1/cohorts
```

e.g. [http://api.godmc.org.uk/v0.1/cohorts](http://api.godmc.org.uk/v0.1/cohorts)

---

## Get mQTLs for a specific SNP or CpG

```
/v0.1/assoc_meta/cpg/<cpgid>
/v0.1/assoc_meta/rsid/<rsid>
/v0.1/assoc_meta/snp/<snpid>
```

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/cpg/cg17242362](http://api.godmc.org.uk/v0.1/assoc_meta/cpg/cg17242362)

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/rsid/rs6602381](http://api.godmc.org.uk/v0.1/assoc_meta/rsid/rs6602381)

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/snp/chr10:10000018:SNP](http://api.godmc.org.uk/v0.1/assoc_meta/snp/chr10:10000018:SNP)

---

The -log10(p-values) for all associations with a particular SNP or CpG can be obtained in bed or BigBed format as:

```
/v0.1/dl/<format>/cpg/<cpgid>
/v0.1/dl/<format>/snp/<snpid>
```

e.g. [http://api.godmc.org.uk/v0.1/dl/bigbed/cpg/cg17242362](http://api.godmc.org.uk/v0.1/dl/bigbed/cpg/cg17242362)

e.g. [http://api.godmc.org.uk/v0.1/dl/bed/snp/chr10:10000018:SNP](http://api.godmc.org.uk/v0.1/dl/bed/snp/chr10:10000018:SNP)


---

## Get all mQTLs where a SNP or CpG is within some range

```
/v0.1/assoc_meta/range/<attribute>/<chrrange>
```

Note: this is a bit slow due to database, needs to be improved

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/range/cpg/10:10000000-10100000](http://api.godmc.org.uk/v0.1/assoc_meta/range/cpg/10:10000000-10100000)

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/range/snp/10:10000000-10100000](http://api.godmc.org.uk/v0.1/assoc_meta/range/snp/10:10000000-10100000)

---

## Get all mQTLs where a SNP or CpG is within 25kb of a gene start site

```
/v0.1/assoc_meta/gene/<attribute>/<gene>
```

Note: this is a bit slow due to database, needs to be improved

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/gene/cpg/A1BG](http://api.godmc.org.uk/v0.1/assoc_meta/gene/cpg/A1BG)

e.g. [http://api.godmc.org.uk/v0.1/assoc_meta/gene/snp/A1BG](http://api.godmc.org.uk/v0.1/assoc_meta/gene/snp/A1BG)

---

## Get a list of all genes

```
/v0.1/list/gene
```

e.g. [http://api.godmc.org.uk/v0.1/list/gene](http://api.godmc.org.uk/v0.1/list/gene)

---

## Get information about a SNP, CpG or gene

```
/v0.1/info/<attribute>/<item>
```

e.g. [http://api.godmc.org.uk/v0.1/info/cpg/cg26866020](http://api.godmc.org.uk/v0.1/info/cpg/cg26866020)

e.g. [http://api.godmc.org.uk/v0.1/info/gene/A1BG](http://api.godmc.org.uk/v0.1/info/gene/A1BG)

e.g. [http://api.godmc.org.uk/v0.1/info/rsid/rs234](http://api.godmc.org.uk/v0.1/info/rsid/rs234)

e.g. [http://api.godmc.org.uk/v0.1/info/snp/chr7:105561135:SNP](http://api.godmc.org.uk/v0.1/info/snp/chr7:105561135:SNP)

---

## More complex queries

There is a limit to the length of a URL, so if you want to extract a large list of SNPs then we need to post the query details through a file. This can be done through `curl` e.g. using:

```bash
curl -i -H "Content-Type: application/json" -X POST -d @test.json http://api.godmc.org.uk/v0.1/query
```

Here we are posting the `test.json` file that contains the details of the query. Examples below

---

Query multiple SNPs, `test.json`:

```json
{
    "snps": ["chr10:100003302:SNP", "chr10:99954538:INDEL", "chr10:99981275:SNP"]
}
```

Query multiple rsids, `test.json`:

```json
{
    "rsids": ["rs6602381", "rs72828459", "rs234"]
}
```

Query multiple CpGs, `test.json`:

```json
{
    "cpgs": ["cg14380065", "cg12715136"]
}
```

Query mQTLs for rsids and CpGs, (i.e. get all results where an mQTL contains a SNP and a CpG specified in the lists), `test.json`:

```json
{
    "rsids": ["rs6602381", "rs72828459", "rs234"],
    "cpgs": ["cg14380065", "cg12715136"]
}
```

As in the third example but set p-value threshold, only return cis effects, and specify which columns to return, `test.json`:

```json
{
    "cpgs": ["cg14380065", "cg12715136"],
    "pval": 1e-10,
    "cistrans": "cis",
    "columns": "pval, cpg, cistrans"
}
```
