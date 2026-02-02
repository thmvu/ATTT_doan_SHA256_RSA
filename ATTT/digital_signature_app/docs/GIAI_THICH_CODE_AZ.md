# GIẢI THÍCH CODE & THUẬT TOÁN "TỪ A ĐẾN Z"

Tài liệu này được viết dành riêng cho việc tìm hiểu sâu về dự án Chữ Ký Số (Digital Signature), giải thích mọi khái niệm từ cơ bản nhất đến chi tiết dòng code.

---

## PHẦN 1: KHÁI NIỆM CƠ BẢN (LÝ THUYẾT)

### 1. Hàm Băm (Hashing) Là Gì?
Hãy tưởng tượng Hàm Băm như một "máy xay thịt":
*   **Đầu vào**: Con bò, con gà, hay chỉ 1 miếng thịt (Dữ liệu bất kỳ: file ảnh, văn bản...).
*   **Đầu ra**: Một cây xúc xích có độ dài cố định (Chuỗi ký tự cố định).

**Tính chất quan trọng**:
1.  **Một chiều**: Từ cây xúc xích không thể nặn lại thành con bò (Không thể dịch ngược từ Hash ra file gốc).
2.  **Duy nhất (gần như)**: Hai con bò khác nhau sẽ ra hai cây xúc xích vị khác nhau. Chỉ cần thay đổi 1 sợi lông của con bò, cây xúc xích sẽ đổi vị hoàn toàn (Hiệu ứng tuyết lở).

> Trong dự án này, chúng ta dùng **SHA-256** (Secure Hash Algorithm 256-bit). Nó biến mọi file thành một chuỗi 64 ký tự Hex (256 bit).

### 2. Mã Hóa RSA (Bất Đối Xứng) Là Gì?
Khác với khóa cửa nhà (dùng 1 chìa để đóng và mở), RSA dùng **2 chìa khóa**:
1.  **Public Key (Khóa Công Khai)**: Ai cũng có thể biết. Dùng để **Khóa** (Mã hóa) hoặc **Kiểm tra** (Verify).
2.  **Private Key (Khóa Bí Mật)**: Chỉ chủ nhà giữ. Dùng để **Mở** (Giải mã) hoặc **Ký** (Sign).

### 3. Chữ Ký Số Hoạt Động Thế Nào?
Chữ ký số là sự kết hợp của HASHING + RSA.

*   **Ký (Sign)**:
    1.  Băm file văn bản $\rightarrow$ Mã Hash (đại diện duy nhất của file).
    2.  Dùng **Private Key** mã hóa Mã Hash đó $\rightarrow$ **Chữ Ký Số**.
    *   *Tại sao băm rồi mới ký?* Vì RSA rất chậm, không thể ký cả file 1GB được. Ký mã Hash (nhẹ hều) nhanh hơn nhiều.

*   **Xác Thực (Verify)**:
    1.  Người nhận dùng **Public Key** giải mã Chữ Ký Số $\rightarrow$ Ra Mã Hash (A).
    2.  Người nhận tự băm file gốc $\rightarrow$ Ra Mã Hash (B).
    3.  So sánh (A) và (B). Nếu giống nhau $\rightarrow$ File "xịn".

---

## PHẦN 2: PHÂN TÍCH CODE CHI TIẾT

Chúng ta sẽ đi sâu vào 2 file quan trọng nhất ("trái tim" của thuật toán).

### 1. `sha256_library.py` (Hàm Băm SHA-256)

Đây là file cài đặt thuật toán SHA-256 "code thuần" (không dùng thư viện có sẵn).

**Step 1: Khởi tạo hằng số (`K`, `h0`...`h7`)**
*   SHA-256 cần các con số ngẫu nhiên nhưng cố định để bắt đầu. Đây là các hằng số toán học (căn bậc 2, căn bậc 3 của các số nguyên tố đầu tiên).

**Step 2: Padding (Đệm dữ liệu) - Hàm `tinh_hash_sha256`**
```python
# Ví dụ message là "abc" (3 bytes = 24 bits)
thong_diep += b'\x80'  # Thêm bit 1 vào cuối -> "abc" + 10000000
while (len(thong_diep) * 8) % 512 != 448: # Thêm số 0...
thong_diep += chieu_dai.to_bytes(8, 'big') # Thêm độ dài file vào cuối
```
*   **Mục đích**: Làm cho tổng độ dài tin nhắn chia hết cho 512 bit (vì SHA-256 xử lý từng khối 512 bit một).

