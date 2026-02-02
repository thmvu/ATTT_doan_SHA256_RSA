# GIAI THICH BAO MAT PRIVATE KEY

## Van De: Tai Sao Khong Nen Luu Private Key Tren Server?

### 1. Nguyen Tac Co Ban Cua RSA
Trong he mat RSA:
- **Public Key (Khoa Cong Khai)**: Co the chia se voi bat ky ai. Dung de XAC THUC chu ky.
- **Private Key (Khoa Bi Mat)**: CHI NGUOI GIU MOI BIET. Dung de KY SO.

> **Quy tac vang**: Neu Private Key bi lo → Bat ky ai cung co the gia mao chu ky cua ban!

### 2. Rui Ro Khi Luu Private Key Tren Server
Neu luu Private Key tren server lau dai:
- ❌ **Rui ro 1**: Neu server bi hack → Tat ca Private Key bi danh cap.
- ❌ **Rui ro 2**: Admin server co the doc Private Key cua moi nguoi.
- ❌ **Rui ro 3**: Neu nhieu nguoi dung → Khong biet ai la chu nhan thuc cua chu ky.

### 3. Nen Lam The Nao?
Trong thuc te, nen:
1. ✅ **Tao khoa tren may cua ban** (hoac download ngay sau khi tao).
2. ✅ **Chi gui Private Key len server tam thoi** khi can ky (server xu ly xong → xoa ngay).
3. ✅ **Luu Private Key vao USB/Mat khau bao ve** de bao quan.

---

## Ung Dung Nay Giai Quyet The Nao?

Ung dung ho tro **2 che do**:

### Che Do 1: DEMO DON GIAN (Khoa Chung)
- Nguoi dung tao khoa → Luu tren server (thu muc `keys/`).
- Tat ca moi nguoi dung CHUNG 1 cap khoa.
- **Muc dich**: Demo nhanh de hieu co che RSA.
- **Han che**: KHONG an toan cho thuc te.

### Che Do 2: BAO MAT THAT (Moi Nguoi Mot Khoa)
- Nguoi dung **tai Private Key ve may** sau khi tao (nut "Tai Private Key").
- Khi ky file, **upload Private Key rieng cua minh** len.
- Server chi dung **tam thoi** de ky, sau do **XOA NGAY**.
- **Uu diem**: Moi nguoi co khoa rieng, khong bi trung lap.

---

## Huong Dan Su Dung An Toan (Cho Thuc Te)

### Buoc 1: Tao Va Luu Khoa
1. Bam nut "Tao Cap Khoa Moi".
2. **QUAN TRONG**: Bam nut "Tai Private Key (Bi Mat)" → Luu vao USB/Thu muc bao mat.
3. Public Key co the de tren server hoac chia se cho nguoi khac.

### Buoc 2: Ky File Voi Khoa Rieng
1. Chon file can ky.
2. **Chon Private Key rieng** (file `.pem` da tai o Buoc 1).
3. Bam "Ky File Ngay".
4. Server se:
   - Nhan Private Key tam thoi.
   - Ky file.
   - Xoa Private Key ngay lap tuc.

### Buoc 3: Xac Thuc
- Nguoi nhan chi can **Public Key** (co the public) + File + Chu ky `.sig` de xac thuc.
- Khong can Private Key!

---

## Ket Luan

- **Che do Demo**: Tien loi cho hoc tap/demo, nhung KHONG an toan.
- **Che do Thuc Te**: Can upload Private Key rieng moi lan ky → An toan hon.
- **Best Practice**: Luon luu Private Key offline (USB, Mat khau,...) va CHI SU DUNG KHI CAN.

> **Luu y cho Do An**: Ban nen giai thich cho thay rang "Em da hieu van de bao mat, nen da thiet ke 2 che do - che do demo de de hieu thuat toan, va che do thuc te cho phep moi nguoi dung khoa rieng".
