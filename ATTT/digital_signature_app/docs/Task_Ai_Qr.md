# NANG CAP DU AN: THEM AI DEEPFAKE DETECTION + QR CODE

## TONG QUAN
Nang cap he thong chu ky so hien tai voi 2 tinh nang moi:
1. **QR Code Verification**: Tao ma QR chua thong tin xac thuc de quet bang dien thoai
2. **AI Deepfake Detection**: Phat hien anh/video bi chinh sua hoac gia mao bang AI

---

## PHASE 1: THIET LAP MOI TRUONG (Setup)

- [ ] Cai dat cac thu vien can thiet <!-- id: 1 -->
  - [ ] `pip install qrcode[pil]` - Tao ma QR <!-- id: 1.1 -->
  - [ ] `pip install Pillow` - Xu ly anh <!-- id: 1.2 -->
  - [ ] `pip install transformers torch` - AI model <!-- id: 1.3 -->
  - [ ] Test import cac thu vien <!-- id: 1.4 -->

- [ ] Tai AI model deepfake detection <!-- id: 2 -->
  - [ ] Test model voi anh mau <!-- id: 2.1 -->
  - [ ] Kiem tra thoi gian xu ly (nen < 5s/anh) <!-- id: 2.2 -->

---

## PHASE 2: TICH HOP QR CODE (De - 2-3 gio)

- [ ] Tao module `qr_generator.py` <!-- id: 3 -->
  - [ ] Ham `tao_ma_qr(du_lieu, ten_file)` <!-- id: 3.1 -->
  - [ ] Du lieu QR chua: file_hash, signature, timestamp, ai_status <!-- id: 3.2 -->
  - [ ] Test tao QR va doc lai bang dien thoai <!-- id: 3.3 -->

- [ ] Cap nhat `app.py` cho QR <!-- id: 4 -->
  - [ ] Route `/ky_file`: Sau khi ky → Tao QR <!-- id: 4.1 -->
  - [ ] Luu file QR vao thu muc `qrcodes/` <!-- id: 4.2 -->
  - [ ] Tra ve link download QR cho user <!-- id: 4.3 -->

- [ ] Cap nhat giao dien `index.html` <!-- id: 5 -->
  - [ ] Hien thi anh QR sau khi ky thanh cong <!-- id: 5.1 -->
  - [ ] Nut "Tai Ma QR" <!-- id: 5.2 -->

- [ ] Test QR Code flow <!-- id: 6 -->
  - [ ] Tao khoa → Ky file → Tai QR → Quet bang dien thoai <!-- id: 6.1 -->
  - [ ] Kiem tra du lieu QR co chinh xac khong <!-- id: 6.2 -->

---

## PHASE 3: TICH HOP AI DETECTION (Trung Binh - 3-4 gio)

- [ ] Tao module `ai_detector.py` <!-- id: 7 -->
  - [ ] Ham `kiem_tra_metadata(file_path)` - Kiem tra EXIF <!-- id: 7.1 -->
    - Phat hien Photoshop, GIMP, thoi gian chinh sua <!-- id: 7.1.1 -->
  - [ ] Ham `kiem_tra_ai_deepfake(file_path)` - Dung model AI <!-- id: 7.2 -->
    - Load model: `dima806/deepfake_vs_real_image_detection` <!-- id: 7.2.1 -->
    - Tra ve: {hop_le: True/False, ty_le: 0.95} <!-- id: 7.2.2 -->
  - [ ] Ham tong hop: `phan_tich_file(file_path)` <!-- id: 7.3 -->

- [ ] Cap nhat `app.py` cho AI <!-- id: 8 -->
  - [ ] Route `/ky_file`: Them checkbox "Kich hoat AI Check" <!-- id: 8.1 -->
  - [ ] Neu AI check bat: <!-- id: 8.2 -->
    - Kiem tra file co phai anh/video khong <!-- id: 8.2.1 -->
    - Chay AI detection truoc khi ky <!-- id: 8.2.2 -->
    - Neu phat hien FAKE → Canh bao, KHONG ky <!-- id: 8.2.3 -->
    - Neu PASS → Tiep tuc ky binh thuong <!-- id: 8.2.4 -->
  - [ ] Luu ket qua AI vao file metadata (JSON) <!-- id: 8.3 -->

- [ ] Cap nhat giao dien cho AI <!-- id: 9 -->
  - [ ] Them checkbox "Kiem tra AI (Chi cho anh/video)" <!-- id: 9.1 -->
  - [ ] Hien thi ket qua AI: <!-- id: 9.2 -->
    - "✅ AI: File hop le (95% tin cay)" <!-- id: 9.2.1 -->
    - "❌ AI: Phat hien gia mao! Khong the ky." <!-- id: 9.2.2 -->
  - [ ] Loading icon khi AI dang xu ly <!-- id: 9.3 -->

- [ ] Test AI Detection flow <!-- id: 10 -->
  - [ ] Test voi anh that (REAL) <!-- id: 10.1 -->
  - [ ] Test voi anh da chinh sua (FAKE) <!-- id: 10.2 -->
  - [ ] Kiem tra thong bao loi neu upload file khong phai anh <!-- id: 10.3 -->

---

## PHASE 4: TICH HOP QR + AI (Ket Hop)

- [ ] QR chua ket qua AI <!-- id: 11 -->
  - [ ] Them truong `ai_check_result` vao QR data <!-- id: 11.1 -->
  - [ ] Mau: `{"ai": "PASS", "confidence": 0.95}` <!-- id: 11.2 -->

