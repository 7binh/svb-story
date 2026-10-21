import os
import json
import argparse
import sys
import io
import shutil
import re
import unicodedata
from datetime import datetime

# Reconfigure stdout/stderr to use UTF-8 on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except AttributeError:
        pass

# ─── Path constants ───────────────────────────────────────────────────────────
ACTIVE_STORY_JSON    = 'active_story.json'
STORIES_DIR          = 'stories'

CONFIG_PATH          = 'story_config.json'
STORY_JSON_PATH      = 'story.json'
CHAPTERS_DIR         = 'chapters'
SUMMARIES_DIR        = 'summaries'
ROLLING_SUMMARY_TXT  = 'rolling_summary.txt'
CHARACTER_BIBLE_JSON = 'character_bible.json'
LOREBOOK_JSON         = 'lorebook.json'
OUTLINE_MD           = 'outline.md'
FORESHADOW_JSON      = 'foreshadow.json'
STYLE_PROFILES_DIR   = 'style_profiles'
ACTIVE_STYLE_PROFILE_JSON = 'active_style_profile.json'


# ─── Helpers ──────────────────────────────────────────────────────────────────
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_current_time():
    return datetime.now().isoformat()

def slugify(text):
    d_map = {'đ': 'd', 'Đ': 'd'}
    text = ''.join(d_map.get(c, c) for c in text)
    text = text.lower()
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9\s_-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def get_active_story():
    if not os.path.exists(ACTIVE_STORY_JSON):
        return None
    try:
        with open(ACTIVE_STORY_JSON, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('active_story')
    except Exception:
        return None

def get_story_dir(story_id):
    return os.path.join(STORIES_DIR, story_id)

def get_paths():
    story_id = get_active_story()
    if not story_id:
        return None
    sdir = get_story_dir(story_id)
    return {
        'story_dir':       sdir,
        'config':          os.path.join(sdir, CONFIG_PATH),
        'story_json':      os.path.join(sdir, STORY_JSON_PATH),
        'draft':           os.path.join(sdir, CHAPTERS_DIR, 'draft.md'),
        'chapters_dir':    os.path.join(sdir, CHAPTERS_DIR),
        'summaries_dir':   os.path.join(sdir, SUMMARIES_DIR),
        'rolling_summary': os.path.join(sdir, SUMMARIES_DIR, ROLLING_SUMMARY_TXT),
        'character_bible': os.path.join(sdir, SUMMARIES_DIR, CHARACTER_BIBLE_JSON),
        'lorebook':        os.path.join(sdir, SUMMARIES_DIR, LOREBOOK_JSON),
        'outline':         os.path.join(sdir, SUMMARIES_DIR, OUTLINE_MD),
        'foreshadow':      os.path.join(sdir, SUMMARIES_DIR, FORESHADOW_JSON),
        'style_profiles_dir':    os.path.join(sdir, SUMMARIES_DIR, STYLE_PROFILES_DIR),
        'active_style_profile':  os.path.join(sdir, SUMMARIES_DIR, ACTIVE_STYLE_PROFILE_JSON),
    }

def load_config(paths):
    with open(paths['config'], 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(paths, config):
    with open(paths['config'], 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def load_story(paths):
    if not os.path.exists(paths['story_json']):
        return {'metadata': {}, 'chapters': []}
    try:
        with open(paths['story_json'], 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {'metadata': {}, 'chapters': []}

def save_story(paths, story):
    with open(paths['story_json'], 'w', encoding='utf-8') as f:
        json.dump(story, f, ensure_ascii=False, indent=2)

def chapter_filepath(paths, n):
    return os.path.join(paths['chapters_dir'], f'chapter_{n:04d}.md')

def chapter_exists(paths, n):
    return os.path.exists(chapter_filepath(paths, n))


# ─── STYLE PROFILE HELPERS (MULTI-PROFILE) ───────────────────────────────────

def get_active_profile_id(paths):
    if not os.path.exists(paths['active_style_profile']):
        return 'default'
    try:
        with open(paths['active_style_profile'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('active_profile', 'default')
    except Exception:
        return 'default'


def get_active_style_profile_info(paths):
    active_id = get_active_profile_id(paths)
    prof_dir = os.path.join(paths['style_profiles_dir'], active_id)
    json_path = os.path.join(prof_dir, 'style_profile.json')
    md_path = os.path.join(prof_dir, 'STYLE_PROFILE.md')

    if not os.path.exists(json_path):
        # Backward compatibility with legacy summaries/style_profile.json
        legacy_json = os.path.join(paths['summaries_dir'], 'style_profile.json')
        if os.path.exists(legacy_json):
            try:
                with open(legacy_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return {
                    'profile_id': 'legacy',
                    'version': data.get('version', '1.0.0'),
                    'json_path': legacy_json,
                    'md_path': os.path.join(paths['summaries_dir'], 'STYLE_PROFILE.md'),
                    'data': data,
                    'context_guidance': data.get('context_guidance', [])
                }
            except Exception:
                pass
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return {
            'profile_id': active_id,
            'version': data.get('version', '1.0.0'),
            'json_path': json_path,
            'md_path': md_path,
            'data': data,
            'context_guidance': data.get('context_guidance', [])
        }
    except Exception:
        return None


def set_active_style_profile(paths, profile_id):
    prof_dir = os.path.join(paths['style_profiles_dir'], profile_id)
    if not os.path.exists(prof_dir):
        return False, f"Profile '{profile_id}' không tồn tại trong {paths['style_profiles_dir']}."
    ensure_dir(paths['summaries_dir'])
    with open(paths['active_style_profile'], 'w', encoding='utf-8') as f:
        json.dump({'active_profile': profile_id, 'updated_at': get_current_time()}, f, ensure_ascii=False, indent=2)
    return True, f"Đã chuyển sang profile văn phong: '{profile_id}'"


def save_style_profile_data(paths, profile_id, profile_data, md_report):
    prof_dir = os.path.join(paths['style_profiles_dir'], profile_id)
    ensure_dir(prof_dir)
    json_path = os.path.join(prof_dir, 'style_profile.json')
    md_path = os.path.join(prof_dir, 'STYLE_PROFILE.md')

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_report)

    # Set as active
    ensure_dir(paths['summaries_dir'])
    with open(paths['active_style_profile'], 'w', encoding='utf-8') as f:
        json.dump({'active_profile': profile_id, 'updated_at': get_current_time()}, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Đã lưu Style Profile: '{profile_id}' (v{profile_data.get('version', '1.0.0')})")
    print(f"  JSON data : {json_path}")
    print(f"  Markdown  : {md_path}")
    print(f"  Đã đặt làm profile hoạt động (active).\n")


# ─── CORE DATABASE SAVE FUNCTIONS ─────────────────────────────────────────────

def save_character_data(paths, name, chapter, status):
    ensure_dir(paths['summaries_dir'])
    bible = {}
    if os.path.exists(paths['character_bible']):
        try:
            with open(paths['character_bible'], 'r', encoding='utf-8') as f:
                bible = json.load(f)
        except json.JSONDecodeError:
            pass

    entry = bible.get(name, {'current_status': '', 'history': []})
    entry['current_status'] = status.strip()
    entry['history'].append({
        'chapter':    chapter,
        'status':     status.strip(),
        'updated_at': get_current_time()
    })
    bible[name] = entry

    with open(paths['character_bible'], 'w', encoding='utf-8') as f:
        json.dump(bible, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Cập nhật nhân vật \"{name}\" tại chương {chapter}.")
    print(f"  Lịch sử: {len(entry['history'])} lần cập nhật.")


def save_summary_data(paths, from_ch, to_ch, text):
    ensure_dir(paths['summaries_dir'])
    date_str = datetime.now().strftime('%Y-%m-%d')
    block = (
        f"[CHƯƠNG {from_ch}–{to_ch} | {date_str}]\n"
        f"{text.strip()}\n"
        f"{'─' * 60}\n\n"
    )
    with open(paths['rolling_summary'], 'a', encoding='utf-8') as f:
        f.write(block)

    print(f"[SUCCESS] Đã nối tóm tắt chương {from_ch}–{to_ch} vào {paths['rolling_summary']}.")


def save_lore_data(paths, entry_name, chapter, content):
    ensure_dir(paths['summaries_dir'])
    lore = {}
    if os.path.exists(paths['lorebook']):
        try:
            with open(paths['lorebook'], 'r', encoding='utf-8') as f:
                lore = json.load(f)
        except json.JSONDecodeError:
            pass

    entry = lore.get(entry_name, {'current_description': '', 'history': []})
    entry['current_description'] = content.strip()
    entry['history'].append({
        'chapter':    chapter,
        'content':    content.strip(),
        'updated_at': get_current_time()
    })
    lore[entry_name] = entry

    with open(paths['lorebook'], 'w', encoding='utf-8') as f:
        json.dump(lore, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Cập nhật Lorebook mục \"{entry_name}\" tại chương {chapter}.")
    print(f"  Lịch sử: {len(entry['history'])} lần cập nhật.")


def save_outline_data(paths, content, append=False):
    ensure_dir(paths['summaries_dir'])
    mode = 'a' if append else 'w'
    with open(paths['outline'], mode, encoding='utf-8') as f:
        if append:
            f.write("\n\n" + content.strip())
        else:
            f.write(content.strip() + "\n")
    print(f"[SUCCESS] Đã cập nhật đề cương tại {paths['outline']}.")


def save_foreshadow_data(paths, clue, chapter, status="open", note=""):
    ensure_dir(paths['summaries_dir'])
    foreshadows = []
    if os.path.exists(paths['foreshadow']):
        try:
            with open(paths['foreshadow'], 'r', encoding='utf-8') as f:
                foreshadows = json.load(f)
        except json.JSONDecodeError:
            pass

    updated = False
    for item in foreshadows:
        if item.get('clue', '').lower() == clue.strip().lower():
            item['status'] = status
            item['updated_chapter'] = chapter
            if note:
                item['resolution_note'] = note
            updated = True
            break

    if not updated:
        foreshadows.append({
            'clue': clue.strip(),
            'introduced_chapter': chapter,
            'status': status,
            'note': note.strip(),
            'created_at': get_current_time()
        })

    with open(paths['foreshadow'], 'w', encoding='utf-8') as f:
        json.dump(foreshadows, f, ensure_ascii=False, indent=2)

    status_str = "ĐÃ GIẢI QUYẾT" if status == "resolved" else "MỞ (ĐANG CHỜ)"
    print(f"[SUCCESS] Cập nhật phục bút \"{clue}\" [{status_str}] tại chương {chapter}.")


def save_chapter_data(paths, title, content, summary="", force=False):
    config = load_config(paths)
    current = config['current_chapter']
    next_n  = current + 1

    # Integrity check: previous chapter file must exist
    if current > 0 and not chapter_exists(paths, current):
        if not force:
            print(f"[WARNING] File của Chương {current} ({chapter_filepath(paths, current)}) không tồn tại!")
            print(f"  Có thể có lỗ hổng dữ liệu. Dùng --force hoặc annotation `/Force` để bỏ qua.")
            return False

    fpath = chapter_filepath(paths, next_n)

    # Prepend Markdown header to the saved file
    header  = f"# Chương {next_n}: {title}\n\n"
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(header + content.strip())

    # Update index story.json (metadata only)
    story = load_story(paths)
    if 'chapters' not in story:
        story['chapters'] = []
    story['chapters'].append({
        'chapter_number': next_n,
        'title':          title,
        'file':           fpath.replace('\\', '/'),
        'summary':        summary.strip(),
        'created_at':     get_current_time()
    })
    save_story(paths, story)

    # Update config
    config['current_chapter'] = next_n
    config['last_updated']    = get_current_time()
    save_config(paths, config)

    print(f"[SUCCESS] Đã lưu Chương {next_n}: \"{title}\"")
    print(f"  File markdown : {fpath}")
    print(f"  Index JSON    : {paths['story_json']}")
    if summary.strip():
        print(f"  Tóm tắt (Brief): \"{summary.strip()}\"")

    # Milestone reminder
    if next_n % 10 == 0:
        lo, hi = next_n - 9, next_n
        print("\n" + "=" * 70)
        print(f"[CỘT MỐC] ĐÃ VIẾT ĐỦ {next_n} CHƯƠNG!")
        print(f"  Hãy tóm tắt chương {lo}–{hi} bằng CLI hoặc annotation nháp:")
        print(f'  - CLI: python manage_story.py append-summary --from {lo} --to {hi} --text "..."')
        print(f'  - Nháp: Bắt đầu file draft.md bằng `/Summary --from {lo} --to {hi}`')
        print("=" * 70 + "\n")
    return True


# ─── INIT ─────────────────────────────────────────────────────────────────────
def action_init(args):
    ensure_dir(STORIES_DIR)
    title = args.title.strip()
    slug = args.story_id
    if not slug:
        slug = slugify(title)
    if not slug:
        slug = 'unnamed-story'

    sdir = get_story_dir(slug)
    print(f"[INFO] Đang khởi tạo dự án truyện tại thư mục: {sdir}")
    
    ensure_dir(sdir)
    ensure_dir(os.path.join(sdir, CHAPTERS_DIR))
    ensure_dir(os.path.join(sdir, SUMMARIES_DIR))

    config = {
        'title':           title,
        'author':          args.author or 'Vô danh',
        'genre':           args.genre or 'Chưa phân loại',
        'description':     args.description or 'Chưa có mô tả',
        'current_chapter': 0,
        'last_updated':    get_current_time()
    }
    with open(os.path.join(sdir, CONFIG_PATH), 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    story = {
        'metadata': {
            'title':       config['title'],
            'author':      config['author'],
            'genre':       config['genre'],
            'description': config['description']
        },
        'chapters': []
    }
    with open(os.path.join(sdir, STORY_JSON_PATH), 'w', encoding='utf-8') as f:
        json.dump(story, f, ensure_ascii=False, indent=2)

    with open(os.path.join(sdir, SUMMARIES_DIR, ROLLING_SUMMARY_TXT), 'w', encoding='utf-8') as f:
        f.write(f"=== TÓM TẮT TRUYỆN: {config['title']} ===\n\n")

    with open(os.path.join(sdir, SUMMARIES_DIR, CHARACTER_BIBLE_JSON), 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(sdir, SUMMARIES_DIR, LOREBOOK_JSON), 'w', encoding='utf-8') as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(sdir, SUMMARIES_DIR, OUTLINE_MD), 'w', encoding='utf-8') as f:
        f.write(f"# ĐỀ CƯƠNG TRUYỆN: {config['title']}\n\n"
                f"## 1. MỤC TIÊU CỐT LÕI (ARC 1)\n"
                f"- Mục tiêu chính: Thiết lập nhân vật chính và thế giới.\n"
                f"- Khủng hoảng kích hoạt: Sự kiện biến cố ban đầu.\n\n"
                f"## 2. KẾ HOẠCH CÁC CHƯƠNG ĐẦU TIÊN\n"
                f"- Chương 1: Giới thiệu nhân vật chính, xung đột ban đầu.\n"
                f"- Chương 2: Bước ngoặt và manh mối đầu tiên.\n")

    with open(os.path.join(sdir, SUMMARIES_DIR, FORESHADOW_JSON), 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=2)

    # Initialize default style profile
    default_style_dir = os.path.join(sdir, SUMMARIES_DIR, STYLE_PROFILES_DIR, 'default')
    ensure_dir(default_style_dir)
    with open(os.path.join(sdir, SUMMARIES_DIR, ACTIVE_STYLE_PROFILE_JSON), 'w', encoding='utf-8') as f:
        json.dump({'active_profile': 'default', 'updated_at': get_current_time()}, f, ensure_ascii=False, indent=2)

    draft_path = os.path.join(sdir, CHAPTERS_DIR, 'draft.md')
    if not os.path.exists(draft_path):
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")

    # Set active story
    with open(ACTIVE_STORY_JSON, 'w', encoding='utf-8') as f:
        json.dump({'active_story': slug}, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Đã khởi tạo dự án truyện mới: {title} (ID: {slug})")
    print(f"  Đã đặt làm truyện hoạt động (active).")


# ─── SELECT ───────────────────────────────────────────────────────────────────
def action_select(args):
    ensure_dir(STORIES_DIR)
    slug = args.story_id.strip()
    sdir = get_story_dir(slug)
    if not os.path.exists(sdir):
        print(f"[ERROR] Không tìm thấy truyện với ID: '{slug}' trong thư mục 'stories/'.")
        return

    with open(ACTIVE_STORY_JSON, 'w', encoding='utf-8') as f:
        json.dump({'active_story': slug}, f, ensure_ascii=False, indent=2)

    try:
        with open(os.path.join(sdir, CONFIG_PATH), 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[SUCCESS] Đã chuyển sang truyện: \"{config['title']}\" (ID: {slug})")
    except Exception:
        print(f"[SUCCESS] Đã chuyển sang truyện (ID: {slug})")


# ─── STORIES (LIST) ───────────────────────────────────────────────────────────
def action_stories(args):
    ensure_dir(STORIES_DIR)
    active = get_active_story()
    
    dirs = []
    if os.path.exists(STORIES_DIR):
        dirs = [d for d in os.listdir(STORIES_DIR) if os.path.isdir(os.path.join(STORIES_DIR, d))]
    
    print("=== DANH SÁCH CÁC TRUYỆN HIỆN CÓ ===")
    if not dirs:
        print("  (Không có truyện nào. Dùng lệnh 'init' để khởi tạo truyện đầu tiên).")
        return
        
    for d in dirs:
        active_marker = " * [ACTIVE]" if d == active else "  "
        title = d
        config_path = os.path.join(STORIES_DIR, d, CONFIG_PATH)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    title = config.get('title', d)
            except Exception:
                pass
        print(f"{active_marker} - {d:<25} (Tên: {title})")


# ─── SAVE (WITH ANNOTATION ROUTING) ───────────────────────────────────────────
def action_save(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        return

    if not os.path.exists(paths['draft']):
        print(f"[ERROR] Không tìm thấy file nháp tại: {paths['draft']}.")
        return

    content = open(paths['draft'], 'r', encoding='utf-8').read().strip()
    if not content or content == "Viết chương mới tại đây...":
        print(f"[ERROR] File nháp trống. Hãy viết truyện vào {paths['draft']} trước.")
        return

    lines = content.split('\n')
    first_line = lines[0].strip()

    # 1. /Summary or /story-summary
    if first_line.startswith('/Summary') or first_line.startswith('/story-summary'):
        from_match = re.search(r'--from\s+(\d+)', first_line)
        to_match = re.search(r'--to\s+(\d+)', first_line)
        if not from_match or not to_match:
            print("[ERROR] Sai cú pháp /Summary hoặc /story-summary. Ví dụ: /story-summary --from 1 --to 10")
            return
        from_ch = int(from_match.group(1))
        to_ch = int(to_match.group(1))
        text = '\n'.join(lines[1:]).strip()
        save_summary_data(paths, from_ch, to_ch, text)
        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 2. /Lore or /story-lore
    elif first_line.startswith('/Lore') or first_line.startswith('/story-lore'):
        entry_match = re.search(r'--entry\s+"([^"]+)"', first_line) or re.search(r'--entry\s+(\S+)', first_line)
        chapter_match = re.search(r'--chapter\s+(\d+)', first_line)
        if not entry_match or not chapter_match:
            print('[ERROR] Sai cú pháp /Lore hoặc /story-lore. Ví dụ: /story-lore --entry "Thành Phố X" --chapter 5')
            return
        entry_name = entry_match.group(1)
        chapter_num = int(chapter_match.group(1))
        lore_content = '\n'.join(lines[1:]).strip()
        save_lore_data(paths, entry_name, chapter_num, lore_content)
        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 3. /Character or /story-character
    elif first_line.startswith('/Character') or first_line.startswith('/story-character'):
        name_match = re.search(r'--name\s+"([^"]+)"', first_line) or re.search(r'--name\s+(\S+)', first_line)
        chapter_match = re.search(r'--chapter\s+(\d+)', first_line)
        if not name_match or not chapter_match:
            print('[ERROR] Sai cú pháp /Character hoặc /story-character. Ví dụ: /story-character --name "Lâm Phong" --chapter 5')
            return
        char_name = name_match.group(1)
        chapter_num = int(chapter_match.group(1))
        char_status = '\n'.join(lines[1:]).strip()
        save_character_data(paths, char_name, chapter_num, char_status)
        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 4. /Outline or /story-outline
    elif first_line.startswith('/Outline') or first_line.startswith('/story-outline'):
        append_flag = '--append' in first_line
        outline_body = '\n'.join(lines[1:]).strip()
        save_outline_data(paths, outline_body, append=append_flag)
        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 5. /Foreshadow or /story-foreshadow
    elif first_line.startswith('/Foreshadow') or first_line.startswith('/story-foreshadow'):
        clue_match = re.search(r'--clue\s+"([^"]+)"', first_line) or re.search(r'--clue\s+(\S+)', first_line)
        chapter_match = re.search(r'--chapter\s+(\d+)', first_line)
        is_resolve = '--resolve' in first_line
        status = 'resolved' if is_resolve else 'open'
        if not clue_match or not chapter_match:
            print('[ERROR] Sai cú pháp /Foreshadow hoặc /story-foreshadow. Ví dụ: /story-foreshadow --clue "Bức thư bí ẩn" --chapter 3')
            return
        clue = clue_match.group(1)
        chapter_num = int(chapter_match.group(1))
        note = '\n'.join(lines[1:]).strip()
        save_foreshadow_data(paths, clue, chapter_num, status=status, note=note)
        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 6. /story-study or /study (Learn style from draft)
    elif first_line.startswith('/story-study') or first_line.startswith('/study'):
        prof_match = re.search(r'--profile\s+([a-zA-Z0-9_-]+)', first_line)
        profile_name = prof_match.group(1) if prof_match else 'default'
        sample_text = '\n'.join(lines[1:]).strip()
        if not sample_text:
            print("[ERROR] Đoạn văn mẫu trong nháp trống. Hãy dán đoạn trích cần học bên dưới dòng /story-study.")
            return

        import scripts.style_analyzer as sa
        print(f"[INFO] Đang phân tích văn phong 5 trục từ đoạn trích dán nháp cho profile '{profile_name}'...")
        analysis = sa.analyze_texts(["Văn bản dán nháp (draft.md)"], [sample_text], profile_id=profile_name)
        md_report = sa.generate_markdown_report(analysis)
        save_style_profile_data(paths, profile_name, analysis, md_report)

        with open(paths['draft'], 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")
        return

    # 7. /Title or /story-title (Chapter drafting)
    elif first_line.startswith('/Title') or first_line.startswith('/story-title'):
        title = first_line.replace('/story-title', '', 1).replace('/Title', '', 1).strip()
        if not title:
            print("[ERROR] Thiếu tiêu đề sau /Title hoặc /story-title.")
            return

        body_lines = lines[1:]
        summary_text = ""
        force = False

        if body_lines and (body_lines[0].strip().startswith('/Brief') or body_lines[0].strip().startswith('/story-brief')):
            summary_text = body_lines[0].strip().replace('/story-brief', '', 1).replace('/Brief', '', 1).strip()
            body_lines = body_lines[1:]

        if body_lines and (body_lines[0].strip().startswith('/Force') or body_lines[0].strip().startswith('/story-force')):
            force = True
            body_lines = body_lines[1:]

        chapter_content = '\n'.join(body_lines).strip()
        success = save_chapter_data(paths, title, chapter_content, summary=summary_text, force=force)
        if success:
            with open(paths['draft'], 'w', encoding='utf-8') as f:
                f.write("Viết chương mới tại đây...")
        return

    # 7. Fallback to CLI argument title
    elif args.title:
        title = args.title.strip()
        summary_text = args.summary or ""
        force = args.force
        chapter_content = content
        success = save_chapter_data(paths, title, chapter_content, summary=summary_text, force=force)
        if success:
            with open(paths['draft'], 'w', encoding='utf-8') as f:
                f.write("Viết chương mới tại đây...")
        return

    else:
        print("[ERROR] Nháp chưa có Annotation hợp lệ ở dòng đầu:")
        print("  - Lưu chương mới : Dòng 1 `/Title <Tên>`, Dòng 2 `/Brief <Tóm tắt>`")
        print("  - Tóm tắt mốc    : Dòng 1 `/Summary --from X --to Y`")
        print("  - Nhân vật       : Dòng 1 `/Character --name \"Tên\" --chapter N`")
        print("  - Bối cảnh       : Dòng 1 `/Lore --entry \"Tên mục\" --chapter N`")
        print("  - Đề cương       : Dòng 1 `/Outline` hoặc `/Outline --append`")
        print("  - Phục bút       : Dòng 1 `/Foreshadow --clue \"Tên\" --chapter N`")
        print("  - Học văn phong  : Dòng 1 `/story-study` hoặc `/story-study --profile <tên>`")


# ─── CONTEXT ──────────────────────────────────────────────────────────────────
def action_context(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        return

    config  = load_config(paths)
    current = config['current_chapter']
    next_n  = current + 1
    M = (current // 10) * 10

    print(f"=== NGỮ CẢNH CẦN ĐỌC TRƯỚC KHI VIẾT CHƯƠNG {next_n} ===\n")

    # 1. Rolling summary
    print(f"[1] ROLLING SUMMARY (tóm tắt chương 1–{M if M > 0 else 'chưa có'}):")
    if M == 0:
        print(f"    → Chưa có tóm tắt mốc (chưa qua mốc 10 chương đầu).")
    else:
        print(f"    → {paths['rolling_summary']}")

    # 2. Unsummarized chapters
    print(f"\n[2] TIẾN TRÌNH CÁC CHƯƠNG CHƯA GỘP TÓM TẮT:")
    unsummarized = list(range(M + 1, current + 1))
    if not unsummarized:
        print("    → Không có (vừa đúng mốc tóm tắt).")
    else:
        story = load_story(paths)
        chapters_meta = {ch['chapter_number']: ch for ch in story.get('chapters', [])}
        
        for n in range(M + 1, current):
            ch_meta = chapters_meta.get(n, {})
            title = ch_meta.get('title', f'Chương {n}')
            brief = ch_meta.get('summary', '').strip()
            if brief:
                print(f"    - [TÓM TẮT] Chương {n}: {title}")
                print(f"      👉 \"{brief}\"")
            else:
                fp = chapter_filepath(paths, n)
                print(f"    - [ĐỌC TOÀN VĂN - Thiếu tóm tắt] Chương {n}: {title} 👉 {fp}")
                
        if current > M:
            ch_meta = chapters_meta.get(current, {})
            title = ch_meta.get('title', f'Chương {current}')
            fp = chapter_filepath(paths, current)
            print(f"    - [BẮT BUỘC ĐỌC TOÀN VĂN ĐỂ BẮT NHỊP] Chương {current}: {title}")
            print(f"      👉 {fp}")

    # 3. Outline & Next chapter goal
    print(f"\n[3] ĐỀ CƯƠNG & ĐỊNH HƯỚNG CỐT TRUYỆN:")
    if os.path.exists(paths['outline']):
        print(f"    → {paths['outline']}")
        # Extract snippet from outline if available
        try:
            with open(paths['outline'], 'r', encoding='utf-8') as f:
                ot_text = f.read()
            match = re.search(rf'Chương\s+{next_n}[:\s\-]+([^\n]+)', ot_text, re.IGNORECASE)
            if match:
                print(f"    🎯 KẾ HOẠCH CHƯƠNG {next_n}: {match.group(1).strip()}")
        except Exception:
            pass
    else:
        print("    → Chưa tạo đề cương.")

    # 4. Foreshadowing / Pending clues
    if os.path.exists(paths['foreshadow']):
        try:
            with open(paths['foreshadow'], 'r', encoding='utf-8') as f:
                foreshadows = json.load(f)
            open_clues = [item for item in foreshadows if item.get('status') == 'open']
            if open_clues:
                print(f"\n[4] PHỤC BÚT / MANH MỐI ĐANG CHỜ GIẢI QUYẾT ({len(open_clues)} mục):")
                for item in open_clues[-5:]:
                    print(f"    - Manh mối: \"{item['clue']}\" (xuất hiện Ch.{item.get('introduced_chapter', '?')})")
                    if item.get('note'):
                        print(f"      Ghi chú: {item['note']}")
        except Exception:
            pass

    # 5. Character bible & Lorebook
    print(f"\n[5] THIẾT LẬP THẾ GIỚI & NHÂN VẬT:")
    print(f"    - Character Bible : {paths['character_bible']}")
    print(f"    - Lorebook        : {paths['lorebook']}")

    # 6. Active Style Profile
    prof_info = get_active_style_profile_info(paths)
    print(f"\n[6] HỒ SƠ VĂN PHONG ĐANG ÁP DỤNG:")
    if prof_info:
        p_id = prof_info['profile_id']
        ver = prof_info.get('version', '1.0.0')
        print(f"    → Profile : '{p_id}' (Phiên bản {ver})")
        print(f"    → Quy tắc : {prof_info['md_path']}")
        guidance = prof_info.get('context_guidance', [])
        for g in guidance:
            print(f"    🎯 {g}")
    else:
        print("    ⚠ Chưa kích hoạt profile văn phong nào. Dùng `/story-study` hoặc `python manage_story.py style --learn` để thiết lập.")


# ─── OUTLINE & FORESHADOW CLI ────────────────────────────────────────────────
def action_outline(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        return
    if not os.path.exists(paths['outline']):
        print("[INFO] Đề cương chưa được tạo. Hãy dùng annotation `/Outline` trong nháp.")
        return
    print("=== ĐỀ CƯƠNG TRUYỆN ===")
    with open(paths['outline'], 'r', encoding='utf-8') as f:
        print(f.read())


def action_foreshadow(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        return
    if not os.path.exists(paths['foreshadow']):
        print("[INFO] Chưa có phục bút nào được ghi nhận.")
        return
    try:
        with open(paths['foreshadow'], 'r', encoding='utf-8') as f:
            foreshadows = json.load(f)
        if not foreshadows:
            print("[INFO] Danh sách phục bút trống.")
            return
        print("=== DANH SÁCH PHỤC BÚT & MANH MỐI ===")
        for item in foreshadows:
            st = "✓ ĐÃ GIẢI" if item.get('status') == 'resolved' else "⏳ ĐANG MỞ"
            print(f"  [{st}] \"{item['clue']}\" (tạo: Ch.{item.get('introduced_chapter')})")
            if item.get('note'):
                print(f"       Ghi chú: {item['note']}")
    except Exception as e:
        print(f"[ERROR] Không thể đọc phục bút: {e}")


def action_list(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        return
    config = load_config(paths)
    story  = load_story(paths)
    chapters = story.get('chapters', [])
    if not chapters:
        print("[INFO] Chưa có chương nào được lưu.")
        return
    print(f"=== DANH SÁCH CHƯƠNG — {config['title']} ({len(chapters)} chương) ===\n")
    for ch in chapters:
        n     = ch['chapter_number']
        title = ch.get('title', '(không có tiêu đề)')
        date  = ch.get('created_at', '')[:10]
        missing = '' if os.path.exists(chapter_filepath(paths, n)) else '  ⚠ FILE THIẾU!'
        print(f"  [{n:04d}] {title:<40} ({date}){missing}")


def action_status(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        return
    config = load_config(paths)
    print("=== THÔNG TIN DỰ ÁN TRUYỆN ===")
    print(f"  Tên truyện : {config['title']}")
    print(f"  Tác giả    : {config['author']}")
    print(f"  Thể loại   : {config['genre']}")
    print(f"  Số chương  : {config['current_chapter']}")
    print(f"  Cập nhật   : {config['last_updated']}")


# ─── QUALITY CHECK & DASHBOARD (INTEGRATED FROM .AGENTS) ──────────────────────
def action_check(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        return
    draft_file = paths['draft']
    if not os.path.exists(draft_file):
        print(f"[ERROR] Không tìm thấy file nháp: {draft_file}")
        return

    import subprocess
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    norm_script = os.path.join(scripts_dir, 'normalize-punctuation.js')
    pat_script  = os.path.join(scripts_dir, 'check-ai-patterns.js')

    print("=== KIỂM SOÁT VĂN PHONG & CHẤT LƯỢNG BẢN NHÁP (.AGENTS TOOLKIT) ===")

    # 1. Punctuation
    if os.path.exists(norm_script):
        try:
            print("[1/2] Chuẩn hóa dấu câu & đối thoại...")
            res = subprocess.run(['node', norm_script, draft_file], capture_output=True, text=True, encoding='utf-8')
            if res.stdout.strip():
                print(f"  {res.stdout.strip()}")
            else:
                print("  ✓ Dấu câu hợp lệ.")
        except Exception as e:
            print(f"  (Bỏ qua normalize: {e})")

    # 2. AI patterns
    if os.path.exists(pat_script):
        try:
            print("[2/2] Quét văn mẫu AI (AI-slop & Clichés)...")
            res = subprocess.run(['node', pat_script, draft_file], capture_output=True, text=True, encoding='utf-8')
            if res.stdout.strip():
                print(f"  {res.stdout.strip()}")
            else:
                print("  ✓ Không phát hiện văn mẫu AI nghiêm trọng.")
        except Exception as e:
            print(f"  (Bỏ qua check-ai-patterns: {e})")


def action_dashboard(args):
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    dash_script = os.path.join(scripts_dir, 'dashboard-server.mjs')
    if not os.path.exists(dash_script):
        print("[ERROR] Không tìm thấy dashboard-server.mjs trong thư mục scripts/")
        return
    import subprocess
    print("=== KHỞI ĐỘNG STORYFLOW DASHBOARD ===")
    print("Đang mở giao diện quản trị truyện trên trình duyệt...")
    try:
        subprocess.run(['node', dash_script, '--root', '.', '--open'])
    except Exception as e:
        print(f"[ERROR] Không thể chạy dashboard: {e}")


# ─── STYLE ENGINE CLI (MULTI-PROFILE) ─────────────────────────────────────────
def action_style(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        return

    import scripts.style_analyzer as sa

    # 1. --list
    if args.list:
        ensure_dir(paths['style_profiles_dir'])
        profiles = [d for d in os.listdir(paths['style_profiles_dir']) if os.path.isdir(os.path.join(paths['style_profiles_dir'], d))]
        active_id = get_active_profile_id(paths)
        print("=== DANH SÁCH STYLE PROFILES HIỆN CÓ ===")
        if not profiles:
            print("  (Chưa có profile nào. Dùng --learn để tạo profile đầu tiên).")
            return
        for p in profiles:
            marker = " * [ACTIVE]" if p == active_id else "  "
            json_p = os.path.join(paths['style_profiles_dir'], p, 'style_profile.json')
            ver = "1.0.0"
            if os.path.exists(json_p):
                try:
                    with open(json_p, 'r', encoding='utf-8') as f:
                        ver = json.load(f).get('version', '1.0.0')
                except Exception:
                    pass
            print(f"{marker} - {p:<20} (Phiên bản {ver})")
        return

    # 2. --set
    if args.set_profile:
        success, msg = set_active_style_profile(paths, args.set_profile)
        if success:
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[ERROR] {msg}")
        return

    # 3. --show
    if args.show is not None:
        p_id = args.show if args.show else get_active_profile_id(paths)
        md_path = os.path.join(paths['style_profiles_dir'], p_id, 'STYLE_PROFILE.md')
        if not os.path.exists(md_path):
            print(f"[ERROR] Không tìm thấy hồ sơ STYLE_PROFILE.md của profile '{p_id}'.")
            return
        with open(md_path, 'r', encoding='utf-8') as f:
            print(f.read())
        return

    # 4. --learn
    if args.learn:
        target_path = args.learn
        profile_name = args.profile or (slugify(os.path.basename(target_path.rstrip('\\/')).split('.')[0]) or 'default')

        if not os.path.exists(target_path):
            print(f"[ERROR] Đường dẫn không tồn tại: {target_path}")
            return

        sources = []
        texts = []

        if os.path.isfile(target_path):
            try:
                with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read().strip()
                if not content:
                    print(f"[ERROR] File mẫu trống: {target_path}")
                    return
                sources.append(target_path)
                texts.append(content)
                print(f"[INFO] Đã đọc 1 file mẫu: {target_path} ({len(content.split()):,} từ)")
            except Exception as e:
                print(f"[ERROR] Không thể đọc file mẫu {target_path}: {e}")
                return
        elif os.path.isdir(target_path):
            print(f"[INFO] Đang quét thư mục mẫu: {target_path}")
            valid_exts = ('.txt', '.md')
            for root, _, files in os.walk(target_path):
                for file in files:
                    if file.lower().endswith(valid_exts):
                        fp = os.path.join(root, file)
                        try:
                            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                                c = f.read().strip()
                            if c:
                                sources.append(fp)
                                texts.append(c)
                                print(f"  + Đã đọc: {file} ({len(c.split()):,} từ)")
                            else:
                                print(f"  - Bỏ qua (file rỗng): {file}")
                        except Exception as e:
                            print(f"  ⚠ Lỗi đọc file {file}: {e}")
            if not texts:
                print(f"[ERROR] Không tìm thấy file văn bản hợp lệ (.txt, .md) nào trong {target_path}")
                return
            print(f"[INFO] Tổng cộng đã nạp thành công {len(texts)} file mẫu.")

        print(f"\n[INFO] Đang phân tích văn phong 5 trục cho profile '{profile_name}'...")
        analysis = sa.analyze_texts(sources, texts, profile_id=profile_name)
        md_report = sa.generate_markdown_report(analysis)
        save_style_profile_data(paths, profile_name, analysis, md_report)
        return

    # Default action if no flags: show active profile status
    active_info = get_active_style_profile_info(paths)
    if active_info:
        print(f"=== PROFILE VĂN PHONG ĐANG HOẠT ĐỘNG: '{active_info['profile_id']}' ===")
        print(f"  Phiên bản : {active_info.get('version', '1.0.0')}")
        print(f"  File JSON : {active_info['json_path']}")
        print(f"  File MD   : {active_info['md_path']}\n")
        print("Dùng `python manage_story.py style --show` để xem toàn văn quy tắc.")
    else:
        print("[INFO] Chưa có profile nào được thiết lập. Dùng `python manage_story.py style --learn <path>` để tạo.")


def main():
    parser = argparse.ArgumentParser(description="StoryFlow CLI - Quản trị và hỗ trợ sáng tác truyện.")
    sub = parser.add_subparsers(dest='command', required=True)

    # init
    p = sub.add_parser('init', help='Khởi tạo dự án truyện mới')
    p.add_argument('--title',       required=True)
    p.add_argument('--author',      default='Vô danh')
    p.add_argument('--genre',       default='Chưa phân loại')
    p.add_argument('--description', default='Chưa có mô tả')
    p.add_argument('--id',          dest='story_id', default=None)

    # select
    p = sub.add_parser('select', help='Chọn truyện làm việc')
    p.add_argument('--id',          dest='story_id', required=True)

    # stories
    sub.add_parser('stories', help='Liệt kê các truyện hiện có')

    # save
    p = sub.add_parser('save', help='Lưu nháp hiện tại')
    p.add_argument('--title',  default=None)
    p.add_argument('--summary', default="")
    p.add_argument('--force',  action='store_true')

    # context
    sub.add_parser('context', help='In ngữ cảnh tối ưu token trước khi viết')

    # outline
    sub.add_parser('outline', help='Xem đề cương truyện')

    # foreshadow
    sub.add_parser('foreshadow', help='Xem danh sách phục bút và manh mối')

    # list
    sub.add_parser('list', help='Danh sách tất cả chương')

    # status
    sub.add_parser('status', help='Xem thông tin truyện')

    # check (from .agents)
    sub.add_parser('check', help='Kiểm tra chất lượng văn phong & khử AI-slop bản nháp (.agents tool)')

    # dashboard (from .agents)
    sub.add_parser('dashboard', help='Mở giao diện Web Dashboard quản lý truyện')

    # style (Style Engine)
    p = sub.add_parser('style', help='Quản lý hồ sơ văn phong truyện mẫu (Style Engine)')
    p.add_argument('--learn', default=None, help='Đường dẫn file hoặc thư mục truyện mẫu để phân tích')
    p.add_argument('--profile', default=None, help='Tên profile cần tạo hoặc cập nhật')
    p.add_argument('--set', dest='set_profile', default=None, help='Chọn profile văn phong làm active')
    p.add_argument('--show', nargs='?', const='', default=None, help='Hiển thị chi tiết Style Profile')
    p.add_argument('--list', action='store_true', help='Liệt kê tất cả Style Profiles hiện có')

    args = parser.parse_args()

    dispatch = {
        'init':       action_init,
        'select':     action_select,
        'stories':    action_stories,
        'save':       action_save,
        'context':    action_context,
        'outline':    action_outline,
        'foreshadow': action_foreshadow,
        'list':       action_list,
        'status':     action_status,
        'check':      action_check,
        'dashboard':  action_dashboard,
        'style':      action_style,
    }
    dispatch[args.command](args)


if __name__ == '__main__':
    main()
