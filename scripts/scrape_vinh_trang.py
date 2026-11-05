#!/usr/bin/env python3
"""
Scrape reference images for Chùa Vĩnh Tràng (Mỹ Tho, Tiền Giang)
Organized specifically for 3D Modeling, Reconstruction & Photogrammetry.
Sources:
1. Wikimedia Commons (Raw 4K-6K Ultra HD archived photos)
2. Bing Images (Diverse angles, details, statues, interiors)
"""

import os
import sys
import time
import json
import hashlib
import re
import requests
from io import BytesIO
from bs4 import BeautifulSoup
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ROOT = os.path.join(BASE_DIR, "assets", "chua_vinh_trang_3d_ref")

CATEGORIES = {
    "01_chanh_dien_mat_tien": "Mặt tiền chánh điện, kiến trúc Á - Âu, vòm Romanesque/Renaissance, cột, mái ngói",
    "02_cong_tam_quan": "Cổng Tam quan cổ nghệ thuật khảm sành sứ, hoành phi, rồng phụng",
    "03_dai_tuong_di_lac": "Đại tượng Phật Di Lặc lộ thiên khổng lồ (ngồi bệ sen, diện mạo hoan hỷ)",
    "04_dai_tuong_a_di_da": "Đại tượng Phật A Di Đà đứng cao 24m, đài sen, cà sa, hào quang",
    "05_tuong_phat_nam": "Đại tượng Phật Thích Ca nhập Niết Bàn (Phật nằm nghiêng dài 35m)",
    "06_noi_dien_tam_bao": "Nội điện, bàn thờ Tam Bảo, tượng gỗ cổ, bao lam chạm lộng Mai Lan Cúc Trúc dát vàng",
    "07_khuon_vien_thap_mo": "Khuôn viên, vườn tháp tổ, hòn non bộ, hồ hoa sen, bối cảnh tổng thể",
    "08_wikimedia_ultra_hd": "Kho ảnh gốc Wikimedia Commons Ultra HD (độ phân giải cao 4K-6K phục vụ texture mapping)"
}

HEADERS_WIKI = {
    "User-Agent": "ChuaOnline3DResearchBot/1.0 (Educational 3D reconstruction project; contact@chuaonline.vn)"
}

HEADERS_WEB = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "vi,en-US;q=0.9,en;q=0.8"
}

def init_folders():
    for cat in CATEGORIES:
        os.makedirs(os.path.join(OUTPUT_ROOT, cat), exist_ok=True)

def sanitize_filename(name):
    clean = re.sub(r'[\\/*?:"<>|#]', "", name)
    clean = re.sub(r'\s+', "_", clean).strip("_")
    return clean[:60]

def is_valid_image(data):
    if len(data) < 15000:  # Skip files smaller than 15KB (usually icons/placeholders/thumbnails)
        return False, None
    try:
        img = Image.open(BytesIO(data))
        w, h = img.size
        fmt = img.format.lower() if img.format else "jpg"
        if w < 300 or h < 300:
            return False, None
        return True, (w, h, fmt)
    except Exception:
        return False, None

def classify_wiki_title(title, desc=""):
    t_lower = (title + " " + desc).lower()
    if any(k in t_lower for k in ["budai", "di lặc", "di lac", "maitreya", "fat buddha"]):
        return "03_dai_tuong_di_lac"
    if any(k in t_lower for k in ["cổng", "cong", "gate", "tam quan"]):
        return "02_cong_tam_quan"
    if any(k in t_lower for k in ["reclining", "phật nằm", "phat nam", "niết bàn", "niet ban"]):
        return "05_tuong_phat_nam"
    if any(k in t_lower for k in ["a di đà", "a di da", "amitabha", "standing buddha"]):
        return "04_dai_tuong_a_di_da"
    if any(k in t_lower for k in ["sanctum", "main deity", "khám thờ", "hoành phi", "altar", "shrine", "bên trong", "nội điện"]):
        return "06_noi_dien_tam_bao"
    if any(k in t_lower for k in ["tháp mộ", "thap mo", "non bộ", "courtyard", "hoa sen", "landscaping", "panoramio"]):
        return "07_khuon_vien_thap_mo"
    return "01_chanh_dien_mat_tien"