- [ ] Tao trang web verify QR <!-- id: 12 -->
  - [ ] Route `/verify_qr?data=...` <!-- id: 12.1 -->
  - [ ] Parse du lieu tu QR → Hien thi ket qua xac thuc <!-- id: 12.2 -->
  - [ ] Hien thi ca: Hash, Signature, Timestamp, AI Check <!-- id: 12.3 -->

- [ ] Test toan bo flow <!-- id: 13 -->
  - [ ] Upload anh → Bat AI check → Ky → Tao QR → Quet QR <!-- id: 13.1 -->
  - [ ] Verify: Kiem tra tat ca thong tin tu QR co chinh xac <!-- id: 13.2 -->

---

## PHASE 5: TOI UU & XU LY LOI

- [ ] Xu ly cac truong hop loi <!-- id: 14 -->
  - [ ] File qua lon (> 10MB) → Canh bao <!-- id: 14.1 -->
  - [ ] Dinh dang file khong ho tro (VD: .txt cho AI) → Thong bao <!-- id: 14.2 -->
  - [ ] AI model khong tai duoc → Fallback che do khong AI <!-- id: 14.3 -->
  - [ ] Timeout neu AI xu ly qua lau (> 30s) <!-- id: 14.4 -->

- [ ] Toi uu hieu suat <!-- id: 15 -->
  - [ ] Cache model AI (khong reload moi lan) <!-- id: 15.1 -->
  - [ ] Nen anh truoc khi AI check (resize 512x512) <!-- id: 15.2 -->
  - [ ] Async processing cho AI (khong block UI) <!-- id: 15.3 -->

- [ ] Cap nhat CSS cho giao dien moi <!-- id: 16 -->
  - [ ] Style checkbox AI Check <!-- id: 16.1 -->
  - [ ] Style hien thi QR code (border, shadow) <!-- id: 16.2 -->
  - [ ] Loading spinner animation <!-- id: 16.3 -->

---

## PHASE 6: VIET TAI LIEU

- [ ] Cap nhat `docs/GIAI_THICH_DU_AN.md` <!-- id: 17 -->
  - [ ] Giai thich QR Code verification <!-- id: 17.1 -->
  - [ ] Giai thich AI Deepfake Detection <!-- id: 17.2 -->
  - [ ] So do luong moi (User → AI Check → RSA Sign → QR) <!-- id: 17.3 -->

- [ ] Tao file moi `docs/AI_VA_QR_HUONG_DAN.md` <!-- id: 18 -->
  - [ ] Huong dan su dung tinh nang AI <!-- id: 18.1 -->
  - [ ] Huong dan quet QR code <!-- id: 18.2 -->
  - [ ] Giai thich AI model su dung (Hugging Face) <!-- id: 18.3 -->
  - [ ] Han che cua AI (khong 100% chinh xac) <!-- id: 18.4 -->

- [ ] Cap nhat `verify_app.py` cho test AI + QR <!-- id: 19 -->
  - [ ] Test case: Ky file voi AI check <!-- id: 19.1 -->
  - [ ] Test case: Tao va doc QR <!-- id: 19.2 -->

---

## PHASE 7: DEMO & GIAI TRINH

- [ ] Chuan bi demo <!-- id: 20 -->
  - [ ] Tai 2-3 anh mau (real + fake) <!-- id: 20.1 -->
  - [ ] Chuan bi script demo (buoc 1, 2, 3...) <!-- id: 20.2 -->
  - [ ] Test demo tren may khac (dam bao chay duoc) <!-- id: 20.3 -->

- [ ] Slides giai trinh <!-- id: 21 -->
  - [ ] Slide 1: Van de (Deepfake la gi? Tai sao nguy hiem?) <!-- id: 21.1 -->
  - [ ] Slide 2: Giai phap (AI + RSA + QR) <!-- id: 21.2 -->
  - [ ] Slide 3: Demo truc tiep <!-- id: 21.3 -->
  - [ ] Slide 4: Ket qua (So sanh voi cach cu) <!-- id: 21.4 -->

---

## UOC LUONG THOI GIAN

- **Phase 1** (Setup): 30 phut
- **Phase 2** (QR Code): 2-3 gio
- **Phase 3** (AI Detection): 3-4 gio
- **Phase 4** (Tich hop): 1-2 gio
- **Phase 5** (Toi uu): 2 gio
- **Phase 6** (Tai lieu): 1 gio
- **Phase 7** (Demo): 1 gio

**TONG**: ~12-15 gio (Chia lam 2 ngay, moi ngay 6-8 gio)

---

## YEU CAU HE THONG

- **RAM**: ≥ 8GB (AI model can ~2GB khi chay)
- **Disk**: ~1GB (model + dependencies)
- **Python**: ≥ 3.8
- **Internet**: Can khi tai model lan dau (500MB)

---

## RUI RO & GIAI PHAP

| Rui Ro | Anh Huong | Giai Phap |
|--------|-----------|-----------|
| AI model qua cham | User phai doi | Them progress bar, resize anh |
| AI khong chinh xac 100% | False positive | Giai thich trong docs, chi la "bo tro" |
| Model qua nang | Khong chay duoc may yeu | Lam che do optional (co the tat AI) |
| QR kho quet | User khong verify duoc | Tang do phan giai QR (300x300px) |

---

## KET QUA MONG DOI

✅ User upload anh → AI check → RSA ky → Tao QR
✅ Quet QR bang dien thoai → Thay tat ca thong tin verify
✅ Phat hien duoc anh bi chinh sua (Photoshop, deepfake)
✅ Do an noi bat, diem cao, demo an tuong!
