import argparse
import re
from pathlib import Path
from pypdf import PdfWriter

def pdf_sort_key(path):
    """Sort by the numeric filename prefix, placing other filenames last."""
    match = re.match(r"^(\d+)_", path.stem)
    if match:
        return (0, int(match.group(1)), path.name.casefold())
    return (1, 0, path.name.casefold())


def merge_pdfs(folder):
    folder = Path(folder).expanduser().resolve()
    if not folder.is_dir():
        raise NotADirectoryError(f"Folder does not exist or is not a directory: {folder}")

    output_file = folder / "merged.pdf"
    pdf_files = sorted(
        (
            path for path in folder.iterdir()
            if path.is_file()
            and path.suffix.lower() == ".pdf"
            and path.resolve() != output_file.resolve()
        ),
        key=pdf_sort_key,
    )
    if not pdf_files:
        print(f"No PDF files to merge in folder: {folder}")
        return

    writer = PdfWriter()
    try:
        for pdf_file in pdf_files:
            print(f"Adding: {pdf_file.name}")
            writer.append(str(pdf_file))
        writer.write(str(output_file))
    finally:
        writer.close()

    print(f"Merged {len(pdf_files)} PDF files: {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Merge PDFs in a folder by numeric filename order")
    parser.add_argument(
        "folder", nargs="?", default=Path(__file__).resolve().parent,
        help="Folder containing PDFs (defaults to the script folder; excludes subfolders)",
    )
    args = parser.parse_args()
    merge_pdfs(args.folder)
