import sys
import os
import pathlib 
import logging
import difflib
from typing import List, Dict, Optional
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

def get_config_file_pairs(path_config: str) -> Dict[str,str]:
    config_file_pairs = { str(path): os.path.join("/", path.relative_to(path_config)) for path in pathlib.Path(path_config).rglob('*') if os.path.isfile(path) }
    logging.debug(f"config_file_pairs=({config_file_pairs})")
    return config_file_pairs

def compare_config_file_pairs(config_file_pairs: Dict[str,str]):
    for path_src, path_dst in config_file_pairs.items():
        if not os.path.isfile(path_src):
            logging.warning(f"file path_src=({path_src}) not found")
            continue
        if not os.path.isfile(path_dst):
            logging.warning(f"file path_dst=({path_dst}) not found")
            continue
        print_file_pair_diff(path_src, path_dst)

def print_file_pair_diff(path_src: str, path_dst: str):
    with open(path_src, 'r') as f_src, open(path_dst, 'r') as f_dst:
        lines_src = f_src.readlines()
        lines_dst = f_dst.readlines()
    diff = list(difflib.unified_diff(lines_src, lines_dst))
    if diff:
        print(f"Files differ: path_src=({path_src}), path_dst=({path_dst})")
        print(''.join(diff))
    else:
        print(f"Files match: path_src=({path_src}), path_dst=({path_dst})")



path_home = os.getenv("HOME")
if not os.path.isdir(path_home):
    raise FileNotFoundError(f"path_home=({path_home}) not found")
logging.debug(f"path_home=({path_home})")

path_config = os.path.join(path_home, "_mld", "macOS")
if not os.path.isdir(path_config):
    raise FileNotFoundError(f"path_config=({path_config}) not found")
logging.debug(f"path_config=({path_config})")


if __name__ == '__main__':
    config_file_pairs = get_config_file_pairs(path_config)
    compare_config_file_pairs(config_file_pairs)

