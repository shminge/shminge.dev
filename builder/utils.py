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
            if file.suffix == '.html':
                components[file.stem] = read_component(file)
            else:
                logging.warning(f"Skipping non-html component {(file.stem, file.suffix)}")
        else:
            logging.warning(f"Skipping non-file {file.stem}")
    
    return components


# sets up the given component
def read_component(file: Path) -> tuple[list[str], str]:
    param_pattern = r"@param (.*)"
    content = file.read_text()

    params = re.findall(param_pattern, content)

    if params:
        parts = content.split('-->', 1)

        if len(parts) <= 1:
            raise Exception(f"Component {file.stem} malformed")

        content = parts[1].lstrip()

    return (params, content)

# parses the component with the given values
def render_component(raw_data: str, substitutions: dict[str, str]) -> str:
    pattern = r"\$(\w+)"

    def replacer(match) -> str:
        key = match.group(1)
        return substitutions.get(key, "!!Invalid!!")

    return re.sub(pattern, replacer, raw_data)



# parses `key="value"` pairs
def parse_args(arg_string: str) -> dict[str, str]:
    
    pattern = r'(\w+)="([^"]*)"'

    matches = re.findall(pattern, arg_string)
    return dict(matches)
