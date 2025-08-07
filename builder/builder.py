import utils
from pathlib import Path
import logging
import re


def parse_page(file: Path):

    page_content = file.read_text()

    for name, data in components.items():
        params, content = data
        pattern = r"<" + name + " (.*)>"


        def substituter(match):
            param_values = utils.parse_args(match.group(1))

            return utils.render_component(content, param_values)
        
        page_content = re.sub(pattern, substituter, page_content)
    
    return page_content





# MAIN LOOP

components = utils.gather_components()


src_dir = Path(utils.get_folder("source"))
output_dir = Path(utils.get_folder("output"))

for file in src_dir.iterdir():
    if file.is_file():
        if file.suffix == '.html':
            new_content = parse_page(file)
            filename = file.stem + file.suffix

            file_path = output_dir / filename

            file_path.write_text(new_content, encoding="utf-8")
        else:
            logging.warning(f"Skipping non-html component {(file.stem, file.suffix)}")
    else:
        logging.warning(f"Skipping non-file {file.stem}")