**Step 3: Vòng lặp nén (Compression Loop)**
```python
for i in range(0, len(thong_diep), 64): # Duyệt từng khối 64 bytes (512 bits)
    # ... Chia nhỏ thành 64 từ (words) ...
    # ... Chạy 64 vòng lặp xáo trộn ...
    S1 = xoay_phai(e, 6) ^ xoay_phai(e, 11) ^ xoay_phai(e, 25)
    # ...
```
*   **Giải thích**: Đây là "máy xay". Nó dùng các phép toán Bitwise (Xoay bit, XOR, AND) để trộn tung dữ liệu lên. Dù input có cấu trúc rõ ràng, sau 64 vòng lặp này, output sẽ trông hoàn toàn ngẫu nhiên.

---

### 2. `rsa_library.py` (Thuật Toán RSA)

File này cài đặt toán học RSA từ con số 0.

**Hàm `kiem_tra_nguyen_to(n)` (Miller-Rabin)**
*   Để tạo khóa RSA, ta cần 2 số nguyên tố cực lớn. Làm sao biết một số 300 chữ số có phải nguyên tố không?
*   Dùng thuật toán Miller-Rabin: Thử xác suất. Nếu vượt qua 40 lần thử (`k=40`), xác suất nó là hợp số cực thấp ($< 2^{-80}$).

**Hàm `tao_cap_khoa_rsa()`**
```python
# 1. Tìm 2 số nguyên tố p, q lớn
p = tao_so_nguyen_to(bits)
q = tao_so_nguyen_to(bits)

# 2. Tính n (Modulus) - Đây là 1 phần của khóa công khai & bí mật
n = p * q 

# 3. Tính e (Số mũ công khai) - Thường chọn 65537
e = 65537

# 4. Tính d (Số mũ bí mật) - Bằng thuật toán Euclid Mở Rộng
d = nghich_dao_module(e, (p-1)*(q-1))
```
*   **Kết quả**: Public Key là `(e, n)`, Private Key là `(d, n)`. Ai có `d` là chủ nhân.

**Hàm `ky_so_rsa(du_lieu, khoa_bi_mat)`**
```python
m = tinh_hash_sha256(du_lieu) # Băm ra số hex
chu_ky = pow(m, d, n)         # CÔNG THỨC THẦN THÁNH: s = m^d mod n
```
*   Hàm `pow(m, d, n)` của Python thực hiện phép tính $m^d \text{ chia lấy dư cho } n$. Đây chính là phép ký RSA.

**Hàm `xac_thuc_chu_ky()`**
```python
m_verify = pow(chu_ky, e, n)  # Giải mã: m' = s^e mod n
if m_verify == m_original: return True # So sánh
```

---

### 3. `ai_detector.py` (Module AI Giả Lập)

Đây là module kiểm tra "Fake" ảnh dựa trên metadata.

```python
exif_data = image.getexif() # Đọc thẻ EXIF ẩn trong ảnh
software = metadata.get("Software") # Tìm thẻ "Phần mềm sử dụng"
if "photoshop" in software: WARNING!
```
*   **Cơ chế**: Ảnh gốc từ Camera thường có EXIF chứa tên Camera (Canon, Sony...). Ảnh qua chỉnh sửa, phần mềm (như Photoshop) thường ghi đè tên của nó vào thẻ Software. Code này bắt được dấu hiệu đó.

---

## PHẦN 3: TỔNG KẾT LUỒNG DỮ LIỆU

Khi bạn ấn nút **"Ký File"**, máy tính làm việc như sau:
1.  **Frontend**: Gửi file lên Server Python.
2.  **App.py**:
    *   Gọi `ai_detector`: "Ê, kiểm tra xem ảnh này có Photoshop không?".
    *   Gọi `sha256`: "Xay nhỏ cái file này ra chuỗi Hash cho tao".
    *   Gọi `rsa`: "Lấy Private Key của tao, mã hóa cái chuỗi Hash kia đi".
    *   Gọi `qrcode`: "Gói cái tên file + chữ ký + kết quả AI vào cái mã QR".
3.  **Frontend**: Nhận về file `.sig` và hiện ảnh QR cho bạn.

Đó là toàn bộ câu chuyện từ A đến Z của dự án này!
