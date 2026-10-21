import os
import re
import json
from datetime import datetime

# ─── Vietnamese sensory & rhetoric lexicons ───────────────────────────────────
SENSORY_LEXICON = {
    'visual': [
        'nhìn', 'thấy', 'ánh', 'màu', 'tối', 'sáng', 'bóng', 'đỏ', 'đen', 'trắng',
        'xanh', 'vàng', 'sương', 'mờ', 'lóe', 'rực', 'chiếu', 'soi', 'chớp', 'khuất',
        'rõ', 'mịt', 'mờ ảo', 'sắc', 'u tối', 'lấp lánh', 'chói', 'hư ảnh'
    ],
    'auditory': [
        'tiếng', 'kêu', 'rít', 'vang', 'động', 'im lặng', 'thầm', 'ầm', 'rống', 'gào',
        'lục cục', 'loảng xoảng', 'thì thầm', 'véo', 'uỳnh', 'rầm', 'cọt kẹt', 'thét',
        'văng vẳng', 'huyên náo', 'tĩnh mịch', 'thanh âm', 'gầm', 'hí'
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
    'hệt như', 'chẳng khác gì', 'giống như', 'dường là'
]

MONOLOGUE_MARKERS = [
    'nghĩ thầm', 'thầm nhủ', 'trong lòng', 'tự hỏi', 'ngẫm nghĩ', 'tự nhủ',
    'chợt nghĩ', 'tự đáy lòng', 'tâm niệm'
]


def tokenize_sentences(text):
    """Splits text into sentences based on punctuation."""
    # Normalize clean breaks
    clean = re.sub(r'[\r\n]+', ' ', text)
    sentences = re.split(r'(?<=[.!?…])\s+', clean)
    return [s.strip() for s in sentences if len(s.strip()) > 1]


def tokenize_words(text):
    """Simple tokenization based on whitespace."""
    return [w for w in re.split(r'\s+', text.strip()) if w]


def analyze_texts(sources, text_list, profile_id="default"):
    """
    Performs comprehensive 5-axis style decomposition:
    1. Sentence structure & rhythm
    2. Sensory density & description
    3. Content distribution (Dialogue vs Action/Narrative vs Monologue)
    4. Tone & voice characteristics
    5. Vocabulary patterns & rhetoric
    """
    full_text = "\n\n".join(text_list)
    paragraphs = [p.strip() for p in full_text.split('\n') if len(p.strip()) > 0]
    sentences = tokenize_sentences(full_text)
    words = tokenize_words(full_text)

    total_words = len(words)
    total_sentences = max(len(sentences), 1)
    total_paragraphs = max(len(paragraphs), 1)

    # ─── Axis 1: Sentence structure & rhythm ─────────────────────────────────
    sentence_lengths = [len(tokenize_words(s)) for s in sentences]
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

    # ─── Axis 2: Sensory density ─────────────────────────────────────────────
    lower_text = full_text.lower()
    sensory_counts = {}
    for cat, kws in SENSORY_LEXICON.items():
        sensory_counts[cat] = sum(lower_text.count(kw) for kw in kws)

    total_sensory_hits = sum(sensory_counts.values())
    sensory_density_per_1000 = round((total_sensory_hits / max(total_words, 1)) * 1000, 1)

    sorted_sensory = sorted(sensory_counts.items(), key=lambda x: x[1], reverse=True)
    primary_sense = sorted_sensory[0][0] if sorted_sensory else 'visual'

    sense_vn_map = {
        'visual': 'Thị giác (Hình ảnh/Màu sắc)',
        'auditory': 'Thính giác (Âm thanh/Tiếng động)',
        'tactile_visceral': 'Xúc giác & Cảm giác cơ thể (Nhiệt/Đau/Rùng mình)',
        'olfactory_gustatory': 'Khứu giác & Vị giác (Mùi vị/Hương thơm)'
    }

    # ─── Axis 3: Content distribution (Dialogue vs Action vs Monologue) ─────
    # Dialogue: text inside quotes or leading dash
    dialogue_matches = re.findall(r'["“「](.*?)["”」]', full_text)
    # Also dash dialogue
    dash_dialogues = re.findall(r'^[—–-]\s*(.*?)$', full_text, flags=re.MULTILINE)
    all_dialogues = dialogue_matches + dash_dialogues

    dialogue_word_count = sum(len(tokenize_words(d)) for d in all_dialogues)
    dialogue_ratio = round(min(dialogue_word_count / max(total_words, 1), 0.9), 2)

    # Monologue estimate via markers
    monologue_hits = sum(lower_text.count(m) for m in MONOLOGUE_MARKERS)
    monologue_ratio = round(min((monologue_hits * 15) / max(total_words, 1), 0.3), 2)

    narrative_ratio = round(max(0.0, 1.0 - dialogue_ratio - monologue_ratio), 2)

    # ─── Axis 4: Tone & Voice ────────────────────────────────────────────────
    # Tone classification based on markers and pacing
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

    # ─── Axis 5: Vocabulary & Rhetoric ───────────────────────────────────────
    # Simile density
    simile_hits = sum(lower_text.count(f" {m} ") for m in RHETORIC_SIMILE_MARKERS)
    simile_density_per_1000 = round((simile_hits / max(total_words, 1)) * 1000, 1)

    # Detect Vietnamese reduplicatives (từ láy / lặp phụ âm đầu)
    word_tokens_lower = [w.lower() for w in re.findall(r'\b[a-zA-ZÀ-ỹ]+\b', lower_text)]
    reduplicatives = []
    for i in range(len(word_tokens_lower) - 1):
        w1, w2 = word_tokens_lower[i], word_tokens_lower[i+1]
        if len(w1) > 2 and len(w2) > 2 and w1 != w2:
            if w1[0] == w2[0] and (w1 in ['róc', 'lung', 'thì', 'thoang', 'lập', 'chầm', 'lặng', 'run', 'hun', 'vồn']):
                reduplicatives.append(f"{w1} {w2}")
    unique_reduplicatives = list(set(reduplicatives))[:6]

    # ─── Generate Style Fingerprint & Style Rules ─────────────────────────────
    fingerprint = {
        "stats": {
            "total_words_analyzed": total_words,
            "total_sentences": total_sentences,
            "total_paragraphs": total_paragraphs,
            "avg_words_per_sentence": avg_sentence_len,
            "sentence_length_distribution": {
                "short_under_10_words": ratio_short,
                "medium_10_to_22_words": ratio_medium,
                "long_over_22_words": ratio_long
            }
        },
        "sensory_profile": {
            "density_per_1000_words": sensory_density_per_1000,
            "primary_sense": sense_vn_map.get(primary_sense, primary_sense),
            "distribution": {sense_vn_map.get(k, k): v for k, v in sensory_counts.items()}
        },
        "content_ratios": {
            "dialogue_ratio": dialogue_ratio,
            "narrative_action_ratio": narrative_ratio,
            "inner_monologue_ratio": monologue_ratio
        },
        "tone_and_voice": {
            "descriptor": tone_descriptor,
            "exclamation_density": round(punc_exclamation / total_sentences, 3),
            "ellipsis_density": round(punc_ellipsis / total_sentences, 3)
        },
        "rhetoric_and_lexicon": {
            "simile_density_per_1000": simile_density_per_1000,
            "sample_reduplicatives": unique_reduplicatives
        }
    }

    # Generate actionable Style Rules
    style_rules = {
        "sentence_structure": (
            f"Duy trì câu trung bình ~{avg_sentence_len} từ. "
            f"Tỷ lệ câu ngắn (~{int(ratio_short*100)}%) dùng cho dồn nén hành động; "
            f"câu dài (~{int(ratio_long*100)}%) dùng cho tả cảnh và lắng đọng tâm lý."
        ),
        "sensory_rule": (
            f"Trọng tâm giác quan hàng đầu là '{sense_vn_map.get(primary_sense, primary_sense)}'. "
            f"Mỗi phân cảnh cần ít nhất {max(2, int(sensory_density_per_1000 // 4))} chi tiết đặc tả giác quan cụ thể (Show, Don't Tell)."
        ),
        "content_distribution": (
            f"Cân đối tỷ lệ: Đối thoại ~{int(dialogue_ratio*100)}%, "
            f"Tự sự/Hành động ~{int(narrative_ratio*100)}%, "
            f"Nội tâm ~{int(monologue_ratio*100)}%. "
            f"Không để hội thoại lấn át diễn biến hành động trừ cảnh tranh biện."
        ),
        "tone_voice": (
            f"Giữ tông giọng: {tone_descriptor}. "
            f"Khoảng cách trần thuật phù hợp, không giải thích thay độc giả."
        ),
        "lexicon_rhetoric": (
            f"Mật độ ví von ẩn dụ khoảng {simile_density_per_1000} lần/1000 từ. "
            f"Tận dụng từ láy biểu cảm có chọn lọc, tránh lặp từ vô nghĩa."
        ),
        "anti_patterns": [
            "Tuyệt đối không dùng cụm từ dịch máy sáo rỗng ('không thể không thừa nhận', 'dường như có một tia').",
            "Không dán nhãn cảm xúc trực tiếp ('hắn rất giận'), phải chuyển thành phản ứng cơ thể.",
            "Không để câu văn đều đều cùng một độ dài gây buồn ngủ (phải có câu ngắn đệm câu dài)."
        ]
    }

    # Generate 3-line quick context guidance
    context_guidance = [
        f"Nhịp câu: ~{avg_sentence_len} từ/câu (ngắn {int(ratio_short*100)}% / vừa {int(ratio_medium*100)}% / dài {int(ratio_long*100)}%); Thoại ~{int(dialogue_ratio*100)}%, Tự sự ~{int(narrative_ratio*100)}%.",
        f"Giác quan: Ưu tiên '{sense_vn_map.get(primary_sense, primary_sense)}' (Show, Don't Tell; tả cảm giác cơ thể & chi tiết không gian).",
        f"Tông giọng & Khẩu khí: {tone_descriptor}; tuyệt đối tránh văn mẫu dịch máy."
    ]

    return {
        "profile_id": profile_id,
        "version": "1.0.0",
        "updated_at": datetime.now().isoformat(),
        "sources": sources,
        "fingerprint": fingerprint,
        "style_rules": style_rules,
        "context_guidance": context_guidance
    }


def generate_markdown_report(profile_data):
    """Generates a structured human-readable STYLE_PROFILE.md."""
    p_id = profile_data.get("profile_id", "default")
    fp = profile_data.get("fingerprint", {})
    rules = profile_data.get("style_rules", {})
    stats = fp.get("stats", {})
    sensory = fp.get("sensory_profile", {})
    ratios = fp.get("content_ratios", {})
    tone = fp.get("tone_and_voice", {})
    rhetoric = fp.get("rhetoric_and_lexicon", {})

    sources_str = ", ".join(profile_data.get("sources", ["Văn bản dán nháp"]))

    md = f"""# HỒ SƠ VĂN PHONG (STYLE PROFILE): {p_id.upper()}
> **Phiên bản:** {profile_data.get('version', '1.0.0')}  
> **Cập nhật:** {profile_data.get('updated_at', '')[:19]}  
> **Nguồn phân tích:** {sources_str}  
> **Tổng dung lượng mẫu:** {stats.get('total_words_analyzed', 0):,} từ ({stats.get('total_sentences', 0):,} câu)

---

## 🎯 1. CHỈ DẪN NHANH KHI VIẾT (QUICK GUIDANCE)
Mỗi khi sáng tác chương mới, AI bắt buộc phải bám sát 3 chỉ dẫn cốt lõi:
1. **Nhịp câu & Cấu trúc:** {rules.get('sentence_structure')}
2. **Trọng tâm Giác quan:** {rules.get('sensory_rule')}
3. **Tông giọng & Khẩu khí:** {rules.get('tone_voice')}

---

## 🔬 2. DẤU VÂN TAY VĂN PHONG (STYLE FINGERPRINT - 5 TRỤC)

### Trục 1: Cấu Trúc & Nhịp Câu (Rhythm & Syntax)
- **Độ dài trung bình:** {stats.get('avg_words_per_sentence', 0)} từ/câu.
- **Phân bổ độ dài câu:**
  - Câu ngắn (< 10 từ - dồn nén hành động): **{int(stats.get('sentence_length_distribution', {}).get('short_under_10_words', 0) * 100)}%**
  - Câu vừa (10–22 từ - chuẩn trần thuật): **{int(stats.get('sentence_length_distribution', {}).get('medium_10_to_22_words', 0) * 100)}%**
  - Câu dài (> 22 từ - tả cảnh, suy tư): **{int(stats.get('sentence_length_distribution', {}).get('long_over_22_words', 0) * 100)}%**

### Trục 2: Mật Độ Giác Quan (Sensory Immersion)
- **Giác quan chủ đạo:** **{sensory.get('primary_sense', 'Thị giác')}**
- **Tần suất chi tiết giác quan:** ~{sensory.get('density_per_1000_words', 0)} lần / 1.000 từ.
- **Phân bổ chi tiết:**
"""
    for k, v in sensory.get("distribution", {}).items():
        md += f"  - {k}: {v} lần\n"

    md += f"""
### Trục 3: Tỷ Lệ Phân Bổ Nội Dung (Content Ratios)
- **Hội thoại:** {int(ratios.get('dialogue_ratio', 0) * 100)}%
- **Tự sự & Hành động:** {int(ratios.get('narrative_action_ratio', 0) * 100)}%
- **Độc thoại nội tâm:** {int(ratios.get('inner_monologue_ratio', 0) * 100)}%

### Trục 4: Khẩu Khí & Tông Giọng (Tone & Voice)
- **Sắc thái:** {tone.get('descriptor', 'Trần thuật khách quan')}
- **Mật độ chấm lửng (...):** {tone.get('ellipsis_density', 0)} / câu
- **Mật độ cảm thán (!):** {tone.get('exclamation_density', 0)} / câu

### Trục 5: Từ Vựng & Tu Từ (Rhetoric & Lexicon)
- **Mật độ ví von/ẩn dụ:** ~{rhetoric.get('simile_density_per_1000', 0)} lần / 1.000 từ.
- **Từ láy tiêu biểu nhận diện được:** {", ".join(rhetoric.get('sample_reduplicatives', [])) or "Không đáng kể"}

---

## ⚡ 3. BỘ QUY TẮC SÁNG TÁC THỰC THI (STYLE RULES PIPELINE)

### Điều Cần Duy Trì:
- {rules.get('sentence_structure')}
- {rules.get('sensory_rule')}
- {rules.get('content_distribution')}
- {rules.get('lexicon_rhetoric')}

### Lỗi Cấm Kỵ (Anti-Patterns):
"""
    for ap in rules.get("anti_patterns", []):
        md += f"- ❌ {ap}\n"

    md += """
---
*Hồ sơ này là tài liệu chuẩn được nạp tự động qua lệnh `python manage_story.py context` và kiểm tra bởi `python manage_story.py check`.*
"""
    return md
