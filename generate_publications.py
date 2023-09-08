import bibtexparser
from io import StringIO

def format_authors(author_str: str):
    authors = [a.strip() for a in author_str.split("and")]
        
    if len(authors) > 1:
        return f"{', '.join(authors[:-1])}, and {authors[-1]}"
    else:
        return authors[0]

def main():
    with open("./publications.bib", "r") as f:
        entries = bibtexparser.load(f).entries

    with open("./publications.md", "w") as page_content:
    # with StringIO() as page_content:
        page_content.writelines([
            "---\n",
            "layout: page\n",
            "title: Publications\n",
            "subtitle:\n",
            "---\n"
        ])

        for entry in entries:
            page_content.writelines([
                "\n",
                f'{format_authors(entry["author"])}, "*{entry["title"]}*"',
                "\n"
            ])

        # print(page_content.getvalue())

if __name__ == "__main__":
    main()