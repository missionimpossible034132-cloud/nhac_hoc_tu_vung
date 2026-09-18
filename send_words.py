# -*- coding: utf-8 -*-
"""
Gửi vài từ vựng tiếng Trung ngẫu nhiên tới Telegram mỗi ngày.
Không cần cài thư viện ngoài (chỉ dùng thư viện chuẩn của Python).

Biến môi trường cần có (đặt trong GitHub Secrets khi chạy qua GitHub Actions):
  TG_BOT_TOKEN   - token của bot, lấy từ @BotFather
  TG_CHAT_ID     - id cuộc trò chuyện cần gửi tới (chat với chính bạn)
Tuỳ chọn:
  WORDS_PER_DAY  - số từ gửi mỗi lần (mặc định 5)
  WORDS_FILE     - đường dẫn file words.json (mặc định words.json)
"""
import json
import os
import random
import sys
import urllib.parse
import urllib.request

BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
CHAT_ID = os.environ.get("TG_CHAT_ID")
WORDS_PER_DAY = int(os.environ.get("WORDS_PER_DAY", "5"))
WORDS_FILE = os.environ.get("WORDS_FILE", "words.json")


def load_words(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [w for w in data if w.get("hz") and w.get("py")]


def pick_words(words, n):
    n = min(n, len(words))
    return random.sample(words, n)


def format_message(words):
    lines = ["📚 Từ vựng tiếng Trung hôm nay:", ""]
    for i, w in enumerate(words, 1):
        vi = w.get("vi", "")
        lines.append(f"{i}. {w['hz']} ({w['py']}) — {vi}")
    lines.append("")
    lines.append("Cố lên nhé! 加油！")
    return "\n".join(lines)


def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode({"chat_id": chat_id, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")


def main():
    if not BOT_TOKEN or not CHAT_ID:
        print("Thiếu TG_BOT_TOKEN hoặc TG_CHAT_ID (biến môi trường / GitHub Secrets).", file=sys.stderr)
        sys.exit(1)
    try:
        words = load_words(WORDS_FILE)
    except FileNotFoundError:
        print(f"Không tìm thấy file {WORDS_FILE}. Hãy xuất file này từ app (tab Dữ liệu) rồi đặt cùng thư mục.", file=sys.stderr)
        sys.exit(1)
    if not words:
        print(f"File {WORDS_FILE} không có từ nào hợp lệ.", file=sys.stderr)
        sys.exit(1)

    chosen = pick_words(words, WORDS_PER_DAY)
    text = format_message(chosen)
    result = send_telegram(BOT_TOKEN, CHAT_ID, text)
    print("Đã gửi thành công:", result)


if __name__ == "__main__":
    main()
