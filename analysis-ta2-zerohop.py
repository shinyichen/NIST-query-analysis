import sys
import os
import re

# inputs
query_dir = '../NIST-SPARQL-Evaluation-v2.3r/M18-data/queries/task2_zerohop_queries'
outdir = 'output/0531'
if not os.path.exists(outdir):
    os.mkdir(outdir)

pattern_entry_point = 'BIND \\(\\"(.*)\\" AS \\?query_link_target\\)'
file_entry_point = {}
for file in os.listdir(query_dir):
    path = query_dir + '/' + file
    if os.path.isfile(path):
        for i, line in enumerate(open(path)):
            match = re.search(pattern_entry_point, line)
            if match:
                file_entry_point[file] = match.group(1)
                break

pattern_line = '^\\| (AIDA_TA2_ZH_.+\\.rq)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|'
with open('../NIST-SPARQL-Evaluation-v2.3r/analysis/ta2-zerohop.txt') as f:
    with open(outdir + '/ta2-zerohop-summary.csv', 'w') as out:
        out.write('Query,EntryPoint,Category,Time,Results\n')
        for line in f:
            match = re.search(pattern_line, line)
            if match:
                query = match.group(1)
                entry_point = file_entry_point[query]
                cat = match.group(2)
                time = match.group(3)
                res = match.group(4)
                out.write(','.join([query, entry_point, cat, time, res]) + '\n')
