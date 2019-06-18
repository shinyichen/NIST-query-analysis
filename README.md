## Python Files
### Requires
* `aida-tools`
* `vistautils`
* `vistanlp-sandbox`
### analysis-ta1-class.py
Process TA1 class query summary results
Inputs:
* query_dir: path to NIST TA1 class queries
* result_file: path to the NIST TA1 class queries summary output
    * To get this file, use `> result_summary.txt` when running the NSIT queries
* outdir: dir you want the output in
### analysis-ta1-graph.py
Process TA1 graph query summary results
Inputs:
* query_dir: path to NIST TA1 graph queries
* result_file: path to the NIST TA1 graph queries summary output
    * To get this file, use `> result_summary.txt` when running the NIST queries
* outdir: dir you want the output in
### analysis-ta1-detail.py
Process all TA1 actual query results
Inputs:
* corpus_file: a zip file of the corpus
    * If corpus is TGZ, run vistautils/scripts/tar_gz_to_zip.py on .tgz corpus
* result_dir: path to the NIST TA1 queries output dir
* out_dir: dir you want the output in
### analysis-ta1-ca.py
Process TA1 confidence aggregation results 
Inputs:
* corpus_file: corpus_file: a zip file of the corpus
    * If corpus is TGZ, run vistautils/scripts/tar_gz_to_zip.py on .tgz corpus
* result_dir: path to the confidence aggregation output dir
* out_dir: dir you want the output in
### analysis-ta2-zerohop.py
Process TA2 zerohop query summary results
Inputs:
* query_dir: path to NIST TA2 zerohop queries
* result_file: path to the NIST TA2 zerohop queries summary output
    * To get this file, use `> result_summary.txt` when running the NSIT queries
* outdir: dir you want the output in
### analysis-ta2-graph.py
Process TA2 graph query summary results
Inputs:
* query_dir: path to NIST TA2 graph queries
* result_file: path to the NIST TA2 graph queries summary output
    * To get this file, use `> result_summary.txt` when running the NIST queries
* outdir: dir you want the output in
### analysis-ta2-detail.py
Process all TA2 actual query results
Inputs:
* corpus_file: a zip file of the corpus
    * If corpus is TGZ, run vistautils/scripts/tar_gz_to_zip.py on .tgz corpus
* result_dir: path to the NIST TA2 queries output dir
* out_dir: dir you want the output in