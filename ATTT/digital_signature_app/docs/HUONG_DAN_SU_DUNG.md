# HƯỚNG DẪN SỬ DỤNG: TÍNH NĂNG MỚI (QR CODE & AI CHECK)

Hệ thống chữ ký số đã được nâng cấp với 2 tính năng bảo mật mới:
1. **QR Code Verification**: Tạo mã QR chứa thông tin xác thực để quét nhanh bằng điện thoại.
2. **AI Deepfake Detection (Metadata)**: Phát hiện ảnh bị chỉnh sửa qua kiểm tra metadata (EXIF).

---

## 1. Hướng Dẫn Ký File Với QR & AI Check

### Bước 1: Chọn File & Khóa
- Tại phần **Ký Văn Bản**, chọn file cần ký như bình thường.
- Chọn Private Key (nếu có).

### Bước 2: Kích Hoạt AI Check (Chỉ cho ảnh)
- Tích vào ô: `🤖 Kích hoạt AI Check (Phát hiện ảnh giả mạo)`
- **Lưu ý**: Tính năng này chỉ hoạt động với các file ảnh (.jpg, .png, .jpeg...).

### Bước 3: Ký File & Nhận Kết Quả
- Nhấn nút "Ký File Ngay".
- Sau khi ký thành công, bạn sẽ thấy:
  - **Thông báo thành công**: "✅ Đã Ký File Thành Công (RSA Pure)!"
  - **Kết quả AI Check**:
    - ✅ **PASS**: Ảnh hợp lệ hoặc không phát hiện dấu hiệu chỉnh sửa.
    - ⚠️ **WARNING**: Phát hiện phần mềm chỉnh sửa (Photoshop, GIMP...). Hệ thống vẫn cho phép ký nhưng cảnh báo bạn.
  - **Mã QR**: Hiển thị ngay trên màn hình.

---

## 2. Cách Sử Dụng Mã QR

### Mục đích
Mã QR chứa tóm tắt thông tin xác thực của file, giúp bạn kiểm tra nhanh bằng điện thoại mà không cần máy tính.

### Cách dùng
1. Mở camera điện thoại hoặc ứng dụng quét QR (Zalo, Google Lens...).
2. Quét mã QR hiển thị trên màn hình (hoặc tải về file `.png`).
3. Thông tin hiển thị sẽ bao gồm:
   - **Tên file**: Tên file gốc.
   - **Signature**: Chữ ký số (rút gọn).
   - **Timestamp**: Thời gian ký.
   - **AI Status**: Kết quả kiểm tra AI (PASS/WARNING).

---

## 3. Câu Hỏi Thường Gặp (FAQ)

### Q: Tại sao AI Check lại báo "WARNING" với ảnh của tôi?
**A**: Hệ thống phát hiện metadata (EXIF) của ảnh có chứa tên phần mềm chỉnh sửa (như Adobe Photoshop, GIMP). Điều này không có nghĩa là ảnh giả mạo 100%, nhưng nó đã qua xử lý và không còn là ảnh gốc từ camera.

### Q: Tôi upload file .txt nhưng bật AI Check thì sao?
**A**: Hệ thống sẽ bỏ qua AI Check và báo "File không phải ảnh". Quá trình ký vẫn diễn ra bình thường.

### Q: Tôi có thể tắt AI Check không?
**A**: Có. AI Check là tùy chọn. Bạn chỉ cần bỏ tích ô checkbox là được.

### Q: Mã QR có thay thế được file chữ ký (.sig) không?
**A**: **KHÔNG**. Mã QR chỉ dùng để tham khảo nhanh. Để xác thực pháp lý hoặc toàn vẹn dữ liệu chính xác 100%, bạn vẫn cần dùng chức năng "Kiểm Tra Toàn Vẹn" với file `.sig`.
