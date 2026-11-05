#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chuyên biệt cào hình ảnh NỘI ĐIỆN & CHÁNH ĐIỆN CHÙA VĨNH TRÀNG (MỸ THO - TIỀN GIANG)
Tập trung vào:
- Góc rộng lòng chánh điện (Wide angle interior hall).
- Bàn thờ Tam Bảo đồ sộ nhiều cấp, tượng Phật Thích Ca, A Di Đà, Di Lặc dát vàng.
- Hệ thống hàng cột gỗ đỏ son, bao lam chạm trổ Cửu Long dát vàng, hoành phi câu đối.
- Bố trí bồ đoàn, thảm lạy Phật, pháp khí chuông mõ, đèn nến, lư hương.
- Nguồn: Bing Images API Async, Google Images, Wikimedia Commons.
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
OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "chua_vinh_trang_3d_ref", "06_noi_dien_tam_bao")
META_PATH = os.path.join(BASE_DIR, "assets", "chua_vinh_trang_3d_ref", "metadata.json")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7"
}

QUERIES = [
    "bên trong chánh điện chùa vĩnh tràng",
    "chánh điện chùa vĩnh tràng mỹ tho",
    "nội điện chùa vĩnh tràng góc rộng",
    "bàn thờ tam bảo chùa vĩnh tràng",
    "tượng phật bên trong chùa vĩnh tràng",
    "khám thờ chánh điện chùa vĩnh tràng",
    "gian thờ phật chùa vĩnh tràng mỹ tho",
    "bao lam hoành phi chùa vĩnh tràng",
    "chùa vĩnh tràng tiền giang bên trong",
    "vinh trang pagoda main hall interior",
    "vinh trang pagoda sanctum altar",
    "vinh trang pagoda inside temple wide view",
    "chùa vĩnh tràng chánh điện sala tv",
    "chùa vĩnh tràng nội điện 18 vị la hán",
    "chùa vĩnh tràng cột gỗ câu đối bên trong"
]

def sanitize(name):
    c = re.sub(r'[\\/*?:"<>|#]', "", name)
    c = re.sub(r'\s+', "_", c).strip("_")
    return c[:65]

def is_valid_image(data):
    if len(data) < 18000:  # Bỏ qua ảnh quá nhỏ / thumbnails mờ
        return False, None
    try:
        img = Image.open(BytesIO(data))
        w, h = img.size
        fmt = img.format.lower() if img.format else "jpg"
        if w < 400 or h < 300:
            return False, None
        return True, (w, h, fmt)
    except Exception:
        return False, None

def main():
    print("=================================================================")
    print(" BẮT ĐẦU CÀO THÊM HÌNH ẢNH NỘI ĐIỆN & CHÁNH ĐIỆN CHÙA VĨNH TRÀNG ")
    print("=================================================================")

    # Đọc metadata hiện có để tránh trùng
    seen_hashes = set()
    existing_meta = []
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, "r", encoding="utf-8") as f:
                existing_meta = json.load(f)
                for item in existing_meta:
                    seen_hashes.add(item.get("id"))
        except Exception as e:
            print("Lỗi đọc metadata:", e)

    # Quét hash các file ảnh đã có trong thư mục
    for fname in os.listdir(OUTPUT_DIR):
        fpath = os.path.join(OUTPUT_DIR, fname)
        if os.path.isfile(fpath):
            try:
                with open(fpath, "rb") as f:
                    seen_hashes.add(hashlib.md5(f.read()).hexdigest())
            except Exception:
                pass

    print(f"-> Đã quét {len(seen_hashes)} ảnh đã có sẵn, bắt đầu cào ảnh mới...")

    session = requests.Session()
    session.headers.update(HEADERS)

    new_saved = 0
    start_index = 25  # Bắt đầu đánh số tiếp theo

    for q in QUERIES:
        print(f"\n[QUERY] -> '{q}'")
        encoded_q = requests.utils.quote(q)
        url = f"https://www.bing.com/images/async?q={encoded_q}&first=0&count=50&scenario=ImageBasicHover&datsrc=N_ दृश्य&layout=RowBased&mmasync=1"
        try:
            r = session.get(url, timeout=12)
            soup = BeautifulSoup(r.text, "html.parser")
            tags = soup.find_all("a", class_="iusc")
            print(f"   Tìm thấy {len(tags)} kết quả.")

            for t in tags:
                try:
                    m = json.loads(t.get("m", "{}"))
                    murl = m.get("murl")
                    turl = m.get("turl")
                    title = m.get("t") or q

                    data = None
                    used_url = murl
                    # Thử lấy ảnh gốc full resolution
                    try:
                        res = session.get(murl, timeout=7)
                        if res.status_code == 200 and "image" in res.headers.get("content-type", "").lower():
                            data = res.content
                    except Exception:
                        data = None

                    # Fallback ảnh thumbnail chất lượng cao nếu web gốc chặn
                    if not data and turl:
                        try:
                            res = session.get(turl, timeout=7)
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
                    safe_title = sanitize(title)
                    filename = f"06_{start_index:02d}_{safe_title}.{fmt}"
                    filepath = os.path.join(OUTPUT_DIR, filename)

                    with open(filepath, "wb") as f:
                        f.write(data)

                    start_index += 1
                    new_saved += 1

                    meta_item = {
                        "id": f"chanh_dien_{start_index:03d}",
                        "filename": filename,
                        "category": "06_noi_dien_tam_bao",
                        "resolution": f"{w}x{h_dim}",
                        "size_kb": len(data) // 1024,
                        "source": "Bing Images (Interior Full-Res)",
                        "title": title,
                        "original_url": used_url
                    }
                    existing_meta.append(meta_item)

                    print(f"   [+ ĐÃ TẢI {new_saved:02d}] {filename} ({w}x{h_dim}, {len(data)//1024} KB)")
                    time.sleep(0.35)

                except Exception as ex:
                    continue

        except Exception as e:
            print(f"   Lỗi cào query {q}: {e}")

    # Cập nhật lại file metadata.json
    try:
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(existing_meta, f, ensure_ascii=False, indent=2)
        print(f"\n===> THÀNH CÔNG: Đã cào thêm {new_saved} hình ảnh chánh điện mới!")
        print(f"===> Đã lưu vào: {OUTPUT_DIR}")
        print(f"===> Đã cập nhật metadata: {META_PATH}")
    except Exception as e:
        print("Lỗi lưu metadata:", e)

if __name__ == "__main__":
    main()
