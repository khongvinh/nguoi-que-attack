# Người Que Tấn Công

Game hành động người que chạy trên trình duyệt (HTML5 Canvas, một file duy nhất, không cần cài đặt).

## Cách chơi
- **Chạm / bấm** vào bất kỳ đâu: người que lướt tới đó nhanh như tia chớp, chém mọi kẻ địch và bắn rơi mũi tên trên đường đi.
- Mỗi lần lướt tốn năng lượng (thanh xanh dương), năng lượng tự hồi.
- Đánh liên tục để tăng **combo** → nhân điểm.
- Hết mỗi đợt được chọn 1 trong 3 sức mạnh. Mỗi 5 đợt có **Trùm**: né sóng chấn động bằng cách lướt lên không.
- Máy tính: chuột để lướt, A/D đi, W nhảy, Space lướt tới địch gần nhất, F/chuột phải ném, E hất tung, S dộng đất, T cây kỹ năng, P tạm dừng.

- **Vũ khí rơi từ địch**: lính kiếm rơi Kiếm/Phi tiêu, cung thủ rơi Phi tiêu/Giáo, đồ tể rơi Rìu/Búa Sấm, trùm rơi cả đống.
  Tỉ lệ rơi thấp và tối đa 3 món trên đất để màn hình gọn. Đi vào để nhặt (khi tay không hoặc cùng loại), **lướt qua** để đổi vũ khí. Vũ khí làm đòn lướt mạnh hơn nhưng có độ bền.
- **Ném vũ khí**: **vuốt nhanh** trên màn hình theo hướng muốn ném (có hỗ trợ ngắm vào địch gần hướng vuốt);
  máy tính: phím F hoặc chuột phải (ném về phía con trỏ). Vũ khí **ném 1 lần là vỡ**.
  Kiếm xoay, Giáo xuyên thấu, Rìu bay vòng cung sát thương lớn, Búa Sấm nổ sóng chấn động, Phi tiêu bay thẳng (nhiều phát).
- **28 vật phẩm nâng cấp**, chia 4 độ hiếm (Thường / Hiếm / Sử Thi / Huyền Thoại), mở khóa dần theo đợt; từ đợt 6 có 4 lựa chọn.
  Ví dụ: Nam Châm, Thợ Rèn, Kho Vũ Khí, Ném Đôi, Khiên Sét, Bão Sét, Thần Sấm, Cuồng Nộ, Bất Tử…
- **Kỹ năng vuốt**: vuốt **LÊN** khi đứng dưới đất = **Hất Tung** (hất văng địch lên trời, bản thân bật lên cao);
  đang trên không vuốt **XUỐNG** = **Dộng Đất** (lao xuống, nổ sóng xung kích, càng cao càng mạnh). Máy tính: E / S.
- **Cây kỹ năng** (nút ở màn chọn vật phẩm, màn tạm dừng, phím T): qua mỗi đợt +1 điểm, hạ trùm +2 điểm. 4 nhánh:
  Sấm (Lướt Sét → Tia Kép → Sét Dư Chấn), Địa Chấn (Dộng Đất+ → Nứt Đất → Dung Nham),
  Phong (Hất Tung+ → Liên Hoàn → Lốc Xoáy), Sinh Lực (Cường Thể → Hồi Phục → Nộ Khí).
- Mỗi lần qua màn, số quái mỗi đợt **tăng 20%**.

- **Chiêu cuối – Thiên Lôi Giáng Thế**: đạt **50 combo** rồi lướt lên không trung → người que bay lên tụ sét rồi đấm thẳng xuống đất,
  nổ toàn bộ mặt đất: đánh trúng mọi kẻ địch, xoá hết tên/bom/sét đang bay. Thanh "Chiêu cuối" ở giữa trên màn hình cho biết tiến độ.

## Màn chơi
Mỗi 5 đợt đổi màn (đợt thứ 5 là trùm), sau màn 4 quay vòng và mạnh hơn:
1. **Đêm Trăng** – trùm *Chúa Tể Bóng Đêm*
2. **Sa Mạc Hoàng Hôn** (bão cát) – trùm *Vua Cát*
3. **Rừng Băng** (tuyết rơi) – trùm *Hiệp Sĩ Băng*
4. **Núi Lửa** (tro lửa bay) – trùm *Quỷ Lửa*

Trùm dùng chiêu giống người chơi, càng về sau càng nhiều chiêu: lướt sét (có vạch đỏ báo trước), ném 3 phi đao,
bay lên bổ nhào (vòng đỏ dưới đất), combo 3 đòn (chém – hất tung – xoay tròn), dậm đất tạo sóng, húc.

Kẻ địch: lính kiếm (đỏ), cung thủ (cam), dơi (tím nhạt), đồ tể (tím), **ninja** (xanh ngọc, lướt chém),
**lính khiên** (bạc, chặn đòn trước mặt — đánh sau lưng), **lính bom** (vàng, lướt qua bom để đá văng),
**pháp sư** (hồng, bay lơ lửng, gọi sét xuống vòng tròn), trùm (đội vương miện).
Dấu **!** đỏ trên đầu = sắp tấn công.

## Chạy
Mở `index.html` bằng trình duyệt, hoặc bật GitHub Pages cho repo để chơi trên điện thoại (nên xoay ngang).

## Bản Android (APK)
File cài đặt: [`dist/NguoiQueTanCong.apk`](dist/NguoiQueTanCong.apk) (Android 7.0 trở lên).
Tải về điện thoại → mở file → cho phép "Cài ứng dụng không rõ nguồn gốc" → Cài đặt.

Build lại (không cần Android SDK/Gradle): xem `android/build.sh`. Ứng dụng là WebView chạy `index.html` offline,
manifest/resources được đóng gói bằng `android/tools/mkapk.py`, ký bằng apksig (chữ ký v2).
