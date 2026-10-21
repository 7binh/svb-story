"""
Module Style Analyzer 5 trục (Style Engine 2.0.0) cho hệ sinh thái StoryFlow.
Bóc tách 5 trục văn phong:
1. Cấu trúc câu & nhịp kể (độ dài theo âm tiết/syllables)
2. Mật độ giác quan & miêu tả
3. Phân bổ hội thoại, tự sự và độc thoại nội tâm (hỗ trợ thoại đa dòng & nhiều dấu thoại)
4. Khẩu khí & tông giọng (gắn nhãn ước lượng / estimated)
5. Từ vựng & biện pháp tu từ (mở rộng nhận diện từ láy tiếng Việt)
"""

import os
import re
import json
from datetime import datetime

SCHEMA_VERSION = "2.0.0"
ANALYSIS_VERSION = "2.0.0"

# ─── Vietnamese sensory & rhetoric lexicons ───────────────────────────────────
SENSORY_LEXICON = {
    'visual': [
        'nhìn', 'thấy', 'ánh', 'màu', 'tối', 'sáng', 'bóng', 'đỏ', 'đen', 'trắng',
        'xanh', 'vàng', 'sương', 'mờ', 'lóe', 'rực', 'chiếu', 'soi', 'chớp', 'khuất',
        'rõ', 'mịt', 'mờ ảo', 'sắc', 'u tối', 'lấp lánh', 'chói', 'hư ảnh', 'le lói'
    ],
    'auditory': [
        'tiếng', 'kêu', 'rít', 'vang', 'động', 'im lặng', 'thầm', 'ầm', 'rống', 'gào',
        'lục cục', 'loảng xoảng', 'thì thầm', 'véo', 'uỳnh', 'rầm', 'cọt kẹt', 'thét',
        'văng vẳng', 'huyên náo', 'tĩnh mịch', 'thanh âm', 'gầm', 'hí', 'xào xạc'
    ],
    'tactile_visceral': [
        'lạnh', 'nóng', 'buốt', 'rát', 'đau', 'nhói', 'run', 'cứng', 'rịn', 'siết',
        'thở', 'ngực', 'tim', 'khô', 'ẩm', 'nhớp nháp', 'rùng mình', 'nổi da gà',
        'nghẹn', 'buốt giá', 'bỏng', 'tê dại', 'xước', 'thô ráp', 'mềm', 'dính'
    ],
    'olfactory_gustatory': [
        'mùi', 'tanh', 'thơm', 'nồng', 'ngai ngái', 'đắng', 'chát', 'mặn', 'ngọt',
        'chua', 'khét', 'hăng', 'cay', 'ẩm mốc', 'xạ hương', 'mùi máu', 'men rượu'
    ]
}

RHETORIC_SIMILE_MARKERS = [
    'như', 'tựa như', 'ngỡ như', 'dường như', 'tựa hồ', 'khác nào', 'tựa',
    'hệt như', 'chẳng khác gì', 'giống như', 'dường là', 'y như'
]

MONOLOGUE_MARKERS = [
    'nghĩ thầm', 'thầm nhủ', 'trong lòng', 'tự hỏi', 'ngẫm nghĩ', 'tự nhủ',
    'chợt nghĩ', 'tự đáy lòng', 'tâm niệm', 'tự trách'
]

# Danh mục tiền tố và mẫu từ láy tiếng Việt phổ biến
REDUPLICATIVE_COMMON = [
    'róc rách', 'lung linh', 'thì thào', 'chập chờn', 'mênh mông', 'xào xạc',
    'nức nở', 'thao thức', 'dồn dập', 'chầm chậm', 'loang lổ', 'ngơ ngác',
    'ngỡ ngàng', 'le lói', 'chói chang', 'bâng khuâng', 'lặng lẽ', 'thoang thoảng',
    'lập lòe', 'hun hút', 'nhè nhẹ', 'vội vã', 'ngập ngừng', 'run rẩy', 'xao xác'
]


def tokenize_sentences(text):
    """Splits text into sentences based on punctuation."""
    clean = re.sub(r'[\r\n]+', ' ', text)
    sentences = re.split(r'(?<=[.!?…])\s+', clean)
    return [s.strip() for s in sentences if len(s.strip()) > 1]


def tokenize_syllables(text):
    """
    Tách các đơn vị âm tiết (syllable units) phân tách bởi khoảng trắng.
    Lưu ý: Trong tiếng Việt, đơn vị phân tách bởi khoảng trắng là âm tiết;
    từ tiếng Việt có thể là từ đơn (1 âm tiết) hoặc từ ghép (2-3 âm tiết).
    """
    return [w for w in re.split(r'\s+', text.strip()) if w]