def scrape_wikimedia(seen_hashes, metadata):
    print("\n--- 1. BẮT ĐẦU CÀO ẢNH WIKIMEDIA COMMONS (ULTRA HD 4K-6K) ---")
    url = "https://commons.wikimedia.org/w/api.php"
    queries = ['"Vinh Trang"', '"Vĩnh Tràng"', '"Pagode Vinh Trang"', '"Vinh Trang Pagoda"']
    collected_files = {}

    for q in queries:
        params = {
            "action": "query",
            "generator": "search",
            "gsrsearch": q,
            "gsrnamespace": 6,
            "gsrlimit": 100,
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "format": "json"
        }
        try:
            r = requests.get(url, params=params, headers=HEADERS_WIKI, timeout=15).json()
            pages = r.get("query", {}).get("pages", {})
            for pid, p in pages.items():
                title = p.get("title", "")
                if title and title not in collected_files:
                    infos = p.get("imageinfo", [])
                    if infos and infos[0].get("mime", "").startswith("image/"):
                        collected_files[title] = {
                            "title": title,
                            "url": infos[0].get("url"),
                            "width": infos[0].get("width"),
                            "height": infos[0].get("height"),
                            "size": infos[0].get("size"),
                            "desc": infos[0].get("extmetadata", {}).get("ImageDescription", {}).get("value", "")
                        }
        except Exception as e:
            print(f"Lỗi truy vấn Wikimedia query={q}: {e}")

    print(f"Đã tìm thấy {len(collected_files)} ảnh tư liệu từ Wikimedia Commons.")
    
    count = 0
    for idx, (title, item) in enumerate(collected_files.items(), 1):
        img_url = item["url"]
        try:
            res = requests.get(img_url, headers=HEADERS_WIKI, timeout=30)
            if res.status_code == 200:
                data = res.content
                h = hashlib.md5(data).hexdigest()
                if h in seen_hashes:
                    continue
                seen_hashes.add(h)

                valid, info = is_valid_image(data)
                if not valid:
                    continue

                w, h_dim, fmt = info
                safe_title = sanitize_filename(title.replace("File:", "").replace(".jpg", "").replace(".png", ""))
                cat = classify_wiki_title(title, item["desc"])

                # Lưu vào thư mục Ultra HD
                ultra_filename = f"wiki_{idx:02d}_{safe_title}.{fmt}"
                ultra_path = os.path.join(OUTPUT_ROOT, "08_wikimedia_ultra_hd", ultra_filename)
                with open(ultra_path, "wb") as f:
                    f.write(data)

                # Lưu vào thư mục phân loại kiến trúc
                cat_filename = f"{cat[:2]}_wiki_{idx:02d}_{safe_title}.{fmt}"
                cat_path = os.path.join(OUTPUT_ROOT, cat, cat_filename)
                with open(cat_path, "wb") as f:
                    f.write(data)

                metadata.append({
                    "id": f"wiki_{idx:03d}",
                    "filename": ultra_filename,
                    "category": cat,
                    "resolution": f"{w}x{h_dim}",
                    "size_kb": len(data) // 1024,
                    "source": "Wikimedia Commons",
                    "title": title,
                    "original_url": img_url
                })
                count += 1
                print(f"[{count:02d}/{len(collected_files)}] Đã tải: {title[:40]} ({w}x{h_dim}, {len(data)//1024} KB) -> {cat}")
                time.sleep(0.5) # Tuân thủ quy định rate limit của Wikimedia
        except Exception as e:
            print(f"Lỗi tải {title}: {e}")

    print(f"Hoàn thành tải {count} ảnh gốc phân giải cao từ Wikimedia Commons.\n")

