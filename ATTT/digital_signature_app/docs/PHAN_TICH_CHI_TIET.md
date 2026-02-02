# PHÂN TÍCH CHI TIẾT DỰ ÁN CHỮ KÝ SỐ AN TOÀN (RSA - SHA256 - AI - QR)

Tài liệu này cung cấp cái nhìn sâu sắc nhất về mã nguồn, luồng dữ liệu và thuật toán của dự án. Được chia thành các phần từ tổng quan đến chi tiết từng dòng code.

---

## MỤC LỤC
1.  **Tổng Quan Hệ Thống**: Kiến trúc và công nghệ.
2.  **Luồng Hoạt Động (Workflow)**: Diagram luồng ký và xác thực.
3.  **Giải Thích Thuật Toán Cốt Lõi**: Phân tích toán học RSA & SHA-256.
4.  **Phân Tích Code Chi Tiết (Code Breakdown)**: Giải thích từng hàm quan trọng.
5.  **Tính Năng Mới (AI & QR)**: Cơ chế hoạt động.

---

## 1. TỔNG QUAN HỆ THỐNG

### Công Nghệ Sử Dụng
*   **Ngôn Ngữ**: Python 3.10+
*   **Framework Web**: Flask (Nhẹ, dễ triển khai)
*   **Thuật Toán Ký**: RSA (Rivest–Shamir–Adleman) - Tự cài đặt "from scratch" để hiểu sâu toán học.
*   **Hàm Băm**: SHA-256 (Secure Hash Algorithm 256-bit) - Tự cài đặt.
*   **Thư Viện Bổ Trợ**:
    *   `qrcode`: Tạo mã QR.
    *   `Pillow (PIL)`: Xử lý ảnh và đọc metadata.

---

## 2. LUỒNG HOẠT ĐỘNG (WORKFLOW)

### Ký Số (Signing Process)
> Mục tiêu: Đảm bảo tính xác thực (Authentication) và toàn vẹn (Integrity) của file.

1.  **Input**: Người dùng chọn File $F$ và Private Key $K_{pri}(d, n)$.
2.  **AI Check** (Optional): $F \xrightarrow{metadata} \text{AI Result}$ (Kiểm tra giả mạo).
3.  **Hashing**: $F \xrightarrow{SHA-256} H$ (Chuỗi hash 64 ký tự hex).
4.  **Signing**: $H \xrightarrow{RSA} S = H^d \mod n$.
5.  **Output**: File chữ ký $S$ (.sig) + Mã QR chứa thông tin verification.

### Xác Thực (Verification Process)
> Mục tiêu: Kiểm tra xem file có bị sửa đổi không và chữ ký có đúng của người gửi không.

1.  **Input**: File gốc $F'$, File chữ ký $S$, Public Key $K_{pub}(e, n)$.
2.  **Decryption**: $S \xrightarrow{RSA} H_{check} = S^e \mod n$.
3.  **Hashing**: $F' \xrightarrow{SHA-256} H_{new}$.
4.  **Comparison**:
    *   Nếu $H_{check} == H_{new}$: ✅ File CHUẨN, không bị sửa.
    *   Nếu khác: ❌ File ĐÃ BỊ SỬA hoặc SAI chữ ký.

---

## 3. GIẢI THÍCH THUẬT TOÁN CỐT LÕI

### A. RSA - Mật Mã Khóa Công Khai
RSA dựa trên độ khó của việc phân tích thừa số nguyên tố của một số rất lớn.

*   **Tạo Khóa**:
    *   Chọn 2 số nguyên tố lớn $p, q$ (dùng thuật toán Miller-Rabin để kiểm tra).
    *   Modulus $n = p \times q$.
    *   Phi Euler $\phi(n) = (p-1)(q-1)$.
    *   Chọn Public Exponent $e = 65537$ (thường dùng).
    *   Tính Private Exponent $d$ sao cho $d \times e \equiv 1 \mod \phi(n)$ (dùng Euclid mở rộng).

*   **Ký & Xác Thực**:
    *   Ký: $S = m^d \mod n$
    *   Xác: $m = S^e \mod n$
    *   Trong Python: `pow(base, exp, mod)` tính rất nhanh nhờ thuật toán "Modular Exponentiation".

