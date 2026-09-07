from pypdf import PdfWriter

pdf_files = [
    "file1.pdf",
    "file2.pdf",
    "file3.pdf",
]

output_file = "merged.pdf"

writer = PdfWriter()

for pdf_file in pdf_files:
    writer.append(pdf_file)

writer.write(output_file)
writer.close()

print(f"PDF 合併完成：{output_file}")