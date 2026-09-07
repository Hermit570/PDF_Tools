# PDF Tools

`merge_pdf.py` 自動讀取指定資料夾內的 PDF，依檔名前的數字排序，合併成一份 `merged.pdf`。適合將以 `01_XXX.pdf`、`02_XXX.pdf` 等格式命名的章節或文件依序整合。

## 安裝

請先安裝 Python，並在使用的 Python 環境中安裝 `pypdf`：

```powershell
python -m pip install pypdf
```

## 使用方式

在終端機切換到 `merge_pdf.py` 所在目錄後執行。

### 合併程式所在資料夾的 PDF

```powershell
python merge_pdf.py
```

未指定路徑時，讀取的是程式所在資料夾。

### 合併指定資料夾的 PDF

```powershell
python merge_pdf.py "C:\Documents\PDFs"
```

也可以使用相對於終端機目前工作目錄的路徑：

```powershell
python merge_pdf.py ".\PDFs"
```

路徑包含空白時，請使用雙引號包住路徑。

### 查看指令說明

```powershell
python merge_pdf.py --help
```

## 排序規則

- 以「數字加底線」開頭的檔名優先，依數字大小排序，例如 `01_Introduction.pdf`、`02_Content.pdf`、`10_Appendix.pdf`。
- 數字不必補零，`2_Content.pdf` 也會排在 `10_Appendix.pdf` 前面。
- 編號相同時，依完整檔名排序，忽略大小寫。
- 不符合編號格式的 PDF 仍會合併，依檔名排序後放在編號檔案之後，忽略大小寫。
- 每份 PDF 內的頁面維持原有順序。

## 範例

假設指定資料夾包含：

```text
PDFs/
├── 10_Appendix.pdf
├── 02_Content.pdf
├── 01_Introduction.pdf
└── Notes.pdf
```

執行後，合併順序為：

```text
01_Introduction.pdf → 02_Content.pdf → 10_Appendix.pdf → Notes.pdf
```

結果儲存為該資料夾內的 `merged.pdf`。終端機會顯示加入的檔名、合併檔案數量及輸出路徑；程式訊息為英文。

## 注意事項

- 僅讀取指定資料夾內的檔案，不包含子資料夾。
- 支援 `.pdf`、`.PDF` 等不同大小寫的副檔名。
- 輸出檔名固定為 `merged.pdf`，既有的同名輸出檔會被排除，避免重複合併。
- 合併時會覆寫既有的 `merged.pdf`；需要保留舊結果時，請先重新命名或備份。
- 原始輸入 PDF 不會被修改。
- 若沒有可合併的 PDF，程式會顯示訊息並結束，不產生新檔案。
- 指定路徑不存在或不是資料夾時，程式會拋出錯誤。
- 程式未提供密碼輸入或損壞檔案略過功能；遇到無法讀取的 PDF 時，合併可能中止並顯示錯誤。
