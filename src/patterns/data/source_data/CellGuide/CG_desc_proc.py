import pandas as pd

cg_desc = pd.read_excel("./CellGuide Validated Descriptions for CL Review.xlsx")
cg_desc.fillna("", inplace=True)
rows = []
rejects = 0
for i, r in cg_desc.iterrows():
    print(bool(r["For CL inclusion"]))
    if not (r["For CL inclusion"]):
        if r["For CL inclusion"] == 0:
            rejects += 1
        continue
    row = {
        "defined_class": r["CL ID"],
        "cell": r["CL ID"],
        "CL_short_form": str(r["CL ID"]).replace(":", "_"),
        "desc": r["Final version (QC'd)"],
        "pubs": "",
    }
    pub_list = []
    for k, v in r.items():
        if str(k).startswith("Supporting"):
            if str(v).startswith("http"):
                pub_list.append(v)
            elif v:
                pub_list.append("DOI:" + v)
    row["pubs"] = "|".join(pub_list)
    rows.append(row)
print("Added %d extended defs" % len(rows))
print("Rejected descriptions %d" % rejects)
out = pd.DataFrame.from_records(rows)
out.to_csv("../../default/ExtendedDescription.tsv", sep="\t", index=False)