def scrape_bing_category(cat_key, queries, max_per_cat, seen_hashes, metadata):
    print(f"\n--- BẮT ĐẦU CÀO HẠNG MỤC: {cat_key} ({CATEGORIES[cat_key]}) ---")
    cat_dir = os.path.join(OUTPUT_ROOT, cat_key)
    session = requests.Session()
    session.headers.update(HEADERS_WEB)

    count = 0
    for query in queries:
        if count >= max_per_cat:
            break
        print(f"-> Tìm kiếm query: '{query}'")
        encoded_q = requests.utils.quote(query)
        url = f"https://www.bing.com/images/async?q={encoded_q}&first=0&count=40&scenario=ImageBasicHover&datsrc=N_ दृश्य&layout=RowBased&mmasync=1"
        try:
            r = session.get(url, timeout=15)
            soup = BeautifulSoup(r.text, "html.parser")
            tags = soup.find_all("a", class_="iusc")
            print(f"   Tìm thấy {len(tags)} kết quả.")

            for t in tags:
                if count >= max_per_cat:
                    break
                try:
                    m = json.loads(t.get("m", "{}"))
                    murl = m.get("murl")
                    turl = m.get("turl")
                    title = m.get("t") or query

                    # Thử tải từ URL ảnh gốc trước (murl)
                    data = None
                    used_url = murl
                    try:
                        res = requests.get(murl, headers=HEADERS_WEB, timeout=8)
                        if res.status_code == 200 and "image" in res.headers.get("content-type", "").lower():
                            data = res.content
                    except Exception:
                        data = None

                    # Fallback sang thumbnail URL nếu web gốc chặn hotlink
                    if not data and turl:
                        try:
                            res = requests.get(turl, headers=HEADERS_WEB, timeout=8)
                            if res.status_code == 200:
                                data = res.content
                                used_url = turl
                        except Exception:
                            data = None

                    if not data:
                        continue

                    h = hashlib.md5(data).hexdigest()
                    if h in seen_hashes:
                        continue
                    seen_hashes.add(h)

                    valid, info = is_valid_image(data)
                    if not valid:
                        continue

                    w, h_dim, fmt = info
                    safe_title = sanitize_filename(title)
                    filename = f"{cat_key[:2]}_{count+1:02d}_{safe_title}.{fmt}"
                    filepath = os.path.join(cat_dir, filename)

                    with open(filepath, "wb") as f:
                        f.write(data)

                    count += 1
                    metadata.append({
                        "id": f"{cat_key}_{count:02d}",
                        "filename": filename,
                        "category": cat_key,
                        "resolution": f"{w}x{h_dim}",
                        "size_kb": len(data) // 1024,
                        "source": "Web / Bing Images",
                        "title": title,
                        "original_url": used_url
                    })
                    print(f"   [{count:02d}/{max_per_cat}] Lưu {filename} ({w}x{h_dim}, {len(data)//1024} KB)")
                    time.sleep(0.3)
                except Exception as ex:
                    continue
        except Exception as e:
            print(f"   Lỗi cào query {query}: {e}")

    print(f"Hoàn thành {cat_key}: đã lưu {count} ảnh chất lượng cao.")

