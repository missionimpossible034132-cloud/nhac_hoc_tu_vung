# Nhắc học từ vựng tiếng Trung qua Telegram (miễn phí, tự động mỗi ngày)

Bộ này dùng **GitHub Actions** làm "đồng hồ hẹn giờ" chạy mỗi ngày, gọi **Telegram Bot API**
để gửi vài từ vựng ngẫu nhiên (ưu tiên có thể tuỳ biến sau) vào Telegram của chính bạn.
Không cần thuê server, không tốn phí.

## 1. Tạo bot Telegram (2 phút)

1. Mở Telegram, tìm và nhắn chuyện với **@BotFather**.
2. Gõ lệnh `/newbot`, đặt tên hiển thị và username cho bot (username phải kết thúc bằng `bot`, ví dụ `hoctuvung_bot`).
3. BotFather trả về một **token** dạng `123456789:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` — lưu lại, đây là `TG_BOT_TOKEN`.

## 2. Lấy chat_id của bạn

1. Trong Telegram, tìm đúng bot vừa tạo (theo username) và bấm **Start**, gửi bất kỳ tin nhắn nào (ví dụ "hi").
2. Mở trình duyệt, vào địa chỉ (thay `<token>` bằng token ở bước 1):
   `https://api.telegram.org/bot<token>/getUpdates`
3. Tìm đoạn `"chat":{"id":123456789,...}` trong kết quả trả về — số đó chính là `TG_CHAT_ID`.
   (Nếu chưa thấy gì, quay lại bước 1 gửi thêm 1 tin nhắn cho bot rồi tải lại trang.)

## 3. Đưa 3 file này lên một repo GitHub

Tạo một repo mới trên GitHub (public hay private đều được), giữ đúng cấu trúc thư mục:

```
ten-repo/
├── send_words.py
├── words.json
└── .github/
    └── workflows/
        └── daily-vocab.yml
```

Cách nhanh nhất: vào repo trên GitHub → **Add file → Upload files** → kéo thả cả 3 file/thư mục vào
(giữ nguyên đường dẫn `.github/workflows/daily-vocab.yml`).

## 4. Khai báo Secrets (để không lộ token trong code)

Vào repo → **Settings → Secrets and variables → Actions → New repository secret**, tạo 2 secret:

| Name | Value |
|---|---|
| `TG_BOT_TOKEN` | token lấy ở bước 1 |
| `TG_CHAT_ID` | id lấy ở bước 2 |

## 5. Chạy thử ngay (không cần chờ đến giờ hẹn)

Vào tab **Actions** của repo → chọn workflow **"Gửi từ vựng tiếng Trung qua Telegram"** →
bấm **Run workflow**. Sau ít giây, kiểm tra Telegram — nếu nhận được tin nhắn là đã thành công.
Từ giờ, workflow sẽ tự chạy mỗi ngày theo lịch đã đặt.

## 6. Tuỳ chỉnh

- **Đổi giờ gửi**: sửa dòng `cron: "0 1 * * *"` trong `.github/workflows/daily-vocab.yml`.
  Giờ trong cron luôn là **giờ UTC** → giờ Việt Nam = giờ UTC + 7. Ví dụ muốn gửi 7h sáng
  giờ Việt Nam thì đặt `cron: "0 0 * * *"`.
- **Đổi số từ mỗi lần gửi**: sửa `WORDS_PER_DAY: "5"` trong cùng file.
- **Đổi danh sách từ / ưu tiên từ đang học yếu**: mở app học từ vựng → tab **Dữ liệu** →
  bấm **"Xuất bộ từ (JSON)"** để tải file JSON mới nhất của bộ đang học, rồi upload đè lên
  `words.json` trong repo (Add file → Upload files, chọn "Replace").

## Giới hạn cần biết

- Đây là bản đơn giản: mỗi lần gửi chọn **ngẫu nhiên** trong file `words.json`, không tự động
  đồng bộ với tiến độ đang lưu trong trình duyệt của app (vì app chỉ lưu trên máy bạn, GitHub
  Actions không đọc được localStorage của trình duyệt). Muốn ưu tiên đúng các từ đang sai nhiều,
  hãy thỉnh thoảng xuất lại JSON như hướng dẫn ở mục 6.
- GitHub Actions cho tài khoản miễn phí có giới hạn số phút chạy/tháng, nhưng một tác vụ gửi
  tin nhắn thế này chỉ tốn vài giây mỗi ngày nên gần như không đáng lo.
