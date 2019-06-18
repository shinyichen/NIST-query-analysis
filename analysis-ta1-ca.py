import sys
import os
import csv
# aida_tools_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../aida-tools')
# sys.path.append(aida_tools_path)
from aida_tools.corpus import TextJustificationLookup, AidaCorpus
from zipfile import ZipFile
from analysis_utils import parse_text_from_source

# confidence aggregation results

# inputs
corpus_file = 'dryrun-2019-03.zip'
result_dir = '../aida/tools/confidence-aggregation/ta1-dryrun3'
out_dir = 'output/dryrun3/ta1-ca'

inf_just_pattern = '(.+):(.+):\\(([0-9]+),[0-9]\\)-\\(([0-9]+),[0-9]\\)'
ldcOnt = 'https://tac.nist.gov/tracks/SM-KBP/2019/ontologies/LDCOntology#'

html_header = '''
<html>
<head>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  text-align: left;
}
</style>
</head>
<body>
'''

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

with ZipFile(corpus_file) as corpus_zipfile:

    text_justification_lookup = TextJustificationLookup(AidaCorpus.from_zip_file(corpus_zipfile))

    # for each ttl directory in result directory
    for aif in os.listdir(result_dir):
        if os.path.isdir(os.path.join(result_dir, aif)):
            ttl_dir = os.path.join(result_dir, aif)

            # create output directory
            ttl_out_dir = os.path.join(out_dir, aif)
            if not os.path.exists(ttl_out_dir):
                os.mkdir(ttl_out_dir)

            # process each query result file
            for file in os.listdir(ttl_dir):
                file_path = ttl_dir + '/' + file
                with open(file_path) as tsv_file:
                    reader = csv.DictReader(tsv_file, delimiter='\t')

                    # class query file
                    if 'AIDA_TA1_CL' in file:
                        with open(ttl_out_dir + '/' + file + '.html', 'w') as out_file_class:
                            out_file_class.write(html_header)
                            out_file_class.write(file)
                            out_file_class.write('<table>')
                            out_file_class.write('''
                            <tr>
                                <th>cluster</th>
                                <th>rank</th>
                            </tr>
                            ''')
                            for row in reader:

                                # write output
                                out_file_class.write('''
                                <tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                </tr>
                                ''' % (row['?cluster'].replace(ldcOnt, 'ldcOnt:')[1:-1],
                                       row['?rank'])
                                )
                            out_file_class.write('<table></body><html>')

                    # graph query file
                    elif 'AIDA_TA1_GR' in file:
                        with open(ttl_out_dir + '/' + file + '.html', 'w') as out_file_graph:
                            out_file_graph.write(html_header)
                            out_file_graph.write(file)
                            out_file_graph.write('<table>')
                            out_file_graph.write('''
                            <tr>
                                <th>docid</th>
                                <th>edge_type_q</th>
                                <th>result</th>
                                <th>ag_cv</th>
                                <th>rank</th>
                             </tr>
                             ''')
                            for row in reader:

                                # get informative mention
                                oinf_j_span = row['?oinf_j_span']
                                ej_span = row['?ej_span']
                                oinf_mention_tok, oinf_mention_txt = parse_text_from_source(text_justification_lookup, inf_just_pattern, oinf_j_span)
                                ej_mention_tok, ej_mention_txt = parse_text_from_source(text_justification_lookup, inf_just_pattern, ej_span)

                                result = '''
                                <ul>
                                <li><b>edge_type</b>: %s</li>
                                <li><b>subject_cluster</b>: %s</li>
                                <li><b>subjectmo</b>: %s</li>
                                <li><b>ej_span</b>: %s</li>
                                <li><b>ej_context</b>: %s</li>
                                </ul>
                                <ul>
                                <li><b>object_cluster</b>: %s</li>
                                <li><b>objectmo</b>: %s</li>
                                <li><b>oinf_j_span</b>: %s</li>
                                <li><b>oinf_j_context</b>: %s</li>
                                </ul>
                                <ul>
                                <li><b>oinf_j_cv</b>: %s</li>
                                <li><b>obcm_cv</b>: %s</li>
                                <li><b>edge_cj_cv</b>: %s</li>
                                <li><b>sbcm_cv</b>: %s</li>
                                </ul>
                                ''' % (row['?edge_type'].replace(ldcOnt, 'ldcOnt:')[1:-1],
                                       row['?subject_cluster'][1:-1],
                                       row['?subjectmo'][1:-1],
                                       ej_mention_tok,
                                       ej_mention_txt,
                                       row['?object_cluster'][1:-1],
                                       row['?objectmo'][1:-1],
                                       oinf_mention_tok,
                                       oinf_mention_txt,
                                       row['?oinf_j_cv'],
                                       row['?obcm_cv'],
                                       row['?edge_cj_cv'],
                                       row['?sbcm_cv']
                                       )
                                out_file_graph.write('''
                                <tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                </tr>
                                ''' % (row['?docid'],
                                       row['?edge_type_q'].replace(ldcOnt, 'ldcOnt:')[1:-1],
                                       result,
                                       row['?ag_cv'],
                                       row['?rank'])
                                )
                            out_file_graph.write('</table></body></html>')