# Backward compatibility alias
tokenize_words = tokenize_syllables


def detect_reduplicatives(text):
    """
    Phát hiện các từ láy tiếng Việt trong văn bản qua:
    1. Tra cứu từ láy văn học tiêu biểu.
    2. Heuristic lặp phụ âm đầu hoặc lặp toàn bộ có biến âm.
    """
    lower = text.lower()
    found = set()

    # 1. Tra cứu trực tiếp từ danh sách phổ biến
    for r in REDUPLICATIVE_COMMON:
        if r in lower:
            found.add(r)

    # 2. Heuristic lặp âm tiết liên tiếp
    tokens = re.findall(r'\b[a-zA-ZÀ-ỹ]+\b', lower)
    for i in range(len(tokens) - 1):
        w1, w2 = tokens[i], tokens[i + 1]
        if len(w1) >= 2 and len(w2) >= 2:
            # Lặp toàn bộ: nhẹ nhẹ, xa xa, rung rung
            if w1 == w2 and len(w1) >= 3:
                found.add(f"{w1} {w2}")
            # Lặp phụ âm đầu (cùng 2 chữ cái đầu nếu có phụ âm ghép như ch, th, nh, ph, tr)
            elif len(w1) >= 3 and len(w2) >= 3:
                prefix = w1[:2] if w1[:2] in ['ch', 'th', 'nh', 'ph', 'tr', 'ng', 'kh', 'gh'] else w1[0]
                if w2.startswith(prefix) and w1 != w2:
                    if w1 in ['lập', 'chầm', 'lặng', 'run', 'mập', 'bập', 'chập', 'hối', 'vội', 'ngập']:
                        found.add(f"{w1} {w2}")

    return sorted(list(found))[:10]


