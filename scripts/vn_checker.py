"""
Module kiểm tra và chuẩn hóa chất lượng văn phong tiếng Việt (Vietnamese Anti-Slop & Punctuation Quality Gate).
Thuần Python, không phụ thuộc thư viện ngoài, tối ưu token và kiểm tra an toàn không phá vỡ ngữ nghĩa.
Tích hợp trực tiếp cơ chế .deslop-whitelist cục bộ (native Python).
"""

import os
import re
import sys
import unicodedata

# ─── CÁC CỤM TỪ VĂN MẪU AI CẤM KỴ (ANTI-SLOP BLACKLIST TỪ REFERENCES/ANTI-SLOP.MD) ─
VIETNAMESE_SLOP_PATTERNS = [
    {
        "pattern": r"không thể không thừa nhận(?:\s+rằng)?",
        "description": "Cụm từ thừa thãi, dịch thô từ tiếng Trung/Anh",
        "suggestion": "Bỏ hẳn cụm từ này, đi thẳng vào nhận định hoặc cảm xúc nhân vật"
    },
    {
        "pattern": r"không thể phủ nhận rằng",
        "description": "Văn thuyết minh giả tạo trong tiểu thuyết",
        "suggestion": "Chuyển thành suy nghĩ nội tâm tự nhiên hoặc hành động cụ thể"
    },
    {
        "pattern": r"(?:bầu\s+)?không khí\s+(?:bỗng\s+|như\s+)?ngưng đọng(?:\s+lại)?",
        "description": "Sáo rỗng (cliché) miêu tả không khí căng thẳng",
        "suggestion": "Tả chi tiết giác quan: tiếng thở dài, tiếng gió rít, cái liếc mắt"
    },
    {
        "pattern": r"(?:dường như\s+|trong mắt\s+)?(?:lóe|loé|xuất hiện)\s+lên\s+một\s+tia\s+phức tạp",
        "description": "Sáo rỗng miêu tả biểu cảm mơ hồ",
        "suggestion": "Tả ánh nhìn vật lý cụ thể: đồng tử co lại, hàng mày nhíu chặt"
    },
    {
        "pattern": r"con đường phía trước còn rất dài",
        "description": "Đúc kết triết lý vụng về ở cuối chương",
        "suggestion": "Kết thúc bằng một câu hỏi mở, bước chân trong đêm hoặc một hành động cụ thể"
    },
    {
        "pattern": r"như thể thời gian đã ngừng trôi",
        "description": "Văn mẫu sáo rỗng miêu tả khoảnh khắc ngưng trệ",
        "suggestion": "Tả chi tiết giác quan chậm lại: tiếng giọt nước rơi, tiếng kim đồng hồ"
    },
    {
        "pattern": r"trong lòng không khỏi\s+(?:dâng lên|cảm thấy)",
        "description": "Dán nhãn cảm xúc gián tiếp mang phong cách dịch máy",
        "suggestion": "Tả phản ứng cơ thể: nghẹn ở cổ họng, lồng ngực đập thình thịch"
    }
]


def load_whitelist(target_file_or_dir):
    """
    Tải danh sách ngoại lệ (.deslop-whitelist) cục bộ từ thư mục chứa file
    hoặc các thư mục cha (ví dụ thư mục truyện).
    """
    if not target_file_or_dir:
        return []

    path_obj = os.path.abspath(target_file_or_dir)
    dir_path = path_obj if os.path.isdir(path_obj) else os.path.dirname(path_obj)

    # Tìm .deslop-whitelist tại dir_path hoặc các cấp cha (tối đa 3 cấp)
    curr = dir_path
    for _ in range(3):
        wl_path = os.path.join(curr, ".deslop-whitelist")
        if os.path.exists(wl_path):
            try:
                with open(wl_path, "r", encoding="utf-8", errors="replace") as f:
                    lines = [line.strip() for line in f.readlines()]
                entries = [l for l in lines if l and not l.startswith("#")]
                return sorted(entries, key=lambda x: len(x), reverse=True)
            except Exception:
                pass
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent

    return []


def mask_whitelist_spans(text, whitelist):
    """
    Ẩn các đoạn văn bản nằm trong danh sách whitelist để tránh regex bắt nhầm.
    Thay thế bằng ký tự khoảng trắng có cùng độ dài để giữ nguyên vị trí index.
    """
    if not whitelist:
        return text

    masked = list(text)
    lower_text = text.lower()

    for item in whitelist:
        target = item.lower()
        idx = lower_text.find(target)
        while idx != -1:
            for i in range(idx, idx + len(target)):
                masked[i] = " "
            idx = lower_text.find(target, idx + len(target))

    return "".join(masked)


