import os
import re

# inputs
outdir = 'output/cmu'
result_file = '../NIST-SPARQL-Evaluation-v2.3r/analysis/ta1-class-cmu.txt'
query_dir = '../NIST-SPARQL-Evaluation-v2.3r/M18-data/queries/task1_class_queries'

if not os.path.exists(outdir):
    os.mkdir(outdir)


pattern_ta1_class = 'BIND\\s*\\((.+) AS \\?query_type\\)'
ta1_class = {}
for file in os.listdir(query_dir):
    path = query_dir + '/' + file
    if os.path.isfile(path):
        for i, line in enumerate(open(path)):
            match = re.search(pattern_ta1_class, line)
            if match:
                ta1_class[file] = match.group(1)
                break

pattern_line = '^\\| (AIDA_TA1_CL_.+\\.rq)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|'
with open(result_file) as f:
    with open(outdir + '/ta1-class-summary.csv', 'w') as out:
        out.write('Query,Description,Category,Time,Results\n')
        for line in f:
            match = re.search(pattern_line, line)
            if match:
                query = match.group(1)
                desc = ta1_class[query]
                cat = match.group(2)
                time = match.group(3)
                res = match.group(4)
                out.write(','.join([query, desc, cat, time, res]) + '\n')
