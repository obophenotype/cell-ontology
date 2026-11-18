"""Filter the OAK diff "Nodes obsoleted without replacement" section.

`runoak diff` lists every obsoleted term that has no `term replaced by`
(IAO:0100001) under "Nodes obsoleted without replacement". An obsolete term
that has one or more `consider` tags still points users to other terms, so it
should not be flagged there. This script removes those terms from that section
and fixes the count in its header. If no terms are left, the whole section is
removed. See https://github.com/obophenotype/cell-ontology/issues/3873
"""
import argparse
import re

SECTION_TITLE = "Nodes obsoleted without replacement"
SECTION_RE = re.compile(
    r"<details>\s*\n<summary>" + re.escape(SECTION_TITLE) + r": \d+</summary>\n"
    r"(?P<body>.*?)</details>\n?",
    re.DOTALL,
)
CURIE_RE = re.compile(r"\(([A-Za-z][\w.]*:[\w.]+)\)\s*\|\s*$")
IRI_RE = re.compile(r"http://purl\.obolibrary\.org/obo/([A-Za-z][\w.]*)_(\w+)")


def terms_with_consider(obo_path):
    """Return the set of term IDs that have at least one consider tag."""
    ids = set()
    current_id = None
    with open(obo_path, encoding="utf-8") as obo:
        for line in obo:
            if line.startswith("["):
                current_id = None
            elif line.startswith("id: "):
                current_id = line[4:].strip()
            elif line.startswith("consider: ") and current_id:
                ids.add(current_id)
    return ids


def row_curie(row):
    """Extract the term CURIE from a markdown table row, or None."""
    match = CURIE_RE.search(row)
    if match:
        return match.group(1)
    match = IRI_RE.search(row)
    if match:
        return f"{match.group(1)}:{match.group(2)}"
    return None


def filter_section(markdown, consider_ids):
    """Rewrite the section, dropping rows for terms that have a consider tag."""
    match = SECTION_RE.search(markdown)
    if not match:
        return markdown

    header, rows = [], []
    for line in match.group("body").splitlines():
        if line.startswith("|") and row_curie(line) is not None:
            if row_curie(line) not in consider_ids:
                rows.append(line)
        elif line.strip():
            header.append(line)

    if rows:
        new_section = (
            f"<details>\n<summary>{SECTION_TITLE}: {len(rows)}</summary>\n\n"
            + "\n".join(header + rows)
            + "\n\n</details>\n"
        )
    else:
        new_section = ""
    return markdown[: match.start()] + new_section + markdown[match.end():]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--diff", required=True, help="OAK diff markdown file, edited in place")
    parser.add_argument("--obo", required=True, help="OBO file of the new release")
    args = parser.parse_args()

    with open(args.diff, encoding="utf-8") as diff_file:
        markdown = diff_file.read()
    filtered = filter_section(markdown, terms_with_consider(args.obo))
    with open(args.diff, "w", encoding="utf-8") as diff_file:
        diff_file.write(filtered)


if __name__ == "__main__":
    main()
