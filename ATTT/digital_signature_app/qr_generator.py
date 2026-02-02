"""
MODULE TAO MA QR CODE

Chuc nang: Tao ma QR code chua thong tin chu ky
Su dung: qrcode library (Don gian, khong can GPU)
"""

import qrcode
import json
import os


def tao_ma_qr(du_lieu_dict, duong_dan_output):
    """
    Tao ma QR tu dictionary data
    
    VD: 
    du_lieu = {
        "file_name": "anh.jpg",
        "signature": "abc123...",
        "timestamp": "2026-02-02 22:00",
        "ai_status": "PASS"
    }
    
    Args:
        du_lieu_dict (dict): Du lieu can chua trong QR
        duong_dan_output (str): Duong dan luu file QR (VD: "qrcodes/anh.jpg.qr.png")
    
    Returns:
        True neu thanh cong, False neu loi
    """
    try:
        # Buoc 1: Chuyen dictionary thanh chuoi JSON (de doc)
        json_data = json.dumps(du_lieu_dict, ensure_ascii=False, indent=2)
        
        # Buoc 2: Tao doi tuong QR
        qr = qrcode.QRCode(
            version=1,  # Kich co QR (1 = nho nhat, tu dong lon len neu can)
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Chiu loi cao (30%)
            box_size=10,  # Kich co moi o vuong
            border=4,  # Vien QR (so o)
        )
        
        # Buoc 3: Them du lieu vao QR
        qr.add_data(json_data)
        qr.make(fit=True)  # Tu dong dieu chinh kich co
        
        # Buoc 4: Tao anh QR (den/trang)
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Buoc 5: Luu anh QR ra file
        img.save(duong_dan_output)
        
        print(f"✅ Da tao QR code: {duong_dan_output}")
        return True
        
    except Exception as e:
        print(f"❌ Loi tao QR: {e}")
        return False


# ====== TEST CODE (Chi chay khi chay truc tiep file nay) ======
if __name__ == "__main__":
    # Test tao QR
    du_lieu_test = {
        "file_name": "test_image.jpg",
        "signature": "a1b2c3d4e5...",
        "timestamp": "2026-02-02 22:30",
        "ai_status": "PASS"
    }
    
    tao_ma_qr(du_lieu_test, "test_qr.png")
    print("Tao test_qr.png xong! Hay quet bang dien thoai de kiem tra.")
