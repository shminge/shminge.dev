import json
import textwrap
import config
from config import GLOBAL_PARAMS
from pathlib import Path
import logging
import re


# returns the folder needed
def get_folder(folder_name: str) -> str:
    match folder_name:
        case "components":
            return config.ROOT + config.COMPONENTS
        case "source":
            return config.ROOT + config.SOURCE
        case "output":
            return config.ROOT + config.OUTPUT
        case _:
            raise Exception(f"Invalid folder: {folder_name}")


# gathers all components from the defined folder
def gather_components() -> dict[str, tuple[list[str], str]]:
    components: dict[str, tuple[list[str], str]] = {}

    components_dir = Path(get_folder("components"))
    for file in components_dir.iterdir():
        if file.is_file():
            if file.suffix == ".html":
                components[file.stem] = read_component(file)
            else:
                logging.warning(
                    f"  Skipping non-html component {(file.stem, file.suffix)}"
                )
        else:
            logging.warning(f"  Skipping non-file {file.stem}")

    return components


# sets up the given component
def read_component(file: Path) -> tuple[list[str], str]:
    param_pattern = r"@param (.*)"
    content = file.read_text()

    params = re.findall(param_pattern, content)

    if params:
        parts = content.split("-->", 1)

        if len(parts) <= 1:
            raise Exception(f"Component {file.stem} malformed")

        content = parts[1].lstrip()

    return (params, content)


# parses the component with the given values
def render_component(raw_data: str, substitutions: dict[str, str], flags: list[str]) -> str:
    # </if> flags first

    if_pattern = re.compile(r'<if (\w+)>(.*?)<\/if>', re.DOTALL)

    def if_repl(match):
        flag = match.group(1)
        content = match.group(2)

        if flag in flags:
            return content
        else:
            return ''
        
    raw_data = re.sub(if_pattern, if_repl, raw_data)


    # we need to perform the json evals

    json_pattern = r"""\$json\(['"](.*?)['"]\)"""

    def json_replace(match):
        return eval_to_json(match.group(1))

    raw_data = re.sub(json_pattern, json_replace, raw_data)


    pattern = r"\$(\w+)"


    def replacer(match) -> str:
        key = match.group(1)
        val = substitutions.get(key, None)
        if val is not None:
            return val
        elif (val2 := config.GLOBAL_PARAMS["current_metadata"].get(key, None)) is not None:
            return val2
        logging.warning(f"  Failed to replace component ${key}")
        return "!!INVALID!!"

    return re.sub(pattern, replacer, raw_data)


# parses `key="value"` pairs
def parse_args(arg_string: str) -> dict[str, str]:

    pattern = r'(\w+)="([^"]*)"'

    matches = re.findall(pattern, arg_string)
    return dict(matches)

def parse_flags(arg_string: str) -> list[str]:
    pattern = r'(?:^|\s)(\w+)(?=\s|$)'

    matches = re.findall(pattern, arg_string)
    return matches


#### SUBSTITUTIONS ####

# parse markdown (if config has it turned on)



def identity(page_content):
    return page_content


parse_markdown = identity

if config.PARSE_MD:
    import markdown_it

    md_pattern = re.compile(r"<md>(.*?)</md>", re.DOTALL)
    md = markdown_it.MarkdownIt("commonmark")

    def parse_md(page_content):
        return re.sub(
            md_pattern, lambda m: md.render(textwrap.dedent(m.group(1))), page_content
        )

    parse_markdown = parse_md


# markdown links
link_pattern = re.compile(
    r"\[\[(?P<local_link>[^\]\|\n]+)(?:\|(?P<local_title>[^\]\n]*))?]]"
    r"|\[(?P<external_title>[^\]]+)\]\((?P<external_link>[^)]+)\)"
)


def link_substituter(match):
    gd = match.groupdict()

    if gd["local_link"]:
        link = gd["local_link"]
        title = gd["local_title"] or gd["local_link"]

    else:  # external link
        link = "https://" + gd["external_link"]
        title = gd["external_title"]

    return f'<a href="{link}">{title}</a>'


def parse_links(content):
    return re.sub(link_pattern, link_substituter, content)


# inline components


def parse_inline(page_content, name, component_content):
    block_pattern = re.compile(r"<" + name + "(.*?)/>", re.DOTALL)

    def block_substituter(match):
        param_values = parse_args(match.group(1))
        flag_values = parse_flags(match.group(1))
        return render_component(component_content, param_values, flag_values)

    for i in range(config.MAX_RECURSION):
        new_content = re.sub(block_pattern, block_substituter, page_content)
        if new_content == page_content:
            break
        page_content = new_content

    return page_content


# mutli-line components (with $inner content)


def parse_multi(page_content, name, component_content):

    multi_pattern = re.compile(r"<" + name + "(.*?)>(.*?)</" + name + ">", re.DOTALL)

    def multi_substituter(match):
        param_values = parse_args(match.group(1))
        flag_values = parse_flags(match.group(1))
        param_values["inner"] = match.group(2)

        return render_component(component_content, param_values, flag_values)

    for i in range(config.MAX_RECURSION):
        new_content = re.sub(multi_pattern, multi_substituter, page_content)

        if new_content == page_content:
            break
        page_content = new_content

    return page_content

def get_page_metadata(page: Path):
    page_content = page.read_text()
    match = re.findall(r"@(\w+) (.*?)$", page_content, re.MULTILINE)
    return dict(match)



if config.GENERATE_RSS:
    from datetime import datetime
    
    def get_page_info(page: Path):
        page_content = page.read_text()

        title_match = re.search(r"@title (.*?)$", page_content, re.MULTILINE)
        
        if title_match:
            date_match = re.search(r"@pubdate (.*?)$", page_content, re.MULTILINE)
            desc_match = re.search(r"@desc (.*?)$", page_content, re.MULTILINE)

            if date_match and desc_match:
                title = title_match.group(1)

                dt = date_match.group(1)
                date = datetime.strptime(dt, "%Y-%m-%d").strftime("%a, %d %b %Y %H:%M:%S +0000")

                desc = desc_match.group(1)

                # Convert page Path to URL
                root_path = Path(config.ROOT).resolve()
                source_path = (root_path / config.SOURCE.strip("/")).resolve()
                link_relative = page.resolve().relative_to(source_path)
                url = config.SITE_ROOT.rstrip("/") + "/" + str(link_relative).replace("\\", "/")

                link = url
                guid = url

                logging.info(f"{page} prepared for RSS as {url}")
            
                return {
                    "title": title,
                    "pubDate": date,
                    "description": desc,
                    "link": link,
                    "guid": guid,
                    "relativeLink": str(link_relative).replace("\\", "/")
                }


def eval_to_json(eval_str):
    return "'"+json.dumps(eval(eval_str))+"'"



def build_sitemap():
    header = """<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Page Title</title>
                </head>
                <body>
                <ul>"""
    footer = """</ul>
                </body>
                </html>"""
    content = ""
    for p in config.GLOBAL_PARAMS["sitemap"]:
        content += f'<li><a href="{p}">{p}</a></li>\n'

    path = Path(get_folder("output")+"/sitemap.html")
    path.write_text(header+content+footer, encoding="utf-8")