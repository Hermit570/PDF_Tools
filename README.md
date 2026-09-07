# PDF Tools

`merge_pdf.py` 自動讀取指定資料夾內的 PDF，依檔名前的數字排序，合併成一份 `merged.pdf`。適合將以 `01_XXX.pdf`、`02_XXX.pdf` 等格式命名的章節或文件依序整合。

`compress_pdf.py` 降低單一 PDF 的檔案大小，預設保留原畫質，也可選擇降低圖片解析度與品質。

## 安裝

請先安裝 Python，並在使用的 Python 環境中安裝依賴。合併程式使用 `pypdf`，壓縮程式使用 `pymupdf`：

```powershell
python -m pip install --upgrade pypdf pymupdf
```

## PDF 合併

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

### 排序規則

- 以「數字加底線」開頭的檔名優先，依數字大小排序，例如 `01_Introduction.pdf`、`02_Content.pdf`、`10_Appendix.pdf`。
- 數字不必補零，`2_Content.pdf` 也會排在 `10_Appendix.pdf` 前面。
- 編號相同時，依完整檔名排序，忽略大小寫。
- 不符合編號格式的 PDF 仍會合併，依檔名排序後放在編號檔案之後，忽略大小寫。
- 每份 PDF 內的頁面維持原有順序。

### 範例

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

### 合併注意事項

- 僅讀取指定資料夾內的檔案，不包含子資料夾。
- 支援 `.pdf`、`.PDF` 等不同大小寫的副檔名。
- 輸出檔名固定為 `merged.pdf`，既有的同名輸出檔會被排除，避免重複合併。
- 合併時會覆寫既有的 `merged.pdf`；需要保留舊結果時，請先重新命名或備份。
- 原始輸入 PDF 不會被修改。
- 若沒有可合併的 PDF，程式會顯示訊息並結束，不產生新檔案。
- 指定路徑不存在或不是資料夾時，程式會拋出錯誤。
- 程式未提供密碼輸入或損壞檔案略過功能；遇到無法讀取的 PDF 時，合併可能中止並顯示錯誤。

## PDF 壓縮

在終端機切換到 `compress_pdf.py` 所在目錄後執行。輸入與輸出可使用絕對路徑，或相對於終端機目前工作目錄的路徑；路徑包含空白時，請使用雙引號包住。

### 保留原畫質

清理未使用及重複物件，並壓縮 PDF 內部資料：

```powershell
python compress_pdf.py "input.pdf"
```

預設輸出為原始檔同資料夾的 `input_compressed.pdf`。

### 降低圖片品質

降低圖片解析度並重新壓縮圖片，以進一步縮小檔案；文字仍保留為文字：

```powershell
python compress_pdf.py "input.pdf" -o "small.pdf" --images --dpi 150 --quality 75
```

### 命令列參數

| 參數 | 說明 | 預設值 |
|---|---|---|
| `input` | 輸入 PDF 路徑，必填 | 無 |
| `-o`、`--output` | 輸出 PDF 路徑 | 原檔名加上 `_compressed.pdf` |
| `--images` | 啟用圖片重新壓縮，可能降低畫質 | 關閉 |
| `--dpi` | 高解析度圖片的目標 DPI，必須大於零，搭配 `--images` 使用 | `150` |
| `--quality` | JPEG 品質，範圍 1–100，搭配 `--images` 使用 | `75` |

只會對超過約 1.5 倍目標 DPI 的圖片進行重採樣；未超過門檻的圖片仍可能重新編碼。JPEG 品質越低，失真通常越明顯。圖片重寫行為參考 [PyMuPDF 文件](https://pymupdf.readthedocs.io/en/latest/document.html#Document.rewrite_images)。

查看完整指令說明：

```powershell
python compress_pdf.py --help
```

### 處理流程與結果

程式先檢查路徑、參數與 PDF，再依設定處理圖片，將最佳化結果儲存至暫存檔。比較大小後才建立正式輸出，暫存資料夾會自動清除。

終端機會顯示輸出路徑、處理前後的 bytes 數及縮減百分比；程式訊息為英文。若壓縮結果沒有更小，輸出會改為原始檔的完整副本。已經最佳化的 PDF 不一定能再縮小。

### 壓縮注意事項

- 原始檔不會被修改；輸入與輸出不可為相同路徑。
- 已存在的輸出檔不會被覆蓋，請改用其他檔名。
- 輸出資料夾需事先存在。
- 不處理需密碼解鎖、具有簽章相關標記或沒有頁面的 PDF。
- 預設模式不主動降低圖片畫質，但會重新整理 PDF 內部結構。
- 若圖片模式提示缺少 `rewrite_images`，請執行 `python -m pip install --upgrade pymupdf`。
