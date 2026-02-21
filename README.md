# OCR Tool (`images_to_text.py`)

フォルダ内の画像を読み込み、OCR結果を1つのテキストファイルにまとめるスクリプトです。

## できること

- 指定フォルダの画像を一括OCR
- ファイル名に含まれる数字で自然順ソート
  - 例: `page1.png`, `page2.png`, `page10.png`
- 出力先テキストファイルを指定
- 拡張子フィルタを指定
- Tesseract実行ファイルパスを明示指定
- OCR言語指定（例: `jpn`, `eng`, `jpn+eng`）

## 必要環境

- Python 3.8+
- Tesseract OCR（外部バイナリ）
- Pythonパッケージ
  - `pillow`
  - `pytesseract`

依存パッケージのインストール:

```bash
pip install -r requirements.txt
```



### Tesseract（Windows）

Windowsでは通常、以下にインストールされます。

`C:\Program Files\Tesseract-OCR\tesseract.exe`

PATHが通っていない場合は、`--tesseract-cmd` で実行ファイルを指定してください。

## 使い方

Tesseract本体のダウンロード先:

- UB Mannheim版（Windows向け配布）: https://github.com/UB-Mannheim/tesseract/wiki

Windowsでのインストール手順:

1. 上記ページからインストーラー（`.exe`）をダウンロードして実行
2. 既定のインストール先（通常 `C:\Program Files\Tesseract-OCR`）でインストール
3. `tesseract.exe` が見つからない場合は `--tesseract-cmd` にフルパスを指定

`jpn_vert`（日本語縦書き用言語データ）のダウンロード先:

- `jpn_vert.traineddata`: https://github.com/tesseract-ocr/tessdata_best/blob/main/jpn_vert.traineddata

配置先（例）:

- `C:\Program Files\Tesseract-OCR\tessdata\jpn_vert.traineddata`

基本:

```bash
python images_to_text.py <folder> -o <output.txt>
```

カレントディレクトリの画像をOCR:

```bash
python images_to_text.py . -o result.txt
```

言語とTesseractパスを指定:

```bash
python images_to_text.py "C:\Users\kenji\Pictures\scans" -o all.txt --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe" --lang jpn
```

縦書き画像をOCR（`jpn_vert`を使用）:

```bash
python images_to_text.py "C:\Users\kenji\Pictures\vertical_scans" -o vertical.txt --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe" --lang jpn_vert
```

拡張子を絞る:

```bash
python images_to_text.py . -o out.txt --exts ".png,.jpg"
```

## CLIオプション

- `folder`:
  - 画像フォルダ（省略時 `.`）
- `-o, --output`:
  - 出力テキスト（既定 `output.txt`）
- `--exts`:
  - 対象拡張子（カンマ区切り、既定 `.png,.jpg,.jpeg,.tif,.tiff,.bmp`）
- `--tesseract-cmd`:
  - Tesseract実行ファイルのフルパス
- `--lang`:
  - OCR言語（Tesseract言語データに依存）

## 注意点

- 画像ごとの見出し行は現在出力しない実装です。
- 画像が見つからない場合は `FileNotFoundError` になります。
- 画像の読み込みやOCRに失敗したファイルは、エラー文がテキストに書き込まれます。

## 関連ドキュメント

- `USAGE.md`: 実行例とトラブルシュート
# ocrpic2txt
