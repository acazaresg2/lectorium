from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED
import shutil

ROOT = Path(__file__).resolve().parents[1]

SOURCE = ROOT / "scripts" / "lab-book-source"
OUTPUT = ROOT / "assets" / "fixtures" / "lab-book.epub"

REQUIRED = [
    SOURCE / "mimetype",
    SOURCE / "META-INF" / "container.xml",
    SOURCE / "OEBPS" / "content.opf",
    SOURCE / "OEBPS" / "nav.xhtml",
    SOURCE / "OEBPS" / "styles.css",
    SOURCE / "OEBPS" / "Text" / "chapter1.xhtml",
    SOURCE / "OEBPS" / "Text" / "chapter2.xhtml",
    SOURCE / "OEBPS" / "Text" / "chapter3.xhtml",
    SOURCE / "OEBPS" / "Images" / "cover.svg",
    SOURCE / "OEBPS" / "Images" / "key.svg",
]

for path in REQUIRED:
    if not path.exists():
        raise FileNotFoundError(f"Missing EPUB source file: {path}")

mime = (SOURCE / "mimetype").read_text(encoding="utf-8")

if mime != "application/epub+zip":
    raise ValueError("mimetype must contain exactly application/epub+zip")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

if OUTPUT.exists():
    OUTPUT.unlink()

with ZipFile(OUTPUT, "w") as epub:
    # EPUB requirement: first entry and uncompressed.
    epub.writestr(
        "mimetype",
        mime,
        compress_type=ZIP_STORED,
    )

    for source_file in REQUIRED[1:]:
        relative = source_file.relative_to(SOURCE)
        epub.write(
            source_file,
            relative.as_posix(),
            compress_type=ZIP_DEFLATED,
        )

print(f"Created: {OUTPUT}")
