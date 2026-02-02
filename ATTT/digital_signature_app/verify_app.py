from app import xu_ly_tao_khoa, xu_ly_ky_file, xu_ly_xac_thuc, DUONG_DAN_KHOA_BI_MAT, DUONG_DAN_KHOA_CONG_KHAI, SIGN_FOLDER
import os
import shutil

def chay_kiem_thu_tu_dong():
    print("--- Bat dau Kiem Thu Tu Dong (Code Thuan) ---")
    
    # Xoa khoa cu
    if os.path.exists(DUONG_DAN_KHOA_BI_MAT): os.remove(DUONG_DAN_KHOA_BI_MAT)
    if os.path.exists(DUONG_DAN_KHOA_CONG_KHAI): os.remove(DUONG_DAN_KHOA_CONG_KHAI)

    # 1. Tao Khoa
    print("[1/4] Kiem tra Tao Khoa...")
    try:
        xu_ly_tao_khoa()
        if os.path.exists(DUONG_DAN_KHOA_BI_MAT) and os.path.exists(DUONG_DAN_KHOA_CONG_KHAI):
            print("   [DAT] Tao khoa thanh cong.")
        else:
            print("   [TRUOT] Khong tim thay file khoa.")
            return
    except Exception as e:
        print(f"   [TRUOT] Loi khi tao khoa: {e}")
        return

    # 2. Tao file gia
    file_mau = "test_doc_verify_pure.txt"
    with open(file_mau, "w") as f:
        f.write("Du lieu mat can bao ve")
    
    # 3. Ky
    print("[2/4] Kiem tra Ky So...")
    try:
        duong_dan_chu_ky = xu_ly_ky_file(file_mau)
        if os.path.exists(duong_dan_chu_ky):
            print(f"   [DAT] Chu ky duoc tao tai {duong_dan_chu_ky}")
        else:
            print("   [TRUOT] File chu ky khong duoc tao.")
            return
    except Exception as e:
        print(f"   [TRUOT] Loi khi ky: {e}")
        return

    # 4. Xac thuc dung
    print("[3/4] Kiem tra Xac Thuc (Truong hop Dung)...")
    try:
        hop_le = xu_ly_xac_thuc(file_mau, duong_dan_chu_ky)
        if hop_le:
            print("   [DAT] File hop le duoc xac nhan dung.")
        else:
            print("   [TRUOT] File hop le bi bao loi.")
    except Exception as e:
        print(f"   [TRUOT] Loi khi xac thuc dung: {e}")

    # 5. Xac thuc sai (Sua file)
    print("[4/4] Kiem tra Xac Thuc (Truong hop Sai/Hack)...")
    try:
        with open(file_mau, "a") as f:
            f.write(" [DA BI HACK]")
        
        hop_le = xu_ly_xac_thuc(file_mau, duong_dan_chu_ky)
        if not hop_le:
            print("   [DAT] File bi sua doi da bi phat hien.")
        else:
            print("   [TRUOT] File bi sua doi nhung van chap nhan (Loi Bao Mat!).")
    except Exception as e:
        print(f"   [TRUOT] Loi khi xac thuc sai: {e}")

    # Don dep
    if os.path.exists(file_mau): os.remove(file_mau)
    if os.path.exists(duong_dan_chu_ky): os.remove(duong_dan_chu_ky)
    
    print("--- Hoan tat Kiem Thu ---")

if __name__ == "__main__":
    chay_kiem_thu_tu_dong()
