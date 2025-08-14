import shutil
import utils
from pathlib import Path
import logging
import re
import config


def parse_page(file: Path):
    print(f"Parsing {file}")

    page_content = file.read_text()


    page_content = utils.parse_links(page_content)

    for name, data in components.items():
        component_params, component_content = data

        page_content = utils.parse_multi(page_content, name, component_content)

        page_content = utils.parse_inline(page_content, name, component_content)


    return page_content


def process_site(src_dir: Path, output_dir: Path):
    for item in src_dir.rglob('*'):
        relative_path = item.relative_to(src_dir)
        destination = output_dir / relative_path

        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)

            if item.suffix == '.html':
                new_content = parse_page(item)
                destination.write_text(new_content, encoding='utf-8')
            else:
                shutil.copy2(item, destination)



# MAIN LOOP

components = utils.gather_components()


src_dir = Path(utils.get_folder("source"))
output_dir = Path(utils.get_folder("output"))

process_site(src_dir=src_dir, output_dir=output_dir)