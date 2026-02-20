# OCR Tool Analysis

## 対象

- `images_to_text.py`
- `README.md`
- `requirements.txt`

## 要約

このツールは、指定フォルダ内の画像を自然順で並べてOCRし、1つのUTF-8テキストに連結するシンプルなCLIです。

- 実装規模が小さく、用途が明確
- 基本運用には十分
- ただし、運用時の品質とトラブル耐性を高める余地がある

## 現状仕様（コードベース）

- 入力: `folder`（省略時 `.`）
- 出力: `-o/--output`（既定 `output.txt`）
- 対象拡張子: `--exts`（カンマ区切り）
- OCRエンジン: `pytesseract` + 外部 `tesseract`
- 言語: `--lang`（例 `jpn`, `eng`, `jpn+eng`）
- ソート: ファイル名内の数字を使った自然順
- エラー時: 当該ファイルのエラー文を出力テキストに書き込んで続行

## 良い点

- 依存が少なく導入しやすい
- 画像列挙とOCR処理が関数分離されていて読みやすい
- 失敗ファイルがあっても全体処理を継続できる
- READMEと実装の整合性が取れている

## リスク・改善候補

### 1. ソートキー衝突時の順序不安定

`extract_sort_key()` は数字列のみを返すため、同じ数字を含む別名ファイルで順序が実行環境依存になる可能性があります。

改善案:

- ソートキーを `(数値タプル, lower_name)` にして同点時にファイル名で安定化

### 2. OCR設定の調整余地が少ない

現在は `--lang` のみ指定可能で、`--psm` や `--oem` などのTesseract設定を渡せません。

改善案:

- `--config` オプションを追加して `image_to_string(..., config=...)` を渡す

### 3. 出力整形の選択肢不足

画像間区切りは内部実装に `sep` があるもののCLIから変更できません。

改善案:

- `--sep` と `--include-header` を追加
- 画像ごとの境界を明示できるようにする

### 4. 入力検証が最小限

フォルダ存在チェックや、`--exts` の不正値検出が明示的ではありません。

改善案:

- 実行前に `os.path.isdir(folder)` を検証
- 拡張子正規化（先頭ドット補完）

### 5. テスト未整備

リファクタや仕様追加時の回帰検知が難しい状態です。

改善案:

- 少なくとも以下のユニットテストを追加
  - 自然順ソート
  - 拡張子フィルタ
  - 画像なし時エラー
  - OCR失敗時の継続動作

## 推奨優先度

1. ソート安定化（低コスト・効果大）
2. `--sep` / `--include-header` 追加（運用性向上）
3. `--config` 追加（OCR品質調整）
4. 入力検証強化
5. テスト追加

## 最小改善タスク例

- [ ] `extract_sort_key()` の同点時キー追加
- [ ] `argparse` に `--sep` 追加
- [ ] `argparse` に `--include-header`（bool）追加
- [ ] `--config` 追加
- [ ] `tests/test_sorting.py` など最小テスト作成

## 確認コマンド

```bash
python images_to_text.py . -o output.txt --lang jpn
python images_to_text.py . -o output.txt --exts ".png,.jpg"
python images_to_text.py . -o output.txt --tesseract-cmd "C:\Program Files\Tesseract-OCR\tesseract.exe"
```
