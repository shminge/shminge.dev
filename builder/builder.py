import shutil
import utils
from pathlib import Path
import config

global_params = {
    "pages": []
}




def parse_page(file: Path):
    print(f"Parsing {file}")

    page_content = file.read_text()


    if config.PARSE_MD:
        page_content = utils.parse_markdown(page_content)

    if config.PARSE_MD_LINKS:
        page_content = utils.parse_links(page_content)

    for name, data in components.items():
        component_params, component_content = data

        page_content = utils.parse_multi(page_content, name, component_content)

        page_content = utils.parse_inline(page_content, name, component_content)


    return page_content


def process_site(src_dir: Path, output_dir: Path):

    pages_queue = []

    for item in src_dir.rglob("*"):
        relative_path = item.relative_to(src_dir)
        destination = output_dir / relative_path

        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)

            if item.suffix == ".html":
                pages_queue.append((item, destination))

                pg_info = utils.get_page_info(item)

                if pg_info:
                    global_params["pages"].append(pg_info)


            else:
                shutil.copy2(item, destination)
    
    for entry in pages_queue:
        page, destination = entry
        new_content = parse_page(page)
        destination.write_text(new_content, encoding="utf-8")


# MAIN LOOP

components = utils.gather_components()


src_dir = Path(utils.get_folder("source"))
output_dir = Path(utils.get_folder("output"))

process_site(src_dir=src_dir, output_dir=output_dir)

if config.GENERATE_RSS:
    import rss
    rss.build_rss(global_params["pages"])
