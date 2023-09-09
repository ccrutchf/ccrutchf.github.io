from typing import Callable, Dict

import bibtexparser

def format_authors(author_str: str):
    authors = [a.strip() for a in author_str.split("and")]
        
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

def format_entry(entry: Dict[str, str]):
    if entry["ENTRYTYPE"] not in ENTRY_FORMATTERS:
        raise ValueError(f'"{entry["ENTRYTYPE"]}" is a supported publication type.')

    return ENTRY_FORMATTERS[entry["ENTRYTYPE"]](entry)

def main():
    with open("./publications.bib", "r") as f:
        entries = bibtexparser.load(f).entries

    with open("./publications.md", "w") as page_content:
        page_content.writelines([
            "---\n",
            "layout: page\n",
            "title: Publications\n",
            "subtitle:\n",
            "---\n",
            "\n",
            "[Bibtex](/publications.bib) [Google Scholar](https://scholar.google.com/citations?user=n0ZF9EcAAAAJ&hl=en) [ORCiD](https://orcid.org/0000-0002-2011-721X)\n"
        ])

        for entry in entries:
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
    "mastersthesis": format_masters_thesis
}

if __name__ == "__main__":
    main()