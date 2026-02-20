# Usage and Troubleshooting

## Quick Commands

カレントフォルダをOCR:

```bash
python images_to_text.py . -o result.txt
```

日本語OCR:

```bash
python images_to_text.py . -o result.txt --lang jpn
```

日英OCR:

```bash
python images_to_text.py . -o result.txt --lang jpn+eng
```

Tesseractパスを明示:

```bash
python images_to_text.py . -o result.txt --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
```

## Typical Errors

`No image files found ...`

- 原因: 指定フォルダ内に対象拡張子の画像がない
- 対応:
  - `folder` を見直す
  - `--exts` を実ファイルに合わせる

`TesseractNotFoundError`（またはtesseractが見つからない）

- 原因: Tesseract未インストール、またはPATH未設定
- 対応:
  - Tesseractをインストール
  - `--tesseract-cmd` でフルパス指定

文字化け・認識精度が低い

- 原因: 言語設定ミスマッチ、画像品質の問題
- 対応:
  - `--lang` を調整（`jpn`, `eng`, `jpn+eng`）
  - 解像度の高い画像を使用
  - 傾き補正・二値化など前処理を追加

## Notes

- ファイル名は数字を基準に自然順ソートされます。
- 出力はUTF-8です。
- 現在は画像ごとの区切りヘッダは出力しません。
