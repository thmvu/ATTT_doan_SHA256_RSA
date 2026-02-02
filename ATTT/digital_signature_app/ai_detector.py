"""
MODULE PHAT HIEN ANH GIA MAO (AI DETECTION)

Chuc nang: Kiem tra anh co bi chinh sua khong (Photoshop, GIMP...)
Cach thuc: Doc metadata EXIF (KHONG can AI model nang)
"""

from PIL import Image
from PIL.ExifTags import TAGS
import os


def la_file_anh(file_path):
    """
    Kiem tra file co phai la anh khong (qua extension)
    
    Args:
        file_path (str): Duong dan file
    
    Returns:
        True neu la anh, False neu khong
    """
    # Lay phan mo rong file (VD: .jpg, .png)
    ext = os.path.splitext(file_path)[1].lower()
    
    # Danh sach dinh dang anh ho tro
    dinh_dang_anh = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    
    return ext in dinh_dang_anh


def kiem_tra_metadata(file_path):
    """
    Phat hien anh bi chinh sua qua EXIF metadata
    
    EXIF la gi? 
    - La thong tin embed trong anh (camera, thoi gian, phan mem chinh sua...)
    - Neu anh qua Photoshop/GIMP → Co dau viet trong EXIF
    
    Args:
        file_path (str): Duong dan file anh
    
    Returns:
        dict: {
            "hop_le": True/False,
            "ly_do": "Vi sao hop le hoac khong hop le",
            "chi_tiet": {...metadata...}
        }
    """
    try:
        
        image = Image.open(file_path)
        
        
        exif_data = image.getexif()
        
        # Truong hop 1: Anh khong co EXIF (Binh thuong voi mot so anh)
        if not exif_data:
            return {
                "hop_le": True,
                "ly_do": "Khong co metadata EXIF (Anh thong thuong)",
                "chi_tiet": {}
            }
        
        # Chuyen EXIF thanh dictionary de doc
        metadata = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)  # Chuyen ID thanh ten (VD: 271 → "Make")
            metadata[tag_name] = str(value)
        
        #  field "Software" 
        software = metadata.get("Software", "").lower()
        
        
        phan_mem_chinh_sua = [
            "photoshop",    # Adobe Photoshop
            "gimp",         # GIMP
            "paint.net",    # Paint.NET
            "pixlr",        # Pixlr Editor
            "lightroom",    # Adobe Lightroom
            "affinity"      # Affinity Photo
        ]
        
        # Kiem tra phan mem chinh sua nao khong
        for tool in phan_mem_chinh_sua:
            if tool in software:
                return {
                    "hop_le": False,  # PHAT HIEN!
                    "ly_do": f"Phat hien phan mem chinh sua: {metadata.get('Software')}",
                    "chi_tiet": metadata
                }
        
        # Co EXIF nhung khong phat hien chinh sua
        return {
            "hop_le": True,
            "ly_do": "Khong phat hien dau hieu chinh sua",
            "chi_tiet": metadata
        }
        
    except Exception as e:
        # Loi doc file → Bo qua, coi nhu hop le
        return {
            "hop_le": True,
            "ly_do": f"Khong the doc metadata: {e}",
            "chi_tiet": {}
        }


# ====== TEST CODE ======
if __name__ == "__main__":
    # Test voi file anh bat ky
    test_file = "test_image.jpg"
    
    # Kiem tra co phai anh khong
    if la_file_anh(test_file):
        print(f"✅ {test_file} la file anh")
        
        # Kiem tra metadata
        result = kiem_tra_metadata(test_file)
        print(f"\nKet qua AI check:")
        print(f"  Hop le: {result['hop_le']}")
        print(f"  Ly do: {result['ly_do']}")
        if result['chi_tiet']:
            print(f"  Chi tiet metadata: {result['chi_tiet']}")
    else:
        print(f"❌ {test_file} khong phai anh")
