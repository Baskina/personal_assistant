import shutil
from pathlib import Path

from .normalize import normalize
from .scan import scan, categories


def main(path):
    """
    Scans the specified directory and performs operations on the files.

    Args:
        path: The path to the directory to be scanned.
    """

    # Scan the directory
    scan(path)
    for category, files in categories.items():
        category_dir = path / category
        category_dir.mkdir(exist_ok=True)

        for file in files:
            new_path = normalize(file.name)
            file.replace(path / category / new_path)

    # Check if the directory is empty and delete it if it is
    scan(path)

    # Iterate over each category and process its files
    arch_path = Path(path / "archives")
    for arch in arch_path.iterdir():
        shutil.unpack_archive(arch, arch_path / arch.stem)
        arch.unlink()

        # Check if the directory is empty and delete it if it is
        scan(arch_path)