### B. SHA-256 - Hàm Băm
SHA-256 biến đổi dữ liệu bất kỳ thành chuỗi 256-bit cố định. Tính chất quan trọng:
*   **Một chiều**: Không thể suy ngược từ Hash ra file gốc.
*   **Chống va chạm**: Rất khó tìm 2 file có cùng mã Hash.
*   **Hiệu ứng tuyết lở**: Thay đổi 1 bit file $\rightarrow$ Hash thay đổi hoàn toàn.

---

## 4. PHÂN TÍCH CODE CHI TIẾT (CODE BREAKDOWN)

### Module 1: `rsa_library.py`

#### Hàm `kiem_tra_nguyen_to(n, k=40)`
Đây là thuật toán **Miller-Rabin Primality Test**.
*   **Tại sao cần?**: Kiểm tra số nguyên tố lớn (vài trăm bit) nếu chạy vòng lặp thường sẽ mất hàng tỷ năm. Miller-Rabin là thuật toán xác suất cực nhanh.
*   **Code logic**:
    ```python
    # Phân tích n-1 = 2^r * d
    while d % 2 == 0: ...
    # Lặp k lần kiểm tra:
    x = pow(a, d, n) # a^d mod n
    # Nếu x != 1 và x != n-1 thì kiểm tra tiếp các bình phương...
    ```

#### Hàm `nghich_dao_module(a, m)`
Tìm $d$ từ $e$ và $\phi(n)$. Đây là cốt lõi để tạo Private Key.
*   Sử dụng **Extended Euclidean Algorithm** (Giải thuật Euclid mở rộng).
*   Tìm $x, y$ sao cho $ax + my = \gcd(a, m) = 1$. Khi đó $x$ chính là nghịch đảo của $a \mod m$.

### Module 2: `sha256_library.py`

#### Hàm `tinh_hash_sha256(thong_diep)`
*   **Bước 1: Padding (Đệm)**:
    ```python
    thong_diep += b'\x80' # Thêm bit 1
    # Thêm các bit 0 cho đến khi len % 512 == 448
    thong_diep += chieu_dai.to_bytes(8, 'big') # 64 bit cuối ghi độ dài
    ```
*   **Bước 2: compression (Nén)**:
    *   Vòng lặp 64 lần với các phép toán Bitwise: `XOAY_PHAI (>>>)`, `XOR (^)`, `AND (&)`.
    *   Mỗi vòng trộn dữ liệu của khối hiện tại vào các biến trạng thái `a, b, c...h`.

### Module 3: `ai_detector.py` (Mới)
*   **Logic**:
    ```python
    image = Image.open(path)
    exif = image.getexif() # Lấy metadata
    software = exif.get("Software") # Lấy thông tin phần mềm tạo ảnh
    if "photoshop" in software: return False # Phát hiện
    ```
*   **Ý nghĩa**: Đây là tầng bảo vệ đầu tiên (Layer 1 Defense). Nếu ảnh đã qua chỉnh sửa, metadata thường sẽ lưu dấu vết của phần mềm đó.

### Module 4: `app.py`
Kết nối mọi thứ lại với nhau.

*   Route `/ky_file`:
    1.  Nhận file từ form HTML.
    2.  `if ai_check_enabled`: Chạy `ai_detector`.
    3.  Đọc bytes file $\rightarrow$ `rsa_library.ky_so_rsa`.
    4.  Nhận chuỗi ký hex.
    5.  Gói thông tin vào JSON $\rightarrow$ `qr_generator`.
    6.  Render template `index.html` với thông tin trả về.

---

## 5. TỪ ĐIỂN THUẬT NGỮ (GLOSSARY)

*   **Public Key (Khóa Công Khai)**: Dùng để xác thực (Verify) hoặc mã hóa. Công khai cho mọi người.
*   **Private Key (Khóa Bí Mật)**: Dùng để ký (Sign) hoặc giải mã. Phải giữ bí mật tuyệt đối.
*   **Digital Signature (Chữ Ký Số)**: Bản chất là Mã Hash của file đã được mã hóa bởi Private Key.
*   **Metadata/EXIF**: Dữ liệu ẩn trong file ảnh (ngày chụp, máy ảnh, phần mềm chỉnh sửa...).
