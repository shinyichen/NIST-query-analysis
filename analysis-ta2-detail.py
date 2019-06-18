import sys
import os
import csv
from aida_tools.corpus import TextJustificationLookup, AidaCorpus
from zipfile import ZipFile
from analysis_utils import parse_text_from_source

# corpus
# Before running this file, run vistautils/scripts/tar_gz_to_zip.py on .tgz corpus
corpus_file = 'dryrun-2019-03.zip'

# inputs
result_dir = '../NIST-SPARQL-Evaluation-v2.3r/M18-data/output/ta2-0531'
out_dir = 'output/0531/ta2'

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
    os.makedirs(out_dir, exist_ok=True)


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

                    if 'AIDA_TA2_ZH' in file:
                        with open(ttl_out_dir + '/' + file + '.html', 'w') as out_file:
                            out_file.write(html_header)
                            out_file.write(file)
                            out_file.write('<table>')
                            out_file.write('''
                            <tr>
                                <th>docid</th>
                                <th>query_link_target</th>
                                <th>link_target</th>
                                <th>cluster</th>
                                <th>infj_span</th>
                                <th>infj_span_context</th>
                                <th>j_cv</th>
                                <th>link_cv</th>
                            </tr>
                            ''')
                            for row in reader:

                                # get informative mention
                                inf_just_span = row['?infj_span']
                                mention_tok, mention_txt = parse_text_from_source(text_justification_lookup, inf_just_pattern, inf_just_span)

                                # write output
                                out_file.write('''
                                <tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                </tr>
                                ''' % (row['?docid'],
                                       row['?query_link_target'],
                                       row['?link_target'],
                                       row['?cluster'][1:-1],
                                       mention_tok,
                                       mention_txt,
                                       row['?j_cv'],
                                       row['?link_cv'])
                                )
                            out_file.write('<table></body><html>')
                    elif 'AIDA_TA2_GR' in file:
                        with open(ttl_out_dir + '/' + file + '.html', 'w') as out_file:
                            out_file.write(html_header)
                            out_file.write(file)
                            out_file.write('<table>')
                            out_file.write('''
                            <tr>
                                <th>docid</th>
                                <th>edge_type_q</th>
                                <th>olink_target_q</th>
                                <th>result</th>
                             </tr>
                             ''')
                            for row in reader:
                                # get informative mention
                                oinf_j_span = row['?oinf_j_span']
                                ej_span = row['?ej_span']
                                oinf_mention_tok, oinf_mention_txt = parse_text_from_source(text_justification_lookup,
                                                                                            inf_just_pattern,
                                                                                            oinf_j_span)
                                ej_mention_tok, ej_mention_txt = parse_text_from_source(text_justification_lookup,
                                                                                        inf_just_pattern, ej_span)

                                result = '''
                                <ul>
                                <li><b>edge_type</b>: %s</li>
                                <li><b>olink_target</b>: %s</li>
                                </ul>
                                <ul>
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
                                <li><b>orfkblink_cv</b>: %s</li>
                                <li><b>oinf_j_cv</b>: %s</li>
                                <li><b>obcm_cv</b>: %s</li>
                                <li><b>edge_cj_cv</b>: %s</li>
                                <li><b>sbcm_cv</b>: %s</li>
                                </ul>
                                ''' % (row['?edge_type'].replace(ldcOnt, 'ldcOnt:')[1:-1],
                                       row['?olink_target'],
                                       row['?subject_cluster'][1:-1],
                                       row['?subjectmo'][1:-1],
                                       ej_mention_tok,
                                       ej_mention_txt,
                                       row['?object_cluster'][1:-1],
                                       row['?objectmo'][1:-1],
                                       oinf_mention_tok,
                                       oinf_mention_txt,
                                       row['?orfkblink_cv'],
                                       row['?oinf_j_cv'],
                                       row['?obcm_cv'],
                                       row['?edge_cj_cv'],
                                       row['?sbcm_cv']
                                       )
                                out_file.write('''
                                <tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                </tr>
                                ''' % (row['?docid'],
                                       row['?edge_type_q'].replace(ldcOnt, 'ldcOnt:')[1:-1],
                                       row['?olink_target_q'],
                                       result)
                                )
                            out_file.write('</table></body></html>')

