# GIAI THICH CHI TIET & PHAN TICH CODE (Detailed Analysis)

Tai lieu nay giai thich chi tiet co che hoat dong va phan tich tung dong code quan trong trong du an Chu Ky So (RSA + SHA-256 Code Thuan).

---

## 1. THUAT TOAN BAM SHA-256 (sha256_library.py)

SHA-256 (Secure Hash Algorithm 256-bit) giup tao ra mot chuoi gia tri duy nhat (digest) tu du lieu dau vao. Neu du lieu thay doi du chi 1 bit, hash se thay doi hoan toan.

### A. Cac Hang So & Ham Bo Tro
Trong code, chung ta su dung cac hang so `K` (64 gia tri) - day la phan thap phan can bac 3 cua 64 so nguyen to dau tien.
Cac gia tri khoi tao `h0`...`h7` la phan thap phan can bac 2 cua 8 so nguyen to dau tien.

**Ham Xoay Phai (Right Rotate):**
Trong SHA-256, phep xoay bit (circular shift) rat quan trong de khuay dao du lieu.
```python
def xoay_phai(gia_tri, so_luong):
    # Dich phai 'so_luong' bit OR Dich trai (32 - 'so_luong') bit
    # & 0xFFFFFFFF de dam bao gia tri luon la 32-bit (khong bi tran so)
    return ((gia_tri >> so_luong) | (gia_tri << (32 - so_luong))) & 0xFFFFFFFF
```

### B. Tien Xu Ly (Padding)
Truoc khi bam, thong diep phai duoc dem (padding) de do dai chia het cho 512 bit.
1. Them bit `1` (`0x80`).
2. Them cac bit `0` cho den khi do dai mod 512 = 448.
3. Them 64-bit cuoi cung la do dai cua thong diep goc (Big Endian).

```python
# Code thuc te:
thong_diep += b'\x80'  # Them bit 1
while (len(thong_diep) * 8) % 512 != 448: # Them 0
    thong_diep += b'\x00'
thong_diep += chieu_dai.to_bytes(8, 'big') # Them do dai
```

### C. Vong Lap Nen (Compression Loop)
Day la trai tim cua thuat toan. Moi khoi 512-bit duoc xu ly qua 64 vong lap.
Su dung cac ham toan hoc `Sigma`, `Ma`, `Ch` de bien doi trang thai `a,b,c,d,e,f,g,h`.

```python
# S1 va ch giup khuay dao bien 'e'
S1 = xoay_phai(e, 6) ^ xoay_phai(e, 11) ^ xoay_phai(e, 25)
ch = (e & f) ^ ((~e) & g)
temp1 = (h + S1 + ch + K[j] + w[j]) & 0xFFFFFFFF

# S0 va maj giup khuay dao bien 'a'
S0 = xoay_phai(a, 2) ^ xoay_phai(a, 13) ^ xoay_phai(a, 22)
maj = (a & b) ^ (a & c) ^ (b & c)
temp2 = (S0 + maj) & 0xFFFFFFFF

# Cap nhat trang thai
e = (d + temp1) & 0xFFFFFFFF
a = (temp1 + temp2) & 0xFFFFFFFF
```
> **Ket qua**: Sau khi xu ly het cac khoi, ghep `h0` den `h7` lai thanh chuoi Hex 64 ky tu.

---

## 2. HE MAT RSA (rsa_library.py)

RSA dua tren do kho cua viec phan tich thua so nguyen to cua hai so rat lon.

### A. Kiem Tra Nguyen To (Miller-Rabin)
De tao khoa, can 2 so nguyen to cuc lon. Thuat toan Miller-Rabin giup kiem tra xac suat nguyen to nhanh chong.
```python
def kiem_tra_nguyen_to(n, k=40):
    # Viet n-1 duoi dang 2^r * d
    # Chon ngau nhien 'a' trong khoang [2, n-2]
    # Kiem tra a^d mod n
    x = pow(a, d, n)
    # Neu x = 1 hoac x = n-1 thi co the la nguyen to => tiep tuc vong lap
    # Neu khong thoa man dieu kien Fermat => Hop so (False)
```

### B. Tao Khoa (Key Generation)
```python
def tao_cap_khoa_rsa():
    # 1. Tim p, q nguyen to (dung ham o tren)
    # 2. n = p * q (Module co so)
    # 3. Phi = (p-1)(q-1)
    # 4. Chon e = 65537 (Rat pho bien vi tinh toan nhanh va du an toan)
    # 5. Tinh d = nghich_dao(e, Phi)
```
> **Cong thuc cot loi**: `d * e ≡ 1 (mod Phi)`.
Ham `nghich_dao_module` su dung thuat toan **Euclid Mo Rong** de tim `d`.

### C. Ky So (Signing) - Khoa Bi Mat
Ban chat cua ky so RSA la "Ma hoa bang Khoa Bi Mat". 
```python
def ky_so_rsa(du_lieu_bytes, khoa_bi_mat):
    d, n = khoa_bi_mat
    m = tinh_hash_sha256(du_lieu_bytes) # Buoc 1: Hash
    
    # Buoc 2: Luy thua module: s = m^d mod n
    chu_ky_int = pow(m, d, n) 
    return hex(chu_ky_int)
```
Ham `pow(m, d, n)` cua Python thuc hien thuat toan **Nhan-Binh Phuong (Modular Exponentiation)** rat hieu qua cho so lon.

### D. Xac Thuc (Verification) - Khoa Cong Khai
Ai cung co the dung Khoa Cong Khai de giai ma chu ky, nhung chi nguoi giu Khoa Bi Mat moi tao ra duoc no.
```python
def xac_thuc_chu_ky(...):
    e, n = khoa_cong_khai
    # Tinh m' = s^e mod n
    m_phay = pow(chu_ky_int, e, n)
    
    # So sanh voi hash cua file goc
    return m == m_phay
```

---

## 3. UNG DUNG BACKEND (app.py)

Day la cau noi giua Logic Toan Hoc va Giao Dien Nguoi Dung.

- `xu_ly_tao_khoa()`: Goi `rsa_library` de tao khoa, sau do luu vao file `.pem` (thuc ra la JSON Base64 tu custom).
- `xu_ly_ky_file()`: 
    1. Doc file upload tu user.
    2. Doc Private Key tu file.
    3. Goi `ky_so_rsa` -> Tao ra file `.sig`.
- `xu_ly_xac_thuc()`:
    1. Doc file goc va file `.sig` user upload.
    2. Doc Public Key.
    3. Goi `xac_thuc_chu_ky` -> Tra ve `True` (Thanh cong) hoac `False` (That bai).

Format file khoa tuy chinh (`luu_khoa`):
Chung ta khong dung thu vien chuan ASN.1 ma dung JSON don gian:
`{"exponent": "...", "modulus": "...", "type": "RSA..."}` -> Base64 -> Boc trong header `-----BEGIN...`.
Cach nay giup doc/ghi de dang ma khong can thu vien ngoai.

---

### TONG KET
Du an nay la minh chung cho viec hieu sau sac ve **Crypto**. Thay vi goi ham `sign()` cua thu vien co san nhu mot "hop den", chung ta da tu xay dung tung banh rang cua co may RSA va SHA-256. 
- **Tinh bao mat**: Dua tren toan hoc vung chac (So nguyen to lon).
- **Tinh toan ven**: Dua tren SHA-256.
- **Hoc thuat**: Code thuan 100%.
