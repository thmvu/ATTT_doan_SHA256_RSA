from flask import Flask, render_template, request, send_file
import os
import rsa_library  # Thu vien RSA tu viet (Code thuan)
import qr_generator  # Thu vien tao QR code
import ai_detector  # Thu vien phat hien anh gia mao
from datetime import datetime

app = Flask(__name__)

# Cau hinh thu muc
UPLOAD_FOLDER = 'uploads'
SIGN_FOLDER = 'signatures'
KEY_FOLDER = 'keys'
QR_FOLDER = 'qrcodes'  # Thu muc luu ma QR

# Dam bao thu muc ton tai
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SIGN_FOLDER, exist_ok=True)
os.makedirs(KEY_FOLDER, exist_ok=True)
os.makedirs(QR_FOLDER, exist_ok=True)  # Tao thu muc QR

# Ten file khoa
TEN_FILE_KHOA_BI_MAT = "private_key.pem"
TEN_FILE_KHOA_CONG_KHAI = "public_key.pem"

DUONG_DAN_KHOA_BI_MAT = os.path.join(KEY_FOLDER, TEN_FILE_KHOA_BI_MAT)
DUONG_DAN_KHOA_CONG_KHAI = os.path.join(KEY_FOLDER, TEN_FILE_KHOA_CONG_KHAI)

# ================= TAO KHOA RSA =================
def xu_ly_tao_khoa():
    # Su dung thu vien tu viet
    # 1024 bit (Hoac 512 neu may cham)
    cap_khoa = rsa_library.tao_cap_khoa_rsa(1024)
    khoa_cong_khai, khoa_bi_mat = cap_khoa
    
    # Luu khoa vao file
    rsa_library.luu_khoa(khoa_bi_mat, DUONG_DAN_KHOA_BI_MAT, la_khoa_bi_mat=True)
    rsa_library.luu_khoa(khoa_cong_khai, DUONG_DAN_KHOA_CONG_KHAI, la_khoa_bi_mat=False)

# ================= KY FILE =================
def xu_ly_ky_file(duong_dan_file, duong_dan_khoa_rieng=None):
    # Doc Khoa Bi Mat (Tu file rieng hoac khoa chung tren server)
    try:
        if duong_dan_khoa_rieng:
            # Nguoi dung upload khoa rieng
            khoa_bi_mat = rsa_library.doc_khoa(duong_dan_khoa_rieng)
        else:
            # Dung khoa chung tren server (Mac dinh)
            khoa_bi_mat = rsa_library.doc_khoa(DUONG_DAN_KHOA_BI_MAT)
    except Exception as e:
        raise Exception(f"Khong the doc khoa: {e}")

    # Doc du lieu file
    with open(duong_dan_file, "rb") as f:
        du_lieu = f.read()

    # Thuc hien ky
    chu_ky_hex = rsa_library.ky_so_rsa(du_lieu, khoa_bi_mat)

    # Luu chu ky
    ten_file = os.path.basename(duong_dan_file)
    ten_file_chu_ky = f"{ten_file}.sig"
    duong_dan_chu_ky = os.path.join(SIGN_FOLDER, ten_file_chu_ky)

    with open(duong_dan_chu_ky, "w") as f:
        f.write(chu_ky_hex)

    return duong_dan_chu_ky

# ================= XAC THUC FILE =================
def xu_ly_xac_thuc(duong_dan_file, duong_dan_chu_ky):
    # Doc Khoa Cong Khai
    try:
        khoa_cong_khai = rsa_library.doc_khoa(DUONG_DAN_KHOA_CONG_KHAI)
    except Exception:
        return False

    # Doc du lieu file
    with open(duong_dan_file, "rb") as f:
        du_lieu = f.read()

    # Doc chu ky
    with open(duong_dan_chu_ky, "r") as f:
        chu_ky_hex = f.read().strip()

    # Xac thuc
    return rsa_library.xac_thuc_chu_ky(du_lieu, chu_ky_hex, khoa_cong_khai)

# ================= ROUTES (DUONG DAN) =================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tao_khoa', methods=['POST'])
def route_tao_khoa():
    try:
        xu_ly_tao_khoa()
        return render_template('index.html', 
                               message="✅ Da Tao Cap Khoa RSA (Code Thuan) Thanh Cong!", 
                               message_type="success",
                               private_key_file=TEN_FILE_KHOA_BI_MAT,
                               public_key_file=TEN_FILE_KHOA_CONG_KHAI)
    except Exception as e:
        return render_template('index.html', message=f"❌ Loi: {str(e)}", message_type="error")

