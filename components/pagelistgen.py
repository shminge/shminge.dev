from datetime import datetime

def render(params, **kwargs):
    pages = params["pages"]
    has_text = kwargs["has"]
    max_posts = kwargs["maxposts"]
    entries = []

    # collect matching pages
    for page in pages:
        if has_text in page["link"]:
            entry = {
                "content": f'<li><a href="{page["link"]}">{page["title"]}</a></li>',
                "date": page["pubDate"],
            }
            entries.append(entry)

    # sort by date (newest first)
    entries.sort(key=lambda e: datetime.strptime(e["date"], "%a, %d %b %Y %H:%M:%S %z"), reverse=True)

    if max_posts > 0:
        entries = entries[:max_posts]

    # build string
    result_lines = []
    for entry in entries:
        result_lines.append(entry["content"])

    return "\n".join(result_lines)