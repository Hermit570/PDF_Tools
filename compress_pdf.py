import argparse
from pathlib import Path
import shutil
import sys
import tempfile
import pymupdf


def compress_pdf(source, output=None, *, images=False, dpi=150, quality=75):

    source = Path(source).expanduser().resolve()
    output = (Path(output).expanduser().resolve() if output else
              source.with_name(f"{source.stem}_compressed.pdf"))
    if not source.is_file():
        raise ValueError(f"Input file does not exist: {source}")
    if source == output:
        raise ValueError("Input and output must be different files.")
    if output.exists():
        raise ValueError(f"Output already exists: {output}")
    if not output.parent.is_dir():
        raise ValueError(f"Output folder does not exist: {output.parent}")
    if dpi <= 0 or not 1 <= quality <= 100:
        raise ValueError("DPI must be positive; quality must be between 1 and 100.")

    original_size = source.stat().st_size
    # Save to a temporary file first so a failed compression leaves no output.
    with tempfile.TemporaryDirectory(prefix="pdf_compress_", dir=output.parent) as temp:
        candidate = Path(temp) / "compressed.pdf"
        with pymupdf.open(source) as doc:
            if not doc.is_pdf:
                raise ValueError("Input must be a PDF file.")
            if doc.is_encrypted:
                raise ValueError("Password-protected PDFs are not supported.")
            if doc.get_sigflags() > 0:
                raise ValueError("PDF has signature fields; compression may invalidate signatures.")
            if not doc.page_count:
                raise ValueError("PDF contains no pages.")
            if images:
                if not hasattr(doc, "rewrite_images"):
                    raise ValueError("Update PyMuPDF: python -m pip install --upgrade pymupdf")
                doc.rewrite_images(dpi_threshold=int(dpi * 1.5) + 1,
                                   dpi_target=dpi, quality=quality)
            doc.save(candidate, garbage=4, deflate=True,
                     deflate_images=True, deflate_fonts=True, use_objstms=1,
                     encryption=pymupdf.PDF_ENCRYPT_KEEP)

        # If optimization made the file larger, retain the original bytes.
        selected = candidate if candidate.stat().st_size < original_size else source
        with selected.open("rb") as reader:
            with output.open("xb") as writer:
                try:
                    shutil.copyfileobj(reader, writer)
                except BaseException:
                    writer.close()
                    output.unlink(missing_ok=True)
                    raise

    final_size = output.stat().st_size
    print(f"Output: {output}")
    print(f"Size: {original_size:,} -> {final_size:,} bytes")
    print(f"Saved: {(1 - final_size / original_size) * 100:.1f}%")
    if final_size == original_size:
        print("No size reduction; copied the original PDF unchanged.")
    return output


def main():
    parser = argparse.ArgumentParser(description="Reduce PDF size (lossless by default).")
    parser.add_argument("input", help="Input PDF path")
    parser.add_argument("-o", "--output", help="Output path (default: INPUT_compressed.pdf)")
    parser.add_argument("--images", action="store_true", help="Recompress images with quality loss")
    parser.add_argument("--dpi", type=int, default=150, help="Target image DPI with --images (default: 150)")
    parser.add_argument("--quality", type=int, default=75, help="JPEG quality 1-100 with --images (default: 75)")
    args = parser.parse_args()
    if not args.images and (args.dpi != 150 or args.quality != 75):
        parser.error("--dpi and --quality require --images")
    try:
        compress_pdf(args.input, args.output, images=args.images,
                     dpi=args.dpi, quality=args.quality)
    except ImportError:
        print("Install dependency: python -m pip install --upgrade pymupdf", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
