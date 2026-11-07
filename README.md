# Người Que Tấn Công

Game hành động người que chạy trên trình duyệt (HTML5 Canvas, một file duy nhất, không cần cài đặt).

## Cách chơi
- **Chạm / bấm** vào bất kỳ đâu: người que lướt tới đó nhanh như tia chớp, chém mọi kẻ địch và bắn rơi mũi tên trên đường đi.
- Mỗi lần lướt tốn năng lượng (thanh xanh dương), năng lượng tự hồi.
- Đánh liên tục để tăng **combo** → nhân điểm.
- Hết mỗi đợt được chọn 1 trong 3 sức mạnh. Mỗi 5 đợt có **Trùm**: né sóng chấn động bằng cách lướt lên không.
- Máy tính: chuột để lướt, A/D đi, W nhảy, Space lướt tới địch gần nhất, P tạm dừng.

Kẻ địch: lính kiếm (đỏ), cung thủ (cam), dơi (tím nhạt), đồ tể (tím), trùm (đỏ đội vương miện).
Dấu **!** đỏ trên đầu = sắp tấn công.

## Chạy
Mở `index.html` bằng trình duyệt, hoặc bật GitHub Pages cho repo để chơi trên điện thoại (nên xoay ngang).

## Bản Android (APK)
File cài đặt: [`dist/NguoiQueTanCong.apk`](dist/NguoiQueTanCong.apk) (Android 7.0 trở lên).
Tải về điện thoại → mở file → cho phép "Cài ứng dụng không rõ nguồn gốc" → Cài đặt.

Build lại (không cần Android SDK/Gradle): xem `android/build.sh`. Ứng dụng là WebView chạy `index.html` offline,
manifest/resources được đóng gói bằng `android/tools/mkapk.py`, ký bằng apksig (chữ ký v2).
