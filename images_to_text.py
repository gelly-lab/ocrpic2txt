import os
import re
import argparse
from PIL import Image
import pytesseract

NUMBER_RE = re.compile(r"(\d+)")


def extract_sort_key(name: str):
    nums = NUMBER_RE.findall(name)
    if nums:
        # use tuple of ints for natural numeric sort (handles multiple numbers)
        return tuple(int(n) for n in nums)
    # fallback: use filename (lowercased)
    return (name.lower(),)


def find_image_files(folder: str, exts):
    files = []
    for entry in os.listdir(folder):
        lower = entry.lower()
        if any(lower.endswith(e) for e in exts):
            files.append(entry)
    files.sort(key=extract_sort_key)
    return [os.path.join(folder, f) for f in files]


def ocr_images_to_text(folder: str, out_path: str, exts, tesseract_cmd: str = None, lang: str = None, sep: str = ""):
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    imgs = find_image_files(folder, exts)
    if not imgs:
        raise FileNotFoundError(f"No image files found in {folder} with extensions {exts}")

    with open(out_path, "w", encoding="utf-8") as out_f:
        for i, img_path in enumerate(imgs, start=1):
            try:
                with Image.open(img_path) as img:
                    text = pytesseract.image_to_string(img, lang=lang) if lang else pytesseract.image_to_string(img)
            except Exception as e:
                text = f"[ERROR opening or OCR'ing {img_path}: {e}]\n"

            header = f"--- FILE {i}: {os.path.basename(img_path)} ---\n"
            #out_f.write(header)
            out_f.write(text)
            if i != len(imgs):
                out_f.write(sep)

    return out_path


def main():
    parser = argparse.ArgumentParser(description="フォルダ内の連番画像を読み込み、1つのテキストファイルにまとめます。")
    parser.add_argument("folder", nargs="?", default=".", help="画像が入っているフォルダ（既定はカレントディレクトリ）")
    parser.add_argument("-o", "--output", default="output.txt", help="出力テキストファイルパス（既定: output.txt）")
    parser.add_argument("--exts", default=".png,.jpg,.jpeg,.tif,.tiff,.bmp", help="カンマ区切りで許可する拡張子（既定: .png,.jpg,.jpeg,.tif,.tiff,.bmp）")
    parser.add_argument("--tesseract-cmd", default=None, help="tesseract実行ファイルのフルパス（例: C:\\Program Files\\Tesseract-OCR\\tesseract.exe）")
    parser.add_argument("--lang", default=None, help="pytesseractに渡す言語オプション（例: jpn）")
    args = parser.parse_args()

    exts = [e.strip().lower() for e in args.exts.split(",") if e.strip()]
    out = ocr_images_to_text(args.folder, args.output, exts, tesseract_cmd=args.tesseract_cmd, lang=args.lang)
    print(f"Wrote OCR text to: {out}")


if __name__ == "__main__":
    main()