@app.route('/ky_file', methods=['POST'])
def route_ky_file():
    if 'file' not in request.files:
        return render_template('index.html', message="❌ Khong co file nao duoc gui", message_type="error")
    
    file = request.files['file']
    if file.filename == '':
        return render_template('index.html', message="❌ Chua chon file", message_type="error")

    if file:
        try:
            duong_dan_file = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(duong_dan_file)

            # ====== AI CHECK (TUY CHON) ======
            ai_result = None
            ai_check_enabled = request.form.get('ai_check') == 'true'  # Doc checkbox
            
            if ai_check_enabled:
                # Kiem tra co phai file anh khong
                if ai_detector.la_file_anh(duong_dan_file):
                    # Chay AI metadata check
                    ai_result = ai_detector.kiem_tra_metadata(duong_dan_file)
                    print(f"🤖 AI Check: {ai_result['ly_do']}")
                else:
                    # Khong phai anh → Khong check duoc
                    ai_result = {
                        "hop_le": True,
                        "ly_do": "File khong phai anh, bo qua AI check",
                        "chi_tiet": {}
                    }

            # ====== KY FILE (Giu nguyen code cu) ======
            # Kiem tra xem user co upload Private Key rieng khong
            duong_dan_khoa_rieng = None
            if 'private_key' in request.files and request.files['private_key'].filename != '':
                # User upload Private Key rieng
                private_key_file = request.files['private_key']
                duong_dan_khoa_rieng = os.path.join(UPLOAD_FOLDER, f"temp_{private_key_file.filename}")
                private_key_file.save(duong_dan_khoa_rieng)
            else:
                # Dung khoa chung - kiem tra ton tai
                if not os.path.exists(DUONG_DAN_KHOA_BI_MAT):
                    return render_template('index.html', message="❌ Bao mat: Khong tim thay Khoa Bi Mat!", message_type="error")

            duong_dan_chu_ky = xu_ly_ky_file(duong_dan_file, duong_dan_khoa_rieng)
            
            # Xoa Private Key tam thoi neu co
            if duong_dan_khoa_rieng and os.path.exists(duong_dan_khoa_rieng):
                os.remove(duong_dan_khoa_rieng)
            
            # ====== TAO QR CODE (TU DONG) ======
            qr_file_name = None
            try:
                # Doc chu ky (hex string)
                with open(duong_dan_chu_ky, "r") as f:
                    chu_ky_hex = f.read().strip()
                
                # Tao du lieu cho QR
                qr_data = {
                    "file_name": file.filename,
                    "signature_short": chu_ky_hex[:30] + "...",  # Chi lay 30 ky tu dau (QR nhe hon)
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "ai_status": "PASS" if (not ai_result or ai_result['hop_le']) else "WARNING"
                }
                
                # Ten file QR
                qr_file_name = f"{file.filename}.qr.png"
                qr_path = os.path.join(QR_FOLDER, qr_file_name)
                
                # Tao QR code
                qr_generator.tao_ma_qr(qr_data, qr_path)
                print(f"✅ Da tao QR code: {qr_file_name}")
                
            except Exception as qr_error:
                print(f"⚠️ Loi tao QR (khong anh huong ky file): {qr_error}")
                # Khong loi ky file, chi khong co QR thoi
            
            # ====== TRA VE KET QUA ======
            return render_template('index.html', 
                                   message="✅ Da Ky File Thanh Cong (RSA Pure)!", 
                                   message_type="success",
                                   signature_file=os.path.basename(duong_dan_chu_ky),
                                   qr_file=qr_file_name,  # Truyen ten file QR
                                   ai_result=ai_result)  # Truyen ket qua AI
        except Exception as e:
            return render_template('index.html', message=f"❌ Loi khi ky file: {str(e)}", message_type="error")


@app.route('/kiem_tra', methods=['POST'])
def route_kiem_tra():
    if 'file' not in request.files or 'signature' not in request.files:
         return render_template('index.html', message="❌ Thieu file goc hoac file chu ky", message_type="error")

    file = request.files['file']
    file_chu_ky = request.files['signature']

    if file.filename == '' or file_chu_ky.filename == '':
        return render_template('index.html', message="❌ Chua chon du file", message_type="error")

    try:
        duong_dan_file = os.path.join(UPLOAD_FOLDER, file.filename)
        duong_dan_chu_ky = os.path.join(SIGN_FOLDER, file_chu_ky.filename)

        file.save(duong_dan_file)
        file_chu_ky.save(duong_dan_chu_ky)

        if not os.path.exists(DUONG_DAN_KHOA_CONG_KHAI):
             return render_template('index.html', message="❌ Khong tim thay Khoa Cong Khai!", message_type="error")

        ket_qua = xu_ly_xac_thuc(duong_dan_file, duong_dan_chu_ky)

        if ket_qua:
            tin_nhan = "✅ TOAN VEN DU LIEU DUOC XAC NHAN: File Chuan Authentic."
            kieu_tin_nhan = "success"
        else:
            tin_nhan = "❌ CANH BAO: File Da Bi Thay Doi Hoac Chu Ky Khong Hop Le."
            kieu_tin_nhan = "error"
            
        return render_template('index.html', message=tin_nhan, message_type=kieu_tin_nhan)
    except Exception as e:
        return render_template('index.html', message=f"❌ Loi xac thuc: {str(e)}", message_type="error")

@app.route('/tai_chu_ky/<filename>')
def route_tai_chu_ky(filename):
    return send_file(os.path.join(SIGN_FOLDER, filename), as_attachment=True)

@app.route('/tai_qr/<filename>')
def route_tai_qr(filename):
    return send_file(os.path.join(QR_FOLDER, filename), as_attachment=True)

@app.route('/tai_khoa/<filename>')
def route_tai_khoa(filename):
    if filename not in [TEN_FILE_KHOA_BI_MAT, TEN_FILE_KHOA_CONG_KHAI]:
        return "Tu choi truy cap", 403
    return send_file(os.path.join(KEY_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