def analyze_texts(sources, text_list, profile_id="default", scope="story"):
    """
    Phân tích văn phong toàn diện 5 trục theo Style Schema 2.0.0:
    1. Cấu trúc câu & nhịp kể (Syntax & Rhythm)
    2. Mật độ giác quan (Sensory Immersion)
    3. Tỷ lệ nội dung: Thoại vs Tự sự vs Nội tâm (Content Distribution)
    4. Khẩu khí & Tông giọng (Tone & Voice - Estimated)
    5. Từ vựng & Tu từ (Rhetoric & Lexicon)
    """
    full_text = "\n\n".join(text_list)
    paragraphs = [p.strip() for p in full_text.split('\n') if len(p.strip()) > 0]
    sentences = tokenize_sentences(full_text)
    syllables = tokenize_syllables(full_text)

    total_syllables = len(syllables)
    total_sentences = max(len(sentences), 1)
    total_paragraphs = max(len(paragraphs), 1)

    # ─── Trục 1: Cấu trúc & Nhịp câu (Syntax & Rhythm) ──────────────────────
    sentence_lengths = [len(tokenize_syllables(s)) for s in sentences]
    avg_sentence_len = round(sum(sentence_lengths) / total_sentences, 1)

    short_sentences = sum(1 for l in sentence_lengths if l < 10)
    medium_sentences = sum(1 for l in sentence_lengths if 10 <= l <= 22)
    long_sentences = sum(1 for l in sentence_lengths if l > 22)

    ratio_short = round(short_sentences / total_sentences, 2)
    ratio_medium = round(medium_sentences / total_sentences, 2)
    ratio_long = round(long_sentences / total_sentences, 2)

    punc_ellipsis = len(re.findall(r'(\.{3,}|…)', full_text))
    punc_dash = len(re.findall(r'(—|--)', full_text))
    punc_exclamation = full_text.count('!')
    punc_question = full_text.count('?')

    # ─── Trục 2: Mật độ giác quan (Sensory Immersion) ────────────────────────
    lower_text = full_text.lower()
    sensory_counts = {}
    for cat, kws in SENSORY_LEXICON.items():
        sensory_counts[cat] = sum(lower_text.count(kw) for kw in kws)

    total_sensory_hits = sum(sensory_counts.values())
    sensory_density_per_1000 = round((total_sensory_hits / max(total_syllables, 1)) * 1000, 1)

    sorted_sensory = sorted(sensory_counts.items(), key=lambda x: x[1], reverse=True)
    primary_sense = sorted_sensory[0][0] if sorted_sensory else 'visual'

    sense_vn_map = {
        'visual': 'Thị giác (Hình ảnh/Màu sắc/Ánh sáng)',
        'auditory': 'Thính giác (Âm thanh/Tiếng động/Khẽ khàng)',
        'tactile_visceral': 'Xúc giác & Cảm giác cơ thể (Nhiệt/Đau/Rùng mình)',
        'olfactory_gustatory': 'Khứu giác & Vị giác (Mùi vị/Hương thơm/Cay đắng)'
    }

    # ─── Trục 3: Tỷ lệ phân bổ nội dung (Content Distribution) ──────────────
    # Hỗ trợ thoại nhiều dòng (re.DOTALL) và nhiều định dạng ngoặc thoại: "", “”, 「」, 『』
    dialogue_quotes = re.findall(r'["“「『](.*?)["”』」]', full_text, flags=re.DOTALL)
    dialogue_dashes = re.findall(r'^[—–-]\s*(.*?)$', full_text, flags=re.MULTILINE)
    all_dialogues = dialogue_quotes + dialogue_dashes

    dialogue_syllable_count = sum(len(tokenize_syllables(d)) for d in all_dialogues)
    dialogue_ratio = round(min(dialogue_syllable_count / max(total_syllables, 1), 0.9), 2)

    # Độc thoại nội tâm
    monologue_hits = sum(lower_text.count(m) for m in MONOLOGUE_MARKERS)
    monologue_ratio = round(min((monologue_hits * 15) / max(total_syllables, 1), 0.3), 2)

    narrative_ratio = round(max(0.0, round(1.0 - dialogue_ratio - monologue_ratio, 2)), 2)

    # ─── Trục 4: Khẩu khí & Tông giọng (Tone & Voice - Estimated) ────────────
    is_fast_paced = ratio_short > 0.4
    has_high_exclamation = (punc_exclamation / total_sentences) > 0.15
    is_reflective = ratio_long > 0.25 or monologue_ratio > 0.12

    if is_fast_paced and has_high_exclamation:
        tone_descriptor = "Dồn dập, căng thẳng, giàu tính xung đột hành động"
    elif is_reflective:
        tone_descriptor = "Trầm tĩnh, chậm rãi (Slow-burn), đào sâu nội tâm và không khí"
    elif dialogue_ratio > 0.45:
        tone_descriptor = "Sống động, kịch tính hóa cao, dẫn dắt bởi đối thoại và khẩu khí"
    else:
        tone_descriptor = "Cân bằng, trần thuật khách quan ngôi thứ 3, nhịp độ vừa phải"

    # ─── Trục 5: Từ vựng & Biện pháp tu từ (Rhetoric & Lexicon) ──────────────
    simile_hits = sum(lower_text.count(f" {m} ") for m in RHETORIC_SIMILE_MARKERS)
    simile_density_per_1000 = round((simile_hits / max(total_syllables, 1)) * 1000, 1)
    reduplicatives = detect_reduplicatives(full_text)

    # ─── Confidence & Limitations ───────────────────────────────────────────
    if total_syllables >= 3000:
        conf_level = "high"
    elif total_syllables >= 500:
        conf_level = "medium"
    else:
        conf_level = "preliminary"

    fingerprint = {
        "stats": {
            "whitespace_syllables_count": total_syllables,
            "total_sentences": total_sentences,
            "total_paragraphs": total_paragraphs,
            "avg_syllables_per_sentence": avg_sentence_len,
            "sentence_length_distribution": {
                "short_under_10_syllables": ratio_short,
                "medium_10_to_22_syllables": ratio_medium,
                "long_over_22_syllables": ratio_long
            },
            "punctuation_density_per_sentence": {
                "ellipsis": round(punc_ellipsis / total_sentences, 3),
                "dash": round(punc_dash / total_sentences, 3),
                "exclamation": round(punc_exclamation / total_sentences, 3),
                "question": round(punc_question / total_sentences, 3)
            },
            "metric_note": "Độ dài câu được tính bằng số âm tiết (syllable units) phân tách bởi khoảng trắng."
        },
        "sensory_profile": {
            "primary_sense": sense_vn_map.get(primary_sense, primary_sense),
            "density_per_1000": sensory_density_per_1000,
            "distribution": {sense_vn_map.get(k, k): v for k, v in sensory_counts.items()}
        },
        "content_ratios": {
            "dialogue_ratio": dialogue_ratio,
            "narrative_action_ratio": narrative_ratio,
            "inner_monologue_ratio": monologue_ratio,
            "note": "Các tỷ lệ mang tính tham khảo tổng thể; có thể biến thiên linh hoạt theo từng cảnh cụ thể."
        },
        "tone_and_voice": {
            "descriptor": tone_descriptor,
            "tone_confidence": "estimated",
            "exclamation_density": round(punc_exclamation / total_sentences, 3),
            "ellipsis_density": round(punc_ellipsis / total_sentences, 3)
        },
        "rhetoric_and_lexicon": {
            "simile_density_per_1000": simile_density_per_1000,
            "sample_reduplicatives": reduplicatives
        }
    }

    style_rules = {
        "sentence_structure": (
            f"Duy trì câu trung bình ~{avg_sentence_len} âm tiết. "
            f"Tỷ lệ câu ngắn (~{int(ratio_short * 100)}%) dùng cho dồn nén hành động; "
            f"câu dài (~{int(ratio_long * 100)}%) dùng cho tả cảnh và lắng đọng tâm lý."
        ),
        "sensory_rule": (
            f"Trọng tâm giác quan hàng đầu là '{sense_vn_map.get(primary_sense, primary_sense)}'. "
            f"Mỗi phân cảnh cần ít nhất {max(2, int(sensory_density_per_1000 // 4))} chi tiết đặc tả giác quan cụ thể (Show, Don't Tell)."
        ),
        "content_distribution": (
            f"Cân đối tỷ lệ trung bình: Đối thoại ~{int(dialogue_ratio * 100)}%, "
            f"Tự sự/Hành động ~{int(narrative_ratio * 100)}%, "
            f"Nội tâm ~{int(monologue_ratio * 100)}%. "
            f"Lưu ý điều chỉnh theo loại cảnh (hành động vs tâm lý vs tranh biện)."
        ),
        "tone_voice": (
            f"Giữ tông giọng ước lượng: {tone_descriptor}. "
            f"Khoảng cách trần thuật phù hợp, không giải thích thay độc giả."
        ),
        "lexicon_rhetoric": (
            f"Mật độ ví von ẩn dụ khoảng {simile_density_per_1000} lần/1.000 âm tiết. "
            f"Tận dụng từ láy biểu cảm có chọn lọc, tránh lặp từ vô nghĩa."
        ),
        "anti_patterns": [
            "Tuyệt đối không dùng cụm từ dịch máy sáo rỗng ('không thể không thừa nhận', 'dường như có một tia phức tạp').",
            "Không dán nhãn cảm xúc trực tiếp ('hắn rất giận'), phải chuyển thành phản ứng cơ thể vật lý cụ thể.",
            "Không để câu văn đều đều cùng một độ dài gây buồn ngủ (phải có câu ngắn đệm câu dài)."
        ]
    }

    scene_variants = {
        "action_scene": {
            "sentence_rhythm": "Đẩy cao tỷ lệ câu ngắn (> 45%), rút ngắn thoại dưới 10 từ/lượt, nhịp dồn dập.",
            "sensory_focus": "Xúc giác & cảm giác cơ thể (nhịp tim, hơi thở, lực va chạm, đau đớn)."
        },
        "emotion_slow_burn": {
            "sentence_rhythm": "Tăng tỷ lệ câu dài (> 30%), mở rộng khoảng lặng giữa các câu thoại.",
            "sensory_focus": "Thị giác chi tiết nhỏ (ánh sáng le lói, giọt nước, nếp nhăn) và thính giác không gian."
        },
        "dialogue_heavy": {
            "sentence_rhythm": "Thoại đối đáp đa tầng có kèm beat hành động nhỏ; tránh thoại trơ trọi không phản ứng cơ thể.",
            "sensory_focus": "Khẩu khí nhân vật và vi cử chỉ (ánh mắt lướt qua, cái nhấp ngụm trà)."
        }
    }

    context_guidance = [
        f"Nhịp câu: ~{avg_sentence_len} âm tiết/câu (ngắn {int(ratio_short * 100)}% / vừa {int(ratio_medium * 100)}% / dài {int(ratio_long * 100)}%); Thoại ~{int(dialogue_ratio * 100)}%, Tự sự ~{int(narrative_ratio * 100)}%.",
        f"Giác quan: Ưu tiên '{sense_vn_map.get(primary_sense, primary_sense)}' (Show, Don't Tell; phản ứng cơ thể & chi tiết không gian).",
        f"Tông giọng: {tone_descriptor} (ước lượng); tránh tuyệt đối cụm từ sáo rỗng AI."
    ]

    confidence_and_limitations = {
        "confidence_level": conf_level,
        "sample_size_syllables": total_syllables,
        "sample_size_sentences": total_sentences,
        "limitations": (
            "Phân tích dựa trên thống kê tần suất từ vựng và biểu thức chính quy. "
            "Nhận định khẩu khí và tông giọng mang tính ước lượng (estimated). "
            "Tỷ lệ thoại/tự sự là trung bình tổng thể, tác giả có quyền điều chỉnh linh hoạt theo từng cảnh."
        )
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "analysis_version": ANALYSIS_VERSION,
        "profile_id": profile_id,
        "scope": scope,
        "updated_at": datetime.now().isoformat(),
        "sources": sources,
        "fingerprint": fingerprint,
        "style_rules": style_rules,
        "scene_variants": scene_variants,
        "context_guidance": context_guidance,
        "confidence_and_limitations": confidence_and_limitations
    }


