import re
from typing import Callable, Dict

import bibtexparser

def format_authors(author_str: str):
    # Split on the BibTeX separator only, so names like "Candelmo" stay intact.
    authors = [a.strip() for a in re.split(r"\s+and\s+", author_str)]
        
    if len(authors) > 1:
        return f"{', '.join(authors[:-1])}, and {authors[-1]}"
    else:
        return authors[0]
    
def format_string(title: str):
    characters_to_remove = [
        "{",
        "}"
    ]

    strings_to_replace = {
        "\\&amp$\\mathsemicolon$": "&"
    }

    for character in characters_to_remove:
        title = title.replace(character, "")

    for key, value in strings_to_replace.items():
        title = title.replace(key, value)

    return title

def format_common(entry: Dict[str, str]):
    return f'{format_authors(entry["author"])}, "**{format_string(entry["title"])}**"'

def format_link(entry: Dict[str, str]):
    return f"([PDF](/assets/pdfs/{entry['file'][1:-4]}))"

def format_date(entry: Dict[str, str]):
    return f"{entry['month']} {entry['year']}"

def format_article(entry: Dict[str, str]):
    return f"{format_common(entry)}, *{format_string(entry['journal'])}*, Vol. {entry['volume']}, No. {entry['number']}, Pages {entry['pages'].replace('--', '-')}, {format_date(entry)} {format_link(entry)}"

def format_in_proceedings(entry: Dict[str, str]):
    return f"{format_common(entry)}, *{format_string(entry['booktitle'])}*, {format_date(entry)} {format_link(entry)}"

def format_masters_thesis(entry: Dict[str, str]):
    return f"{format_common(entry)}, MS Thesis, Department of Electrical and Computer Engineering, {entry['school']}, {format_date(entry)} {format_link(entry)}"

def format_patent(entry: Dict[str, str]):
    return f"{format_common(entry)}, {entry['type']} {entry['number']}, {format_date(entry)} {format_link(entry)}"

def format_unpublished(entry: Dict[str, str]):
    links = []
    if "file" in entry:
        links.append(f"[PDF](/assets/pdfs/{entry['file'][1:-4]})")
    if "doi" in entry:
        links.append(f"[Preprint](https://doi.org/{entry['doi']})")
    link_text = f" ({', '.join(links)})" if links else ""

    return f"{format_common(entry)}, {entry['note']}, {entry['year']}{link_text}"

def format_entry(entry: Dict[str, str]):
    if entry["ENTRYTYPE"] not in ENTRY_FORMATTERS:
        raise ValueError(f'"{entry["ENTRYTYPE"]}" is a supported publication type.')

    return ENTRY_FORMATTERS[entry["ENTRYTYPE"]](entry)

def main():
    with open("./publications.bib", "r") as f:
        # Keep entry types bibtexparser 1.x does not consider standard (e.g. @Patent).
        parser = bibtexparser.bparser.BibTexParser(ignore_nonstandard_types=False)
        entries = bibtexparser.load(f, parser=parser).entries

    with open("./publications.md", "w") as page_content:
        page_content.writelines([
            "---\n",
            "layout: page\n",
            "title: Publications\n",
            "subtitle:\n",
            "---\n",
        ])

        sections = [
            ("In Submission", [e for e in entries if e["ENTRYTYPE"] == "unpublished"]),
            ("Published", [e for e in entries if e["ENTRYTYPE"] != "unpublished"]),
        ]

        for heading, section_entries in sections:
            if not section_entries:
                continue

            page_content.writelines(["\n", f"## {heading}\n"])

            for entry in section_entries:
                page_content.writelines([
                    "\n",
                    format_entry(entry),
                    "\n"
                ])

    with open("./publications.md", "r") as page_content:
        print("Publications page generated with content:")
        print("\n".join(page_content.readlines()))

ENTRY_FORMATTERS: Dict[str, Callable] = {
    "article": format_article,
    "inproceedings": format_in_proceedings,
    "mastersthesis": format_masters_thesis,
    "patent": format_patent,
    "unpublished": format_unpublished
}

if __name__ == "__main__":
    main()