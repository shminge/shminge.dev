import shutil
import utils
from pathlib import Path
import logging
import re
import config


def parse_page(file: Path):
    print(f"Parsing {file}")

    page_content = file.read_text()

    for name, data in components.items():
        params, content = data
        block_pattern = r"<" + name + " (.*)/*>"
        multi_pattern = re.compile(r"<"+ name + "(.*?)>(.*?)</"+name+">", re.DOTALL)


        def block_substituter(match):
            param_values = utils.parse_args(match.group(1))

            return utils.render_component(content, param_values)

        def multi_substituter(match):
            param_values = utils.parse_args(match.group(1))
            param_values["inner"] = match.group(2)

            return utils.render_component(content, param_values)
        
        for i in range(config.MAX_RECURSION):
            new_content = re.sub(multi_pattern, multi_substituter, page_content)

            if new_content == page_content:
                break
            page_content = new_content
        

        for i in range(config.MAX_RECURSION):
            new_content = re.sub(block_pattern, block_substituter, page_content)
            if new_content == page_content:
                break
            page_content = new_content

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