import bibtexparser

def format_authors(author_str: str):
    authors = [a.strip() for a in author_str.split("and")]
        
    if len(authors) > 1:
        return f"{', '.join(authors[:-1])}, and {authors[-1]}"
    else:
        return authors[0]
    
def format_title(title: str):
    characters_to_remove = [
        "{",
        "}"
    ]

    for character in characters_to_remove:
        title = title.replace(character, "")

    return title

def main():
    with open("./publications.bib", "r") as f:
        entries = bibtexparser.load(f).entries

    with open("./publications.md", "w") as page_content:
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
                f'{format_authors(entry["author"])}, "**{format_title(entry["title"])}**"',
                "\n"
            ])

    with open("./publications.md", "r") as page_content:
        print("Publications page generated with content:")
        print("\n".join(page_content.readlines()))

if __name__ == "__main__":
    main()