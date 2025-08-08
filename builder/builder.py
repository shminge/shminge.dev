import shutil
import utils
from pathlib import Path
import logging
import re


def parse_page(file: Path):

    page_content = file.read_text()

    for name, data in components.items():
        params, content = data
        pattern = r"<" + name + " (.*)/*>"


        def substituter(match):
            param_values = utils.parse_args(match.group(1))

            return utils.render_component(content, param_values)
        
        page_content = re.sub(pattern, substituter, page_content)
    
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