def check_punctuation(text):
    """
    Kiểm tra các lỗi dấu câu tiếng Việt phổ biến:
    - Khoảng trắng trước dấu phẩy/chấm/chấm phẩy/chấm than/hỏi chấm.
    - Thiếu khoảng trắng sau dấu câu khi nối từ.
    - Cặp dấu ngoặc kép không cân xứng (lẻ).
    - Chuỗi chấm bất thường (2 chấm hoặc 4+ chấm).
    """
    issues = []

    # 1. Khoảng trắng trước dấu câu
    space_before_punc = re.findall(r'\s+([,.;!?])', text)
    if space_before_punc:
        issues.append({
            "type": "space_before_punctuation",
            "severity": "warning",
            "message": f"Phát hiện {len(space_before_punc)} vị trí có khoảng trắng thừa trước dấu câu ({set(space_before_punc)})."
        })

    # 2. Thiếu khoảng trắng sau dấu câu giữa các chữ cái
    missing_space_after = re.findall(r'([,;!?])[a-zA-ZÀ-ỹ0-9]', text)
    if missing_space_after:
        issues.append({
            "type": "missing_space_after_punctuation",
            "severity": "warning",
            "message": f"Phát hiện {len(missing_space_after)} vị trí thiếu khoảng trắng sau dấu câu."
        })

    # 3. Kiểm tra ngoặc kép
    straight_quotes = text.count('"')
    if straight_quotes % 2 != 0:
        issues.append({
            "type": "unbalanced_quotes",
            "severity": "warning",
            "message": f"Số lượng dấu ngoặc kép thẳng (\") bị lẻ ({straight_quotes} dấu), có thể chưa đóng ngoặc thoại."
        })

    # 4. Dấu chấm lửng bất thường (.. hoặc ....)
    odd_dots = re.findall(r'(?<!\.)\.\.(?!\.)|(?<!\.)\.{4,}(?!\.)', text)
    if odd_dots:
        issues.append({
            "type": "irregular_ellipsis",
            "severity": "info",
            "message": f"Phát hiện {len(odd_dots)} dấu chấm lửng bất thường (nên dùng 3 chấm '...' hoặc '…')."
        })

    return issues


def check_ai_slop(text, whitelist=None):
    """
    Quét các cụm từ sáo rỗng AI theo danh mục anti-slop.
    Áp dụng whitelist nếu được cung cấp để bỏ qua các ngoại lệ chủ ý của tác giả.
    """
    findings = []
    scannable_text = mask_whitelist_spans(text, whitelist) if whitelist else text
    lower_text = scannable_text.lower()

    for item in VIETNAMESE_SLOP_PATTERNS:
        matches = list(re.finditer(item["pattern"], lower_text))
        if matches:
            for m in matches:
                start = max(0, m.start() - 30)
                end = min(len(text), m.end() + 30)
                snippet = text[start:end].replace('\n', ' ')
                findings.append({
                    "matched_text": text[m.start():m.end()],
                    "snippet": f"...{snippet}...",
                    "description": item["description"],
                    "suggestion": item["suggestion"]
                })
    return findings


def normalize_punctuation_safe(text):
    """
    Chuẩn hóa dấu câu một cách an toàn mà KHÔNG thay đổi từ ngữ hay cấu trúc:
    - Xóa khoảng trắng trước [, . ; : ! ?]
    - Đảm bảo 1 khoảng trắng sau [, ; :] nếu ngay sau là chữ cái
    - Chuẩn hóa 2 chấm thành 3 chấm (...)
    """
    # 1. Bỏ khoảng trắng trước dấu câu
    text = re.sub(r'[ \t]+([,.;:!?])', r'\1', text)
    # 2. Thêm khoảng trắng sau dấu phẩy nếu ngay sau là chữ cái
    text = re.sub(r'([,;:!?])([a-zA-ZÀ-ỹ])', r'\1 \2', text)
    # 3. Chuẩn hóa 2 dấu chấm đứng độc lập thành 3 dấu chấm
    text = re.sub(r'(?<!\.)\.\.(?!\.)', '...', text)
    return text


def inspect_text(text, target_path=None, whitelist=None):
    """
    Hàm tổng hợp kiểm tra toàn diện một văn bản nháp tiếng Việt.
    Hỗ trợ tự động nạp .deslop-whitelist nếu target_path được cung cấp.
    """
    clean_text = text.lstrip('\ufeff')
    wl = whitelist if whitelist is not None else load_whitelist(target_path)
    punc_issues = check_punctuation(clean_text)
    slop_findings = check_ai_slop(clean_text, whitelist=wl)

    # Đếm số lượng từ/âm tiết
    words = [w for w in re.split(r'\s+', clean_text.strip()) if w]
    word_count = len(words)

    has_blocking = len(slop_findings) > 0
    return {
        "word_count": word_count,
        "punctuation_issues": punc_issues,
        "slop_findings": slop_findings,
        "whitelist_count": len(wl),
        "passed": not has_blocking,
        "has_warnings": len(punc_issues) > 0 or has_blocking
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vn_checker.py <filepath> [--normalize]")
        sys.exit(0)

    target_file = sys.argv[1]
    do_normalize = "--normalize" in sys.argv

    if not os.path.exists(target_file):
        print(f"[ERROR] Không tìm thấy file: {target_file}")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if do_normalize:
        norm = normalize_punctuation_safe(content)
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(norm)
        print(f"✓ Đã chuẩn hóa dấu câu an toàn cho file: {target_file}")
    else:
        res = inspect_text(content, target_path=target_file)
        print(f"=== KẾT QUẢ KIỂM TRA: {os.path.basename(target_file)} ({res['word_count']} chữ) ===")
        if res['whitelist_count']:
            print(f"  (Đã áp dụng {res['whitelist_count']} quy tắc ngoại lệ từ .deslop-whitelist)")
        if res['slop_findings']:
            print(f"  ❌ Phát hiện {len(res['slop_findings'])} cụm từ văn mẫu AI cấm kỵ:")
            for s in res['slop_findings']:
                print(f"     - '{s['matched_text']}': {s['description']}")
                print(f"       Gợi ý: {s['suggestion']}")
        else:
            print("  ✓ Không phát hiện cụm từ văn mẫu AI nghiêm trọng.")

        if res['punctuation_issues']:
            print("  ⚠ Cảnh báo dấu câu:")
            for p in res['punctuation_issues']:
                print(f"     - {p['message']}")
        sys.exit(0 if res['passed'] else 1)
