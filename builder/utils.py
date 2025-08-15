import textwrap
import config
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
                    f"Skipping non-html component {(file.stem, file.suffix)}"
                )
        else:
            logging.warning(f"Skipping non-file {file.stem}")

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
def render_component(raw_data: str, substitutions: dict[str, str]) -> str:
    pattern = r"\$(\w+)"

    def replacer(match) -> str:
        key = match.group(1)
        return substitutions.get(key) or config.GLOBAL_PARAMS.get(key) or "!!INVALID!!"

    return re.sub(pattern, replacer, raw_data)


# parses `key="value"` pairs
def parse_args(arg_string: str) -> dict[str, str]:

    pattern = r'(\w+)="([^"]*)"'

    matches = re.findall(pattern, arg_string)
    return dict(matches)


#### SUBSTITUTIONS ####

# parse markdown (if config has it turned on)


def identity(page_content):
    return page_content


parse_markdown = identity

if config.PARSE_MD:
    import markdown_it, re, textwrap

    md_pattern = re.compile(r"<md>(.*?)</md>", re.DOTALL)
    md = markdown_it.MarkdownIt("commonmark")

    def parse_md(page_content):
        # Step 1: Extract and protect content within <raw> tags
        raw_pattern = re.compile(r"<raw>(.*?)</raw>", re.DOTALL)
        raw_content = []
        
        def store_raw(match):
            index = len(raw_content)
            raw_content.append(match.group(1))  # Store just the content, not the tags
            return f"__RAW_PLACEHOLDER_{index}__"
        
        # Replace all <raw> content with placeholders
        content_with_raw_protected = re.sub(raw_pattern, store_raw, page_content)
        
        # Step 2: Find and process <md> blocks in the protected content
        def process_md_block(match):
            md_content = match.group(1)
            
            # Step 3: Restore raw content within this md block before rendering
            md_with_raw_restored = md_content
            for i, content in enumerate(raw_content):
                placeholder = f"__RAW_PLACEHOLDER_{i}__"
                md_with_raw_restored = md_with_raw_restored.replace(placeholder, content)
            
            # Step 4: Render the markdown
            return md.render(textwrap.dedent(md_with_raw_restored))
        
        # Process all md blocks
        result = re.sub(md_pattern, process_md_block, content_with_raw_protected)
        
        # Step 5: Restore any remaining raw content that was outside md blocks
        for i, content in enumerate(raw_content):
            placeholder = f"__RAW_PLACEHOLDER_{i}__"
            result = result.replace(placeholder, content)
        
        return result

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
        return render_component(component_content, param_values)

    for i in range(config.MAX_RECURSION):
        new_content = re.sub(block_pattern, block_substituter, page_content)
        if new_content == page_content:
            break
        page_content = new_content

    return page_content


# mutli_line components (with $inner content)


def parse_multi(page_content, name, component_content):

    multi_pattern = re.compile(r"<" + name + "(.*?)>(.*?)</" + name + ">", re.DOTALL)

    def multi_substituter(match):
        param_values = parse_args(match.group(1))
        param_values["inner"] = match.group(2)

        return render_component(component_content, param_values)

    for i in range(config.MAX_RECURSION):
        new_content = re.sub(multi_pattern, multi_substituter, page_content)

        if new_content == page_content:
            break
        page_content = new_content

    return page_content




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

                print(f"{page} added to RSS as {url}")
            
                return {
                    "title": title,
                    "pubDate": date,
                    "description": desc,
                    "link": link,
                    "guid": guid
                }