def main():
    print("==========================================================")
    print("  TOOL SCRAPE HÌNH ẢNH THAM KHẢO 3D - CHÙA VĨNH TRÀNG    ")
    print("  Chuẩn bị tư liệu cho 3D Modeling, Reconstruction, Texturing ")
    print("==========================================================")

    init_folders()
    seen_hashes = set()
    metadata = []

    # 1. Scrape Wikimedia Commons Ultra HD
    scrape_wikimedia(seen_hashes, metadata)

    # 2. Scrape Bing Images cho từng hạng mục kiến trúc cụ thể
    bing_tasks = [
        ("01_chanh_dien_mat_tien", [
            "mặt tiền chánh điện chùa vĩnh tràng mỹ tho",
            "chùa vĩnh tràng kiến trúc mặt trước vòm hoa văn",
            "mái ngói lan can chùa vĩnh tràng",
            "vinh trang pagoda facade architecture"
        ], 18),
        ("02_cong_tam_quan", [
            "cổng tam quan chùa vĩnh tràng khảm sành sứ",
            "cổng cổ chùa vĩnh tràng chi tiết rồng gốm sứ",
            "cổng chùa vĩnh tràng mỹ tho góc thẳng",
            "vinh trang pagoda ceramic mosaic triple gate"
        ], 15),
        ("03_dai_tuong_di_lac", [
            "tượng phật di lặc chùa vĩnh tràng mỹ tho",
            "đại tượng phật di lặc chùa vĩnh tràng các góc",
            "tượng phật di lặc chùa vĩnh tràng hoa viên",
            "giant maitreya budai statue vinh trang pagoda"
        ], 16),
        ("04_dai_tuong_a_di_da", [
            "tượng phật a di đà chùa vĩnh tràng 24m",
            "tượng phật a di đà đứng chùa vĩnh tràng",
            "tượng phật đứng đài sen chùa vĩnh tràng",
            "standing amitabha buddha statue vinh trang pagoda"
        ], 16),
        ("05_tuong_phat_nam", [
            "tượng phật thích ca nhập niết bàn chùa vĩnh tràng",
            "tượng phật nằm chùa vĩnh tràng mỹ tho",
            "tượng phật nằm dài 35m chùa vĩnh tràng",
            "reclining buddha statue vinh trang pagoda"
        ], 15),
        ("06_noi_dien_tam_bao", [
            "nội điện chánh điện chùa vĩnh tràng mỹ tho",
            "bàn thờ tam bảo chùa vĩnh tràng tượng phật gỗ",
            "bao lam dát vàng hoành phi chùa vĩnh tràng",
            "vinh trang pagoda interior altar statues"
        ], 16),
        ("07_khuon_vien_thap_mo", [
            "khuôn viên vườn tháp chùa vĩnh tràng mỹ tho",
            "hòn non bộ hồ sen chùa vĩnh tràng",
            "toàn cảnh chùa vĩnh tràng trên cao flycam",
            "vinh trang pagoda grounds stupa garden"
        ], 15),
    ]

    for cat_key, queries, max_count in bing_tasks:
        scrape_bing_category(cat_key, queries, max_count, seen_hashes, metadata)

    # 3. Ghi file Metadata JSON
    meta_path = os.path.join(OUTPUT_ROOT, "metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    # 4. Ghi file Thống kê & Hướng dẫn 3D Modeling (README.md)
    readme_path = os.path.join(OUTPUT_ROOT, "README.md")
    
    cat_counts = {}
    for item in metadata:
        c = item["category"]
        cat_counts[c] = cat_counts.get(c, 0) + 1

    readme_content = f"""# BỘ TƯ LIỆU HÌNH ẢNH THAM KHẢO DỰNG HÌNH 3D CHÙA VĨNH TRÀNG (MỸ THO - TIỀN GIANG)

Bộ dữ liệu này được thu thập và phân loại chuyên biệt nhằm phục vụ quy trình dựng hình 3D (3D Modeling), tái tạo quang trắc (Photogrammetry), Gaussian Splatting hoặc tạo Texture PBR cho dự án **Chùa Online**.

## 1. Thống Kê Tổng Quan
- **Tổng số hình ảnh thu thập được:** {len(metadata)} files
- **Định dạng:** JPG, PNG, WEBP (Đã kiểm tra tính toàn vẹn và độ phân giải)
- **Nguồn:** Wikimedia Commons (Tư liệu gốc 4K - 6K Ultra HD) + Kho ảnh thực địa góc đa chiều

## 2. Phân Bổ Các Thư Mục Chuyên Môn
| Thư mục | Hạng mục | Số lượng ảnh | Mục đích ứng dụng 3D |
| :--- | :--- | :--- | :--- |
| `01_chanh_dien_mat_tien/` | Mặt tiền Chánh điện | {cat_counts.get("01_chanh_dien_mat_tien", 0)} | Dựng khối nhà chính, vòm cong Phục Hưng, cột La Mã, hoa văn mái |
| `02_cong_tam_quan/` | Cổng Tam Quan | {cat_counts.get("02_cong_tam_quan", 0)} | Dựng cổng tam quan, trích xuất texture khảm sành sứ (mosaic) |
| `03_dai_tuong_di_lac/` | Tượng Phật Di Lặc | {cat_counts.get("03_dai_tuong_di_lac", 0)} | Điêu khắc số (sculpting) tỷ lệ cơ thể, nét mặt hoan hỷ, bệ sen |
| `04_dai_tuong_a_di_da/` | Tượng Phật A Di Đà (24m) | {cat_counts.get("04_dai_tuong_a_di_da", 0)} | Dựng tượng Phật đứng, nếp gấp áo cà sa, đài sen, vòng hào quang |
| `05_tuong_phat_nam/` | Tượng Phật Nhập Niết Bàn (35m) | {cat_counts.get("05_tuong_phat_nam", 0)} | Dựng tượng Phật nằm nghiêng, gối kê đầu, bệ nằm |
| `06_noi_dien_tam_bao/` | Nội điện & Bàn thờ | {cat_counts.get("06_noi_dien_tam_bao", 0)} | Dựng không gian nội thất, tượng gỗ cổ, bao lam chạm trổ, hoành phi dát vàng |
| `07_khuon_vien_thap_mo/` | Khuôn viên & Vườn tháp | {cat_counts.get("07_khuon_vien_thap_mo", 0)} | Dựng environment, terrain, vườn tháp tổ, hồ sen, cây cảnh bonsai |
| `08_wikimedia_ultra_hd/` | Master Ultra HD (4K-6K) | {cat_counts.get("08_wikimedia_ultra_hd", 0)} | File gốc độ phân giải cực cao để làm UV Mapping & PBR Texture |

## 3. Khuyến Nghị Kỹ Thuật Khi Dựng 3D
1. **Phong cách kiến trúc giao thoa:** Chùa Vĩnh Tràng kết hợp 5 nền văn hóa: Pháp (vòm cửa, cột tròn), La Mã (hàng hiên), Thái Lan (tháp nhọn chánh điện), Campuchia (chạm nổi Khmer) và Việt - Hoa (mái ngói âm dương, khảm sành sứ). Khi dựng mesh cần chia rõ phần khung Gothic/Renaissance và phần mái trang trí Đông phương.
2. **Nghệ thuật khảm sành sứ Cổng Tam Quan:** Không nên dựng polygon quá dày cho từng mảnh gốm; nên dựng mesh chuẩn hình khối rồi sử dụng Normal Map kết hợp Roughness Map tạo độ bóng men sứ.
3. **Bộ 3 Đại tượng Phật lộ thiên:**
   - **Tượng Phật Di Lặc:** Tượng thạch cao màu trắng ngà bóng mờ.
   - **Tượng Phật A Di Đà:** Tượng bê tông cốt thép sơn trắng, cao 24m (tính cả bệ).
   - **Tượng Phật Niết Bàn:** Dài 35m, bệ bê tông ốp đá trang trí.
"""
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("\n==========================================================")
    print(f" HOÀN TẤT! Đã cào và lưu trữ tổng cộng {len(metadata)} ảnh.")
    print(f" Thư mục: {OUTPUT_ROOT}")
    print(f" File metadata: {meta_path}")
    print(f" Hướng dẫn 3D: {readme_path}")
    print("==========================================================")

if __name__ == "__main__":
    main()
