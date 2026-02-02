import random
import json
import base64
import sha256_library

# ================= CAC HAM HO TRO TOAN HOC =================

def kiem_tra_nguyen_to(n, k=40):
    """Kiem tra so nguyen to Miller-Rabin."""
    if n == 2 or n == 3: return True
    if n % 2 == 0 or n < 2: return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def tao_so_nguyen_to(bits):
    """Tao mot so nguyen to ngau nhien voi do dai bit cho truoc."""
    while True:
        # Tao so le ngau nhien
        n = random.getrandbits(bits)
        if n % 2 == 0:
            n += 1
        # Kiem tra tinh nguyen to
        if kiem_tra_nguyen_to(n):
            return n

def uoc_chung_lon_nhat(a, b):
    while b:
        a, b = b, a % b
    return a

def nghich_dao_module(a, m):
    """Thuat toan Euclid mo rong de tim nghich dao module."""
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# ================= RSA CORE =================

def tao_cap_khoa_rsa(kich_thuoc_khoa=1024):
    """
    Tao cap khoa Public va Private.
    Tra ve: ((e, n), (d, n))
    """
    # 1. Tao p va q (hai so nguyen to lon)
    # Su dung 512 bit cho p va q de co khoa ~1024 bit
    do_dai_bit = kich_thuoc_khoa // 2
    
    p = tao_so_nguyen_to(do_dai_bit)
    q = tao_so_nguyen_to(do_dai_bit)
    while p == q:
        q = tao_so_nguyen_to(do_dai_bit)

    # 2. Tinh n = p * q
    n = p * q

    # 3. Tinh phi(n) = (p-1)*(q-1)
    phi = (p - 1) * (q - 1)

    # 4. Chon so nguyen e sao cho 1 < e < phi va gcd(e, phi) = 1
    e = 65537 # So mu cong khai tieu chuan
    if uoc_chung_lon_nhat(e, phi) != 1:
        # Fallback neu e khong nguyen to cung nhau (rat hiem)
        e = 3
        while uoc_chung_lon_nhat(e, phi) != 1:
            e += 2

    # 5. Tinh d sao cho d * e = 1 (mod phi)
    d = nghich_dao_module(e, phi)

    # Tra ve ((public), (private))
    return ((e, n), (d, n))

def tinh_hash_sha256(du_lieu):
    """Tra ve gia tri so nguyen cua ma bam SHA-256 su dung thu vien code thuan."""
    digest = sha256_library.tinh_hash_sha256(du_lieu)
    return int(digest, 16)

def ky_so_rsa(du_lieu_bytes, khoa_bi_mat):
    """
    Ky thong diep su dung Khoa Bi Mat (d, n).
    Chu ky s = m^d mod n
    Thong diep 'm' la ma bam cua du lieu.
    """
    d, n = khoa_bi_mat
    
    # 1. Bam thong diep
    m = tinh_hash_sha256(du_lieu_bytes)
    
    # 2. RSA Ky: s = m^d mod n
    chu_ky_int = pow(m, d, n)
    
    # Tra ve chuoi hex
    return hex(chu_ky_int)[2:]

def xac_thuc_chu_ky(du_lieu_bytes, chu_ky_hex, khoa_cong_khai):
    """
    Xac thuc chu ky su dung Khoa Cong Khai (e, n).
    Kiem tra: m' = s^e mod n
    Neu m' == hash(du_lieu), thi hop le.
    """
    e, n = khoa_cong_khai
    
    # 1. Bam thong diep goc
    m = tinh_hash_sha256(du_lieu_bytes)
    
    try:
        chu_ky_int = int(chu_ky_hex, 16)
    except ValueError:
        return False
        
    # 2. RSA Xac thuc: m_prime = s^e mod n
    m_phay = pow(chu_ky_int, e, n)
    
    # 3. So sanh
    return m == m_phay

# ================= HO TRO LUU TRU KHOA =================

def luu_khoa(khoa, ten_file, la_khoa_bi_mat=True):
    """
    Luu khoa vao file duoi dang JSON gia lap PEM.
    khoa: tuple (exp, mod)
    """
    du_lieu_khoa = {
        "exponent": str(khoa[0]),
        "modulus": str(khoa[1]),
        "type": "RSA Private" if la_khoa_bi_mat else "RSA Public"
    }
    json_str = json.dumps(du_lieu_khoa)
    b64_str = base64.b64encode(json_str.encode()).decode()
    
    header = "-----BEGIN RSA PRIVATE KEY-----" if la_khoa_bi_mat else "-----BEGIN RSA PUBLIC KEY-----"
    footer = "-----END RSA PRIVATE KEY-----" if la_khoa_bi_mat else "-----END RSA PUBLIC KEY-----"
    
    with open(ten_file, 'w') as f:
        f.write(f"{header}\n{b64_str}\n{footer}")

def doc_khoa(ten_file):
    """
    Doc khoa tu file dinh dang tuy chinh.
    Tra ve tuple (exp, mod)
    """
    with open(ten_file, 'r') as f:
        noi_dung = f.read().strip()
    
    # Xoa header/footer de lay base64
    cac_dong = noi_dung.splitlines()
    b64_str = ""
    for dong in cac_dong:
        if "BEGIN" in dong or "END" in dong:
            continue
        b64_str += dong.strip()
        
    try:
        json_str = base64.b64decode(b64_str).decode()
        du_lieu = json.loads(json_str)
        return (int(du_lieu["exponent"]), int(du_lieu["modulus"]))
    except Exception as e:
        raise ValueError(f"Dinh dang khoa khong hop le: {e}")
