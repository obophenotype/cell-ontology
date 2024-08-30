import pandas as pd
cg_desc = pd.read_excel('./CellGuide Validated Descriptions for CL Review.xlsx')
cg_desc.fillna('', inplace=True)
rows = []
for i,r in cg_desc.iterrows():
    if not (r['For CL inclusion'] == 1):
        next
    row = {'defined_class': r['CL ID'], 'CL_short_form': str(r['CL ID']).replace(':', '_'),
           'desc': r["Final version (QC'd)"], 'pubs': ''}
    pub_list = []
    for k,v in r.items():
            if str(k).startswith('Supporting'):
               if str(v).startswith('http'):
                   pub_list.append(v)
               elif(v):
                   pub_list.append('DOI:' + v)
    row['pubs'] = '|'.join(pub_list)
    rows.append(row)
out = pd.DataFrame.from_records(rows)
out.to_csv('../../default/ExtendedDescription.tsv', sep='\t', index=False)