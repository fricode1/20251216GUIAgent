import pymupdf4llm

md_text = pymupdf4llm.to_markdown(r"data\人类理解论第二卷\locke1690book2.pdf")

# now work with the markdown text, e.g. store as a UTF8-encoded file
import pathlib
pathlib.Path("output.md").write_bytes(md_text.encode())