def migrate_legacy_profile(data):
    """
    Adapter tương thích ngược: nâng cấp profile từ schema 1.0.0 hoặc legacy lên schema 2.0.0
    mà không làm mất bất kỳ dữ liệu ban đầu nào.
    """
    if data.get("schema_version") == SCHEMA_VERSION:
        return data

    migrated = dict(data)
    migrated["schema_version"] = SCHEMA_VERSION
    migrated["analysis_version"] = ANALYSIS_VERSION
    migrated["scope"] = data.get("scope", "story")

    if "scene_variants" not in migrated:
        migrated["scene_variants"] = {
            "action_scene": {"sentence_rhythm": "Đẩy cao tỷ lệ câu ngắn, dồn dập."},
            "emotion_slow_burn": {"sentence_rhythm": "Giãn nhịp câu dài, đào sâu không khí và nội tâm."}
        }

    if "confidence_and_limitations" not in migrated:
        migrated["confidence_and_limitations"] = {
            "confidence_level": "medium",
            "limitations": "Profile được nâng cấp tự động từ phiên bản cũ (legacy schema)."
        }

    return migrated


def generate_markdown_report(profile_data):
    """Sinh tài liệu STYLE_PROFILE.md chuẩn mực cho người đọc và AI tham chiếu."""
    p_id = profile_data.get("profile_id", "default")
    scope = profile_data.get("scope", "story")
    ver = profile_data.get("schema_version", "2.0.0")
    fp = profile_data.get("fingerprint", {})
    rules = profile_data.get("style_rules", {})
    stats = fp.get("stats", {})
    sensory = fp.get("sensory_profile", {})
    ratios = fp.get("content_ratios", {})
    tone = fp.get("tone_and_voice", {})
    rhetoric = fp.get("rhetoric_and_lexicon", {})
    variants = profile_data.get("scene_variants", {})
    limitations = profile_data.get("confidence_and_limitations", {})

    sources_str = ", ".join(profile_data.get("sources", ["Văn bản dán nháp"]))

    md = f"""# HỒ SƠ VĂN PHONG (STYLE PROFILE): {p_id.upper()}
> **Phiên bản Schema:** {ver}  
> **Phạm vi (Scope):** {scope.upper()}  
> **Cập nhật:** {profile_data.get('updated_at', '')[:19]}  
> **Nguồn phân tích:** {sources_str}  
> **Dung lượng mẫu:** {stats.get('whitespace_syllables_count', 0):,} âm tiết ({stats.get('total_sentences', 0):,} câu)  
> **Mức độ tin cậy:** {limitations.get('confidence_level', 'medium').upper()}  

---

## 🎯 1. CHỈ DẪN NHANH KHI VIẾT (QUICK CONTEXT GUIDANCE)
Mỗi khi sáng tác chương mới, AI và tác giả bám sát 3 chỉ dẫn cốt lõi:
1. **Nhịp câu & Cấu trúc:** {rules.get('sentence_structure')}
2. **Trọng tâm Giác quan:** {rules.get('sensory_rule')}
3. **Tông giọng & Khẩu khí:** {rules.get('tone_voice')}

---

## 🔬 2. DẤU VÂN TAY VĂN PHONG (STYLE FINGERPRINT - 5 TRỤC)

### Trục 1: Cấu Trúc & Nhịp Câu (Rhythm & Syntax)
- **Độ dài trung bình:** {stats.get('avg_syllables_per_sentence', 0)} âm tiết/câu.
- **Phân bổ độ dài câu:**
  - Câu ngắn (< 10 âm tiết - dồn nén hành động): **{int(stats.get('sentence_length_distribution', {}).get('short_under_10_syllables', 0) * 100)}%**
  - Câu vừa (10–22 âm tiết - chuẩn trần thuật): **{int(stats.get('sentence_length_distribution', {}).get('medium_10_to_22_syllables', 0) * 100)}%**
  - Câu dài (> 22 âm tiết - tả cảnh, suy tư): **{int(stats.get('sentence_length_distribution', {}).get('long_over_22_syllables', 0) * 100)}%**
- *Ghi chú:* {stats.get('metric_note', '')}

### Trục 2: Mật Độ Giác Quan (Sensory Immersion)
- **Giác quan chủ đạo:** **{sensory.get('primary_sense', 'Thị giác')}**
- **Tần suất chi tiết giác quan:** ~{sensory.get('density_per_1000', 0)} lần / 1.000 âm tiết.
- **Phân bổ chi tiết:**
"""
    for k, v in sensory.get("distribution", {}).items():
        md += f"  - {k}: {v} lần\n"

    md += f"""
### Trục 3: Tỷ Lệ Phân Bổ Nội Dung (Content Ratios)
- **Hội thoại:** {int(ratios.get('dialogue_ratio', 0) * 100)}%
- **Tự sự & Hành động:** {int(ratios.get('narrative_action_ratio', 0) * 100)}%
- **Độc thoại nội tâm:** {int(ratios.get('inner_monologue_ratio', 0) * 100)}%
- *Ghi chú:* {ratios.get('note', '')}

### Trục 4: Khẩu Khí & Tông Giọng (Tone & Voice - Estimated)
- **Sắc thái chủ đạo:** {tone.get('descriptor', 'Trần thuật khách quan')} *(Ước lượng heuristic)*
- **Mật độ cảm thán (!):** {tone.get('exclamation_density', 0)} / câu
- **Mật độ chấm lửng (...):** {tone.get('ellipsis_density', 0)} / câu

### Trục 5: Từ Vựng & Tu Từ (Rhetoric & Lexicon)
- **Mật độ so sánh (như, tựa như):** ~{rhetoric.get('simile_density_per_1000', 0)} lần / 1.000 âm tiết.
- **Từ láy biểu cảm phát hiện được:** {", ".join(rhetoric.get('sample_reduplicatives', [])) or "Không đáng kể"}

---

## 🎭 3. ĐẶC ĐIỂM LINH HOẠT THEO TỪNG LOẠI CẢNH (SCENE VARIANTS)
Không áp đặt một công thức cố định cho toàn truyện. Hãy điều chỉnh linh hoạt theo ngữ cảnh:
- **Cảnh Hành Động / Giao Tranh:** {variants.get('action_scene', {}).get('sentence_rhythm', 'Tăng nhịp câu ngắn, dồn dập.')}
- **Cảnh Tâm Lý / Lắng Đọng:** {variants.get('emotion_slow_burn', {}).get('sentence_rhythm', 'Tăng nhịp câu dài, mở rộng không gian.')}
- **Cảnh Đối Thoại / Tranh Biện:** {variants.get('dialogue_heavy', {}).get('sentence_rhythm', 'Thoại sắc bén kèm beat hành động nhỏ.')}

---

## ⚡ 4. BỘ QUY TẮC SÁNG TÁC THỰC THI (STYLE RULES PIPELINE)

### Điều Cần Duy Trì:
- {rules.get('sentence_structure')}
- {rules.get('sensory_rule')}
- {rules.get('content_distribution')}
- {rules.get('lexicon_rhetoric')}

### Lỗi Cấm Kỵ (Anti-Patterns):
"""
    for ap in rules.get("anti_patterns", []):
        md += f"- ❌ {ap}\n"

    md += f"""
---

## ⚠️ 5. ĐỘ TIN CẬY & GIỚI HẠN (CONFIDENCE & LIMITATIONS)
- **Độ tin cậy:** {limitations.get('confidence_level', 'medium').upper()} (Dựa trên mẫu {stats.get('whitespace_syllables_count', 0):,} âm tiết).
- **Giới hạn kỹ thuật:** {limitations.get('limitations', '')}
- **Bảo toàn dữ liệu nguồn:** Profile này chỉ trích xuất các quy tắc ngữ văn và kỹ thuật kể chuyện khái quát; tuyệt đối không sao chép nguyên văn tình tiết từ tác phẩm mẫu.
"""
    return md
