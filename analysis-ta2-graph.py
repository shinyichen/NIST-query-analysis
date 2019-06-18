import sys
import os
import re

# inputs
query_dir = '../NIST-SPARQL-Evaluation-v2.3r/M18-data/queries/task2_graph_queries'
outdir = 'output/0531'
if not os.path.exists(outdir):
    os.mkdir(outdir)

pattern_entry_point = 'BIND \\(\\"(.*)\\" AS \\?olink_target_q\\)'
pattern_edge_type = 'BIND \\((.*) AS \\?edge_type_q\\)'
file_entry_point = {}
file_edge_type = {}
for file in os.listdir(query_dir):
    path = query_dir + '/' + file
    if os.path.isfile(path):
        for i, line in enumerate(open(path)):
            match1 = re.search(pattern_entry_point, line)
            match2 = re.search(pattern_edge_type, line)
            if match1:
                file_entry_point[file] = match1.group(1)
            if match2:
                file_edge_type[file] = match2.group(1)
            if file in file_entry_point and file in file_edge_type:
                break

pattern_line = '^\\| (AIDA_TA2_GR_.+\\.rq)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|\\s*([^\\s]+)\\s*\\|'
with open('ta2-graph.txt') as f:
    with open(outdir + '/ta2-graph-summary.csv', 'w') as out:
        out.write('Query,EntryPoint,EdgeType,Category,Time,Results\n')
        for line in f:
            match = re.search(pattern_line, line)
            if match:
                query = match.group(1)
                entry_point = file_entry_point[query]
                edge_type = file_edge_type[query]
                cat = match.group(2)
                time = match.group(3)
                res = match.group(4)
                out.write(','.join([query, entry_point, edge_type, cat, time, res]) + '\n')
