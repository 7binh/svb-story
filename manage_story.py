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
ACTIVE_STORY_JSON         = 'active_story.json'
STORIES_DIR               = 'stories'
GLOBAL_STYLE_LIBRARY_DIR  = 'style_library'

CONFIG_PATH               = 'story_config.json'
STORY_JSON_PATH           = 'story.json'
CHAPTERS_DIR              = 'chapters'
SUMMARIES_DIR             = 'summaries'
ROLLING_SUMMARY_TXT       = 'rolling_summary.txt'
CHARACTER_BIBLE_JSON      = 'character_bible.json'
LOREBOOK_JSON             = 'lorebook.json'
OUTLINE_MD                = 'outline.md'
FORESHADOW_JSON           = 'foreshadow.json'
STYLE_PROFILES_DIR        = 'style_profiles'
ACTIVE_STYLE_PROFILE_JSON = 'active_style_profile.json'


# ─── Helpers ──────────────────────────────────────────────────────────────────
def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


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


def atomic_write(filepath, content, mode='w', encoding='utf-8'):
    """Ghi file an toàn sử dụng tệp tạm thời rồi hoán đổi nguyên tử."""
    dir_name = os.path.dirname(os.path.abspath(filepath))
    ensure_dir(dir_name)
    tmp_path = os.path.join(dir_name, f".tmp_{os.path.basename(filepath)}_{datetime.now().strftime('%f')}")
    try:
        with open(tmp_path, mode, encoding=encoding) as f:
            f.write(content)
        os.replace(tmp_path, filepath)
    except Exception:
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass
        raise


def atomic_save_json(filepath, data):
    content = json.dumps(data, ensure_ascii=False, indent=2)
    atomic_write(filepath, content, mode='w', encoding='utf-8')


def archive_draft_backup(paths, draft_content):
    """Lưu bản sao lưu lịch sử của nháp vào chapters/.draft_backups trước khi thao tác reset."""
    backups_dir = os.path.join(paths['chapters_dir'], '.draft_backups')
    ensure_dir(backups_dir)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    backup_file = os.path.join(backups_dir, f'draft_{ts}.md')
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(draft_content)
    return backup_file


def reset_draft(paths, placeholder="Viết chương mới tại đây..."):
    atomic_write(paths['draft'], placeholder, mode='w', encoding='utf-8')


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
        'story_dir':            sdir,
        'config':               os.path.join(sdir, CONFIG_PATH),
        'story_json':           os.path.join(sdir, STORY_JSON_PATH),
        'draft':                os.path.join(sdir, CHAPTERS_DIR, 'draft.md'),
        'chapters_dir':         os.path.join(sdir, CHAPTERS_DIR),
        'summaries_dir':        os.path.join(sdir, SUMMARIES_DIR),
        'rolling_summary':      os.path.join(sdir, SUMMARIES_DIR, ROLLING_SUMMARY_TXT),
        'character_bible':      os.path.join(sdir, SUMMARIES_DIR, CHARACTER_BIBLE_JSON),
        'lorebook':             os.path.join(sdir, SUMMARIES_DIR, LOREBOOK_JSON),
        'outline':              os.path.join(sdir, SUMMARIES_DIR, OUTLINE_MD),
        'foreshadow':           os.path.join(sdir, SUMMARIES_DIR, FORESHADOW_JSON),
        'style_profiles_dir':   os.path.join(sdir, SUMMARIES_DIR, STYLE_PROFILES_DIR),
        'active_style_profile': os.path.join(sdir, SUMMARIES_DIR, ACTIVE_STYLE_PROFILE_JSON),
        'global_style_library': GLOBAL_STYLE_LIBRARY_DIR,
        'memory_dir':           os.path.join(sdir, SUMMARIES_DIR, 'memory'),
        'canon_json':           os.path.join(sdir, SUMMARIES_DIR, 'memory', 'canon.json'),
        'events_json':          os.path.join(sdir, SUMMARIES_DIR, 'memory', 'events.json'),
        'chars_state_json':     os.path.join(sdir, SUMMARIES_DIR, 'memory', 'characters_state.json'),
        'knowledge_json':       os.path.join(sdir, SUMMARIES_DIR, 'memory', 'knowledge.json'),
        'conflicts_json':       os.path.join(sdir, SUMMARIES_DIR, 'memory', 'conflicts.json'),
    }


def get_memory_engine(paths):
    if not paths:
        return None
    try:
        import scripts.narrative_memory as nm
        story_id = get_active_story()
        return nm.NarrativeMemoryEngine(paths['memory_dir'], paths['chapters_dir'], story_id=story_id)
    except Exception as e:
        print(f"[WARNING] Không thể tải Narrative Memory Engine: {e}")
        return None


def load_config(paths):
    with open(paths['config'], 'r', encoding='utf-8') as f:
        return json.load(f)


def save_config(paths, config):
    atomic_save_json(paths['config'], config)


def load_story(paths):
    if not os.path.exists(paths['story_json']):
        return {'metadata': {}, 'chapters': []}
    try:
        with open(paths['story_json'], 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {'metadata': {}, 'chapters': []}


def save_story(paths, story):
    atomic_save_json(paths['story_json'], story)


def chapter_filepath(paths, n):
    return os.path.join(paths['chapters_dir'], f'chapter_{n:04d}.md')


def chapter_exists(paths, n):
    return os.path.exists(chapter_filepath(paths, n))


# ─── STYLE PROFILE HELPERS (MULTI-PROFILE: STORY & GLOBAL) ───────────────────

def get_active_profile_id(paths):
    if not paths or not os.path.exists(paths['active_style_profile']):
        return None
    try:
        with open(paths['active_style_profile'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('active_profile')
    except Exception:
        return None


def get_active_style_profile_info(paths):
    if not paths or not os.path.exists(paths['active_style_profile']):
        return None
    try:
        with open(paths['active_style_profile'], 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except Exception:
        return None

    active_id = meta.get('active_profile')
    if not active_id:
        return None
    scope = meta.get('scope', 'story')

    if scope == 'global':
        prof_dir = os.path.join(paths['global_style_library'], active_id)
    else:
        prof_dir = os.path.join(paths['style_profiles_dir'], active_id)

    json_path = os.path.join(prof_dir, 'style_profile.json')
    md_path = os.path.join(prof_dir, 'STYLE_PROFILE.md')

    if not os.path.exists(json_path):
        # Backward compatibility with legacy summaries/style_profile.json
        legacy_json = os.path.join(paths['summaries_dir'], 'style_profile.json')
        if os.path.exists(legacy_json) and active_id == 'default':
            try:
                with open(legacy_json, 'r', encoding='utf-8') as f:
                    ldata = json.load(f)
                return {
                    'profile_id': 'legacy',
                    'version': ldata.get('schema_version', ldata.get('version', '1.0.0')),
                    'scope': 'story',
                    'json_path': legacy_json,
                    'md_path': os.path.join(paths['summaries_dir'], 'STYLE_PROFILE.md'),
                    'data': ldata,
                    'context_guidance': ldata.get('context_guidance', [])
                }
            except Exception:
                pass
        return None

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            pdata = json.load(f)
        return {
            'profile_id': active_id,
            'version': pdata.get('schema_version', pdata.get('version', '2.0.0')),
            'scope': scope,
            'json_path': json_path,
            'md_path': md_path,
            'data': pdata,
            'context_guidance': pdata.get('context_guidance', [])
        }
    except Exception:
        return None


def set_active_style_profile(paths, profile_id, scope='story'):
    if scope == 'global':
        prof_dir = os.path.join(paths['global_style_library'], profile_id)
    else:
        prof_dir = os.path.join(paths['style_profiles_dir'], profile_id)

    # Nếu không tìm thấy trong scope yêu cầu, thử tìm kiếm ở scope thay thế
    if not os.path.exists(prof_dir):
        if scope == 'story':
            alt_dir = os.path.join(paths['global_style_library'], profile_id)
            if os.path.exists(alt_dir):
                scope = 'global'
                prof_dir = alt_dir
        elif scope == 'global':
            alt_dir = os.path.join(paths['style_profiles_dir'], profile_id)
            if os.path.exists(alt_dir):
                scope = 'story'
                prof_dir = alt_dir

    if not os.path.exists(prof_dir):
        return False, f"Profile '{profile_id}' không tồn tại trong thư mục {prof_dir}."

    ver = "2.0.0"
    json_path = os.path.join(prof_dir, 'style_profile.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                ver = json.load(f).get('schema_version', '2.0.0')
        except Exception:
            pass

    ensure_dir(paths['summaries_dir'])
    active_meta = {
        'active_profile': profile_id,
        'scope': scope,
        'version': ver,
        'updated_at': get_current_time()
    }
    atomic_save_json(paths['active_style_profile'], active_meta)
    return True, f"Đã chuyển sang profile văn phong: '{profile_id}' (Phạm vi: {scope.upper()} | v{ver})"


def save_style_profile_data(paths, profile_id, profile_data, md_report, scope='story'):
    if scope == 'global':
        prof_dir = os.path.join(GLOBAL_STYLE_LIBRARY_DIR, profile_id)
    else:
        prof_dir = os.path.join(paths['style_profiles_dir'], profile_id)

    ensure_dir(prof_dir)
    json_path = os.path.join(prof_dir, 'style_profile.json')
    md_path = os.path.join(prof_dir, 'STYLE_PROFILE.md')

    atomic_save_json(json_path, profile_data)
    atomic_write(md_path, md_report, encoding='utf-8')

    # Đặt làm profile active cho truyện hiện tại nếu đang trong một dự án
    if paths:
        ensure_dir(paths['summaries_dir'])
        active_meta = {
            'active_profile': profile_id,
            'scope': scope,
            'version': profile_data.get('schema_version', '2.0.0'),
            'updated_at': get_current_time()
        }
        atomic_save_json(paths['active_style_profile'], active_meta)

    print(f"[SUCCESS] Đã lưu Style Profile: '{profile_id}' (v{profile_data.get('schema_version', '2.0.0')} | Phạm vi: {scope.upper()})")
    print(f"  JSON data : {json_path}")
    print(f"  Markdown  : {md_path}")
    if paths:
        print(f"  Đã đặt làm profile hoạt động (active) cho truyện hiện tại.\n")


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

    atomic_save_json(paths['character_bible'], bible)
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

    atomic_save_json(paths['lorebook'], lore)
    print(f"[SUCCESS] Cập nhật Lorebook mục \"{entry_name}\" tại chương {chapter}.")
    print(f"  Lịch sử: {len(entry['history'])} lần cập nhật.")


def save_outline_data(paths, content, append=False):
    ensure_dir(paths['summaries_dir'])
    if append and os.path.exists(paths['outline']):
        with open(paths['outline'], 'r', encoding='utf-8') as f:
            old = f.read()
        atomic_write(paths['outline'], old.rstrip() + "\n\n" + content.strip() + "\n", encoding='utf-8')
    else:
        atomic_write(paths['outline'], content.strip() + "\n", encoding='utf-8')
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

    atomic_save_json(paths['foreshadow'], foreshadows)
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
    atomic_write(fpath, header + content.strip(), encoding='utf-8')

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

    # Hook into Narrative Memory Engine: register confirmed event
    mem_engine = get_memory_engine(paths)
    if mem_engine:
        try:
            mem_engine.add_event(
                chapter=next_n,
                title=title,
                summary=summary.strip() or f"Hoàn thành Chương {next_n}: {title}",
                status="confirmed"
            )
        except Exception as e:
            print(f"[WARNING] Không thể tự động ghi nhận sự kiện vào Narrative Memory: {e}")

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
    atomic_save_json(os.path.join(sdir, CONFIG_PATH), config)

    story = {
        'metadata': {
            'title':       config['title'],
            'author':      config['author'],
            'genre':       config['genre'],
            'description': config['description']
        },
        'chapters': []
    }
    atomic_save_json(os.path.join(sdir, STORY_JSON_PATH), story)

    with open(os.path.join(sdir, SUMMARIES_DIR, ROLLING_SUMMARY_TXT), 'w', encoding='utf-8') as f:
        f.write(f"=== TÓM TẮT TRUYỆN: {config['title']} ===\n\n")

    atomic_save_json(os.path.join(sdir, SUMMARIES_DIR, CHARACTER_BIBLE_JSON), {})
    atomic_save_json(os.path.join(sdir, SUMMARIES_DIR, LOREBOOK_JSON), {})

    with open(os.path.join(sdir, SUMMARIES_DIR, OUTLINE_MD), 'w', encoding='utf-8') as f:
        f.write(f"# ĐỀ CƯƠNG TRUYỆN: {config['title']}\n\n"
                f"## 1. MỤC TIÊU CỐT LÕI (ARC 1)\n"
                f"- Mục tiêu chính: Thiết lập nhân vật chính và thế giới.\n"
                f"- Khủng hoảng kích hoạt: Sự kiện biến cố ban đầu.\n\n"
                f"## 2. KẾ HOẠCH CÁC CHƯƠNG ĐẦU TIÊN\n"
                f"- Chương 1: Giới thiệu nhân vật chính, xung đột ban đầu.\n"
                f"- Chương 2: Bước ngoặt và manh mối đầu tiên.\n")

    atomic_save_json(os.path.join(sdir, SUMMARIES_DIR, FORESHADOW_JSON), [])

    draft_path = os.path.join(sdir, CHAPTERS_DIR, 'draft.md')
    if not os.path.exists(draft_path):
        with open(draft_path, 'w', encoding='utf-8') as f:
            f.write("Viết chương mới tại đây...")

    # Set active story
    atomic_save_json(ACTIVE_STORY_JSON, {'active_story': slug})

    print(f"[SUCCESS] Đã khởi tạo dự án truyện mới: {title} (ID: {slug})")
    print(f"  Đã đặt làm truyện hoạt động (active).")


# ─── SELECT ───────────────────────────────────────────────────────────────────
def action_select(args):
    ensure_dir(STORIES_DIR)
    slug = args.story_id.strip()
    sdir = get_story_dir(slug)
    if not os.path.exists(sdir):
        print(f"[ERROR] Không tìm thấy truyện với ID: '{slug}' trong thư mục 'stories/'.")
        sys.exit(1)

    atomic_save_json(ACTIVE_STORY_JSON, {'active_story': slug})

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


# ─── DRAFT ANNOTATION PARSER (SAFE & FLEXIBLE) ─────────────────────────────────
def parse_draft_annotation(content):
    """
    Bóc tách annotation dòng đầu từ bản nháp:
    - Loại bỏ BOM UTF-8
    - Bỏ qua các dòng trống ở đầu file mà không làm mất annotation
    - Nhận diện linh hoạt thứ tự tham số
    """
    clean = content.lstrip('\ufeff')
    raw_lines = clean.split('\n')

    # Tìm dòng không trống đầu tiên
    first_idx = -1
    for i, line in enumerate(raw_lines):
        if line.strip():
            first_idx = i
            break

    if first_idx == -1:
        return {'type': 'empty', 'error': 'File nháp trống.'}

    first_line = raw_lines[first_idx].strip()
    body_lines = raw_lines[first_idx + 1:]

    # 1. Summary
    if first_line.startswith('/Summary') or first_line.startswith('/story-summary'):
        from_m = re.search(r'--from\s+(\d+)', first_line)
        to_m = re.search(r'--to\s+(\d+)', first_line)
        if not from_m or not to_m:
            return {'type': 'invalid', 'error': 'Sai cú pháp /Summary. Ví dụ: /story-summary --from 1 --to 10'}
        return {
            'type': 'summary',
            'from_ch': int(from_m.group(1)),
            'to_ch': int(to_m.group(1)),
            'text': '\n'.join(body_lines).strip()
        }

    # 2. Lore
    if first_line.startswith('/Lore') or first_line.startswith('/story-lore'):
        entry_m = re.search(r'--entry\s+"([^"]+)"', first_line) or re.search(r'--entry\s+(\S+)', first_line)
        chap_m = re.search(r'--chapter\s+(\d+)', first_line)
        if not entry_m or not chap_m:
            return {'type': 'invalid', 'error': 'Sai cú pháp /Lore. Ví dụ: /story-lore --entry "Tên bối cảnh" --chapter 5'}
        return {
            'type': 'lore',
            'entry': entry_m.group(1),
            'chapter': int(chap_m.group(1)),
            'content': '\n'.join(body_lines).strip()
        }

    # 3. Character
    if first_line.startswith('/Character') or first_line.startswith('/story-character'):
        name_m = re.search(r'--name\s+"([^"]+)"', first_line) or re.search(r'--name\s+(\S+)', first_line)
        chap_m = re.search(r'--chapter\s+(\d+)', first_line)
        if not name_m or not chap_m:
            return {'type': 'invalid', 'error': 'Sai cú pháp /Character. Ví dụ: /story-character --name "Tên" --chapter 5'}
        return {
            'type': 'character',
            'name': name_m.group(1),
            'chapter': int(chap_m.group(1)),
            'status': '\n'.join(body_lines).strip()
        }

    # 4. Outline
    if first_line.startswith('/Outline') or first_line.startswith('/story-outline'):
        return {
            'type': 'outline',
            'append': '--append' in first_line,
            'content': '\n'.join(body_lines).strip()
        }

    # 5. Foreshadow
    if first_line.startswith('/Foreshadow') or first_line.startswith('/story-foreshadow'):
        clue_m = re.search(r'--clue\s+"([^"]+)"', first_line) or re.search(r'--clue\s+(\S+)', first_line)
        chap_m = re.search(r'--chapter\s+(\d+)', first_line)
        if not clue_m or not chap_m:
            return {'type': 'invalid', 'error': 'Sai cú pháp /Foreshadow. Ví dụ: /story-foreshadow --clue "Bức thư" --chapter 3'}
        return {
            'type': 'foreshadow',
            'clue': clue_m.group(1),
            'chapter': int(chap_m.group(1)),
            'status': 'resolved' if '--resolve' in first_line else 'open',
            'note': '\n'.join(body_lines).strip()
        }

    # 6. Study (Learn from draft)
    if first_line.startswith('/story-study') or first_line.startswith('/study'):
        prof_m = re.search(r'--profile\s+([a-zA-Z0-9_-]+)', first_line)
        scope_m = re.search(r'--scope\s+(story|global)', first_line)
        profile_name = prof_m.group(1) if prof_m else 'default'
        scope = scope_m.group(1) if scope_m else 'story'
        sample_text = '\n'.join(body_lines).strip()
        if not sample_text:
            return {'type': 'invalid', 'error': 'Đoạn văn mẫu trong nháp trống. Hãy dán đoạn trích cần học bên dưới dòng /story-study.'}
        return {
            'type': 'study',
            'profile': profile_name,
            'scope': scope,
            'text': sample_text
        }

    # 7. Chapter drafting (/Title or /story-title)
    if first_line.startswith('/Title') or first_line.startswith('/story-title'):
        title = first_line.replace('/story-title', '', 1).replace('/Title', '', 1).strip()
        if not title:
            return {'type': 'invalid', 'error': 'Thiếu tiêu đề sau /Title hoặc /story-title.'}

        summary_text = ""
        force = False
        remaining = []

        # Hỗ trợ thứ tự linh hoạt cho /Brief và /Force ở các dòng tiếp theo
        for line in body_lines:
            s = line.strip()
            if not summary_text and (s.startswith('/Brief') or s.startswith('/story-brief')):
                summary_text = s.replace('/story-brief', '', 1).replace('/Brief', '', 1).strip()
            elif not force and (s.startswith('/Force') or s.startswith('/story-force')):
                force = True
            else:
                remaining.append(line)

        return {
            'type': 'chapter',
            'title': title,
            'summary': summary_text,
            'force': force,
            'content': '\n'.join(remaining).strip()
        }

    return {'type': 'unknown', 'first_line': first_line}


# ─── SAVE (WITH ATOMIC WRITES & ARCHIVING) ─────────────────────────────────────
def action_save(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        sys.exit(1)

    if not os.path.exists(paths['draft']):
        print(f"[ERROR] Không tìm thấy file nháp tại: {paths['draft']}.")
        sys.exit(1)

    with open(paths['draft'], 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.strip() or content.strip() == "Viết chương mới tại đây...":
        print(f"[ERROR] File nháp trống. Hãy viết truyện vào {paths['draft']} trước.")
        sys.exit(1)

    parsed = parse_draft_annotation(content)

    if parsed['type'] == 'summary':
        backup_file = archive_draft_backup(paths, content)
        save_summary_data(paths, parsed['from_ch'], parsed['to_ch'], parsed['text'])
        reset_draft(paths)
        print(f"  [BACKUP] Bản nháp cũ đã được sao lưu tại: {backup_file}")
        return

    elif parsed['type'] == 'lore':
        backup_file = archive_draft_backup(paths, content)
        save_lore_data(paths, parsed['entry'], parsed['chapter'], parsed['content'])
        reset_draft(paths)
        print(f"  [BACKUP] Bản nháp cũ đã được sao lưu tại: {backup_file}")
        return

    elif parsed['type'] == 'character':
        backup_file = archive_draft_backup(paths, content)
        save_character_data(paths, parsed['name'], parsed['chapter'], parsed['status'])
        reset_draft(paths)
        print(f"  [BACKUP] Bản nháp cũ đã được sao lưu tại: {backup_file}")
        return

    elif parsed['type'] == 'outline':
        backup_file = archive_draft_backup(paths, content)
        save_outline_data(paths, parsed['content'], append=parsed['append'])
        reset_draft(paths)
        print(f"  [BACKUP] Bản nháp cũ đã được sao lưu tại: {backup_file}")
        return

    elif parsed['type'] == 'foreshadow':
        backup_file = archive_draft_backup(paths, content)
        save_foreshadow_data(paths, parsed['clue'], parsed['chapter'], status=parsed['status'], note=parsed['note'])
        reset_draft(paths)
        print(f"  [BACKUP] Bản nháp cũ đã được sao lưu tại: {backup_file}")
        return

    elif parsed['type'] == 'study':
        # Đối với học văn phong từ nháp: KHÔNG âm thầm xóa nguồn mẫu của tác giả!
        backup_file = archive_draft_backup(paths, content)
        import scripts.style_analyzer as sa
        profile_name = parsed['profile']
        scope = parsed['scope']
        sample_text = parsed['text']

        print(f"[INFO] Đang phân tích văn phong 5 trục từ đoạn trích dán nháp cho profile '{profile_name}' (Phạm vi: {scope.upper()})...")
        analysis = sa.analyze_texts(["Văn bản dán nháp (draft.md)"], [sample_text], profile_id=profile_name, scope=scope)
        md_report = sa.generate_markdown_report(analysis)
        save_style_profile_data(paths, profile_name, analysis, md_report, scope=scope)

        # Lưu bản sao nguồn mẫu vào profile
        prof_dir = os.path.join(GLOBAL_STYLE_LIBRARY_DIR if scope == 'global' else paths['style_profiles_dir'], profile_name)
        with open(os.path.join(prof_dir, 'source_sample.txt'), 'w', encoding='utf-8') as sf:
            sf.write(sample_text)

        # Giữ nguyên nguồn mẫu trong draft kèm thông báo để tác giả không bị mất dữ liệu
        banner = f"<!-- [STYLE_LEARNED: Profile '{profile_name}' đã được phân tích và lưu thành công. Bạn có thể xóa nháp này khi sẵn sàng.] -->\n\n"
        atomic_write(paths['draft'], banner + sample_text, encoding='utf-8')
        print(f"[INFO] Bản thảo văn mẫu trong draft.md được bảo toàn an toàn (đã lưu bản sao vào {prof_dir}/source_sample.txt).")
        return

    elif parsed['type'] == 'chapter':
        backup_file = archive_draft_backup(paths, content)
        success = save_chapter_data(paths, parsed['title'], parsed['content'], summary=parsed['summary'], force=parsed['force'])
        if success:
            reset_draft(paths)
            print(f"  [BACKUP] Bản nháp chương đã được sao lưu an toàn tại: {backup_file}")
            return
        else:
            print("[ERROR] Quá trình lưu chương thất bại. Bản nháp draft.md được giữ nguyên trạng.")
            sys.exit(1)

    # Fallback to CLI argument title
    elif args.title:
        backup_file = archive_draft_backup(paths, content)
        success = save_chapter_data(paths, args.title.strip(), content, summary=args.summary or "", force=args.force)
        if success:
            reset_draft(paths)
            print(f"  [BACKUP] Bản nháp chương đã được sao lưu an toàn tại: {backup_file}")
            return
        else:
            print("[ERROR] Quá trình lưu chương thất bại. Bản nháp draft.md được giữ nguyên trạng.")
            sys.exit(1)

    else:
        err = parsed.get('error', 'Nháp chưa có Annotation hợp lệ ở dòng đầu.')
        print(f"[ERROR] {err}")
        print("  - Lưu chương mới : Dòng 1 `/Title <Tên>`, Dòng 2 `/Brief <Tóm tắt>` (hoặc `/story-title`, `/story-brief`)")
        print("  - Tóm tắt mốc    : Dòng 1 `/Summary --from X --to Y`")
        print("  - Nhân vật       : Dòng 1 `/Character --name \"Tên\" --chapter N`")
        print("  - Bối cảnh       : Dòng 1 `/Lore --entry \"Tên mục\" --chapter N`")
        print("  - Đề cương       : Dòng 1 `/Outline` hoặc `/Outline --append`")
        print("  - Phục bút       : Dòng 1 `/Foreshadow --clue \"Tên\" --chapter N`")
        print("  - Học văn phong  : Dòng 1 `/story-study [--profile <tên>] [--scope story|global]`")
        sys.exit(1)


# ─── APPEND SUMMARY CLI COMMAND ───────────────────────────────────────────────
def action_append_summary(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        sys.exit(1)

    if args.from_ch <= 0 or args.to_ch < args.from_ch:
        print(f"[ERROR] Phạm vi chương không hợp lệ: --from {args.from_ch} --to {args.to_ch}.")
        sys.exit(1)

    if not args.text.strip():
        print("[ERROR] Nội dung tóm tắt (--text) không được để trống.")
        sys.exit(1)

    save_summary_data(paths, args.from_ch, args.to_ch, args.text)


# ─── CONTEXT (5-LAYER ARCHITECTURE) ──────────────────────────────────────────
def action_context(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        sys.exit(1)

    config  = load_config(paths)
    current = config['current_chapter']
    next_n  = current + 1
    M = (current // 10) * 10

    # Load Narrative Memory Engine
    mem_engine = get_memory_engine(paths)
    prof_info = get_active_style_profile_info(paths)

    # Extract goal from outline if available
    next_goal = f"Phát triển cốt truyện Chương {next_n}"
    if os.path.exists(paths['outline']):
        try:
            with open(paths['outline'], 'r', encoding='utf-8') as f:
                ot_text = f.read()
            match = re.search(rf'Chương\s+{next_n}[:\s\-]+([^\n]+)', ot_text, re.IGNORECASE)
            if match:
                next_goal = match.group(1).strip()
        except Exception:
            pass

    print(f"======================================================================")
    print(f"  BẢN THÔNG TIN ĐA TẦNG (5-LAYER CONTEXT) — SOẠN THẢO CHƯƠNG {next_n}")
    print(f"======================================================================\n")

    # [LỚP A: CORE CONTEXT]
    print(f"=== [LỚP A: CORE CONTEXT — TRỌNG TÂM CHƯƠNG {next_n}] ===")
    print(f"🎯 Mục tiêu chương   : {next_goal}")
    print(f"📍 Tiến trình hiện tại: Đã lưu {current} chương. Đang chuẩn bị viết Chương {next_n}.")
    if mem_engine:
        world_rules = [
            f for f in mem_engine.canon
            if f.get("fact_type") == "world_truth" and f.get("state") == "confirmed" and ("luật" in f.get("tags", []) or "thế_giới" in f.get("tags", []))
        ]
        if world_rules:
            print("📜 Quy tắc thế giới trọng yếu:")
            for r in world_rules[:3]:
                print(f"   • {r['subject']} {r['predicate']} {r['object']}")

    # [LỚP B: RELEVANT STORY MEMORY]
    print(f"\n=== [LỚP B: RELEVANT STORY MEMORY — TIẾN TRÌNH & BỘ NHỚ LIÊN QUAN] ===")
    if mem_engine:
        recent_evs = [e for e in mem_engine.events if e.get("chapter", 0) <= current][-3:]
        if recent_evs:
            print("🔗 Các sự kiện/biến cố tiền đề:")
            for e in recent_evs:
                print(f"   • [Ch.{e.get('chapter')}] {e.get('title')}: {e.get('summary')}")
                if e.get("lasting_changes"):
                    for chg in e["lasting_changes"]:
                        print(f"     👉 Di chứng: {chg}")

        # Active characters dynamic state summary
        tracked_chars = list(mem_engine.characters.keys())
        if tracked_chars:
            print("\n👤 Trạng thái nhân vật trọng điểm:")
            for c_name in tracked_chars[:3]:
                st = mem_engine.get_character_state(c_name)
                injs = st.get("physical_state", {}).get("injuries", [])
                inv = st.get("physical_state", {}).get("inventory", [])
                inj_str = f" | ⚠️ Chấn thương: {', '.join(injs)}" if injs else ""
                inv_str = f" | 🎒 Vật phẩm: {', '.join(inv)}" if inv else ""
                print(f"   • {c_name} (Tâm trạng: {st.get('emotional_state','Bình thường')}{inj_str}{inv_str})")

        # Secrets matrix
        secrets = mem_engine.knowledge.get("secrets", [])
        if secrets:
            print("\n🤫 Ma trận bí mật cần bảo mật:")
            for s in secrets[:3]:
                known_str = ", ".join(s.get("known_by", []))
                print(f"   • \"{s.get('title')}\" [Chỉ {known_str} biết | Status: {s.get('status','concealed')}]")

    # [LỚP C: SOURCE EVIDENCE & CONFLICTS]
    print(f"\n=== [LỚP C: SOURCE EVIDENCE & MÂU THUẪN TRANH CHẤP] ===")
    if mem_engine:
        open_confs = mem_engine.get_open_conflicts()
        if open_confs:
            print(f"⚠️ Cảnh báo: Có {len(open_confs)} mâu thuẫn đang tranh chấp cần chú ý:")
            for c in open_confs:
                print(f"   • [{c.get('severity','critical').upper()}] {c.get('subject')}: {c.get('description')}")
        else:
            print("✅ Không có mâu thuẫn mở giữa các nguồn văn bản.")

    # [LỚP D: STYLE CONTEXT]
    print(f"\n=== [LỚP D: STYLE CONTEXT — HƯỚNG DẪN VĂN PHONG] ===")
    if prof_info:
        p_id = prof_info['profile_id']
        ver = prof_info.get('version', '2.0.0')
        scope = prof_info.get('scope', 'story')
        print(f"   • Profile áp dụng: '{p_id}' (v{ver} | Scope: {scope.upper()})")
        print(f"   • Tệp quy tắc    : {prof_info['md_path']}")
        for g in prof_info.get('context_guidance', []):
            print(f"   🎯 {g}")
    else:
        print("   • No active style profile (Chưa kích hoạt profile văn phong nào. Dùng `/story-study` để thiết lập).")
    print("   🛡️ Giới hạn suy luận: Tôn trọng chấn thương, không để nhân vật nói lộ bí mật họ chưa biết.")

    # [LỚP E: RECENT CONTEXT]
    print(f"\n=== [LỚP E: RECENT CONTEXT — BẮT NHỊP TỪ CHƯƠNG TRƯỚC] ===")
    if current > 0:
        prev_fp = chapter_filepath(paths, current)
        print(f"   • Chương {current} (Chương liền kề): {prev_fp}")
        if os.path.exists(prev_fp):
            try:
                with open(prev_fp, 'r', encoding='utf-8') as pf:
                    lines = [l.strip() for l in pf.readlines() if l.strip()]
                if lines:
                    last_para = lines[-1]
                    print(f"   👉 Đoạn kết Chương {current} để nối mạch:")
                    print(f"      \"{last_para}\"")
            except Exception:
                pass
    else:
        print("   • Chưa có chương trước (đây là chương mở đầu tác phẩm).")

    # Legacy navigation pointers
    print(f"\n--- [TÀI LIỆU THAM CHIẾU HỆ THỐNG] ---")
    print(f"   - Rolling Summary : {paths['rolling_summary']} (Mốc 1–{M if M > 0 else 'chưa có'})")
    print(f"   - Đề cương Arc    : {paths['outline']}")
    print(f"   - Phục bút Clues  : {paths['foreshadow']}")
    print(f"   - Character Bible : {paths['character_bible']}")
    print(f"   - Lorebook        : {paths['lorebook']}")
    print(f"======================================================================\n")


# ─── OUTLINE & FORESHADOW CLI ────────────────────────────────────────────────
def action_outline(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        sys.exit(1)
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
        sys.exit(1)
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
        sys.exit(1)


def action_list(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        sys.exit(1)
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
        sys.exit(1)
    config = load_config(paths)
    print("=== THÔNG TIN DỰ ÁN TRUYỆN ===")
    print(f"  Tên truyện : {config['title']}")
    print(f"  Tác giả    : {config['author']}")
    print(f"  Thể loại   : {config['genre']}")
    print(f"  Số chương  : {config['current_chapter']}")
    print(f"  Cập nhật   : {config['last_updated']}")


# ─── QUALITY CHECK & DASHBOARD ────────────────────────────────────────────────
def action_check(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động.")
        sys.exit(1)
    draft_file = paths['draft']
    if not os.path.exists(draft_file):
        print(f"[ERROR] Không tìm thấy file nháp: {draft_file}")
        sys.exit(1)

    print("=== KIỂM SOÁT VĂN PHONG & CHẤT LƯỢNG BẢN NHÁP (QUALITY GATE) ===")

    with open(draft_file, 'r', encoding='utf-8', errors='replace') as f:
        draft_content = f.read()

    # 1. Native Vietnamese Quality Check (Pure Python)
    import scripts.vn_checker as vnc
    print("[1/2] Kiểm tra văn phong tiếng Việt & khử slop (Native Python)...")
    vn_res = vnc.inspect_text(draft_content)
    has_blocking = False

    if vn_res['slop_findings']:
        has_blocking = True
        print(f"  ❌ Phát hiện {len(vn_res['slop_findings'])} cụm từ văn mẫu AI cấm kỵ:")
        for sf in vn_res['slop_findings']:
            print(f"     - '{sf['matched_text']}': {sf['description']}")
            print(f"       Gợi ý: {sf['suggestion']}")
    else:
        print("  ✓ Không phát hiện cụm từ văn mẫu AI nghiêm trọng.")

    if vn_res['punctuation_issues']:
        print("  ⚠ Cảnh báo định dạng dấu câu:")
        for pi in vn_res['punctuation_issues']:
            print(f"     - {pi['message']}")

    # 2. External pattern checker (Node.js) nếu có
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    pat_script  = os.path.join(scripts_dir, 'check-ai-patterns.js')

    if os.path.exists(pat_script):
        print("[2/2] Kiểm tra mở rộng qua pattern checker...")
        import subprocess
        try:
            res = subprocess.run(['node', pat_script, '--fail-on=blocking', draft_file],
                                 capture_output=True, text=True, encoding='utf-8')
            if res.returncode != 0:
                err_text = res.stderr.strip() or res.stdout.strip()
                if "Cannot find module" in err_text or "MODULE_NOT_FOUND" in err_text:
                    print(f"  [FAIL] Script kiểm tra Node.js crash do thiếu module dependency: {err_text[:200]}")
                    has_blocking = True
                elif res.stdout.strip():
                    print(f"  ❌ Phát hiện vi phạm từ pattern checker:\n{res.stdout.strip()}")
                    has_blocking = True
                else:
                    print(f"  [FAIL] Script kiểm tra Node.js trả về mã lỗi {res.returncode}: {err_text[:200]}")
                    has_blocking = True
            else:
                if res.stdout.strip():
                    print(f"  {res.stdout.strip()}")
                else:
                    print("  ✓ Đạt chuẩn kiểm tra mở rộng.")
        except FileNotFoundError:
            print("  (Node.js không có sẵn trên hệ thống, hoàn tất kiểm tra an toàn bằng bộ lọc Python).")
        except Exception as e:
            print(f"  [ERROR] Lỗi thực thi checker Node.js: {e}")
            has_blocking = True

    if has_blocking:
        print("\n[KẾT QUẢ] ❌ KIỂM SOÁT CHẤT LƯỢNG THẤT BẠI. Cần khắc phục các vi phạm trước khi lưu.")
        sys.exit(1)
    else:
        print("\n[KẾT QUẢ] ✓ BẢN NHÁP ĐẠT TIÊU CHUẨN CHẤT LƯỢNG.")


def action_dashboard(args):
    scripts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'scripts')
    dash_script = os.path.join(scripts_dir, 'dashboard-server.mjs')
    if not os.path.exists(dash_script):
        print("[ERROR] Không tìm thấy dashboard-server.mjs trong thư mục scripts/")
        sys.exit(1)
    import subprocess
    print("=== KHỞI ĐỘNG STORYFLOW DASHBOARD ===")
    print("Đang mở giao diện quản trị truyện trên trình duyệt...")
    try:
        subprocess.run(['node', dash_script, '--root', '.', '--open'])
    except Exception as e:
        print(f"[ERROR] Không thể chạy dashboard: {e}")
        sys.exit(1)


# ─── STYLE ENGINE CLI (MULTI-PROFILE: STORY & GLOBAL) ─────────────────────────
def action_style(args):
    paths = get_paths()
    scope = getattr(args, 'scope', 'story') or 'story'

    import scripts.style_analyzer as sa

    # 1. --list
    if args.list:
        print("=== DANH SÁCH STYLE PROFILES HIỆN CÓ ===")
        active_id = get_active_profile_id(paths) if paths else None
        found_any = False

        show_story = (scope in ['story', 'all']) and (paths is not None)
        show_global = (scope in ['global', 'all']) or (scope == 'story')

        # Liệt kê local story profiles nếu có story active
        if show_story:
            ensure_dir(paths['style_profiles_dir'])
            story_profs = [d for d in os.listdir(paths['style_profiles_dir']) if os.path.isdir(os.path.join(paths['style_profiles_dir'], d))]
            if story_profs:
                found_any = True
                print("  [PHẠM VI TRUYỆN HIỆN TẠI (STORY)]:")
                for p in story_profs:
                    marker = " * [ACTIVE]" if p == active_id else "  "
                    json_p = os.path.join(paths['style_profiles_dir'], p, 'style_profile.json')
                    ver = "2.0.0"
                    if os.path.exists(json_p):
                        try:
                            with open(json_p, 'r', encoding='utf-8') as f:
                                ver = json.load(f).get('schema_version', '2.0.0')
                        except Exception:
                            pass
                    print(f"   {marker} - {p:<20} (Phiên bản {ver})")

        # Liệt kê global profiles
        if show_global:
            ensure_dir(GLOBAL_STYLE_LIBRARY_DIR)
            global_profs = [d for d in os.listdir(GLOBAL_STYLE_LIBRARY_DIR) if os.path.isdir(os.path.join(GLOBAL_STYLE_LIBRARY_DIR, d))]
            if global_profs:
                found_any = True
                print("  [PHẠM VI TOÀN CỤC (GLOBAL LIBRARY)]:")
                for p in global_profs:
                    marker = " * [ACTIVE]" if p == active_id else "  "
                    json_p = os.path.join(GLOBAL_STYLE_LIBRARY_DIR, p, 'style_profile.json')
                    ver = "2.0.0"
                    if os.path.exists(json_p):
                        try:
                            with open(json_p, 'r', encoding='utf-8') as f:
                                ver = json.load(f).get('schema_version', '2.0.0')
                        except Exception:
                            pass
                    print(f"   {marker} - {p:<20} (Phiên bản {ver})")

        if not found_any:
            print("  (Chưa có profile nào. Dùng `python manage_story.py style --learn <path>` để tạo).")
        return

    # 2. --set
    if args.set_profile:
        if not paths:
            print("[ERROR] Cần chọn một truyện hoạt động trước khi đặt active profile.")
            sys.exit(1)
        success, msg = set_active_style_profile(paths, args.set_profile, scope=scope)
        if success:
            print(f"[SUCCESS] {msg}")
        else:
            print(f"[ERROR] {msg}")
            sys.exit(1)
        return

    # 3. --show
    if args.show is not None:
        p_id = args.show if args.show else (get_active_profile_id(paths) if paths else None)
        if not p_id:
            print("[ERROR] Chưa có profile nào được chọn. Hãy chỉ định tên profile: `python manage_story.py style --show <tên>`")
            sys.exit(1)

        # Tìm trong local trước, sau đó tìm trong global
        md_path = None
        if paths and os.path.exists(os.path.join(paths['style_profiles_dir'], p_id, 'STYLE_PROFILE.md')):
            md_path = os.path.join(paths['style_profiles_dir'], p_id, 'STYLE_PROFILE.md')
        elif os.path.exists(os.path.join(GLOBAL_STYLE_LIBRARY_DIR, p_id, 'STYLE_PROFILE.md')):
            md_path = os.path.join(GLOBAL_STYLE_LIBRARY_DIR, p_id, 'STYLE_PROFILE.md')

        if not md_path or not os.path.exists(md_path):
            print(f"[ERROR] Không tìm thấy hồ sơ STYLE_PROFILE.md của profile '{p_id}'.")
            sys.exit(1)

        with open(md_path, 'r', encoding='utf-8') as f:
            print(f.read())
        return

    # 4. --learn
    if args.learn:
        target_path = args.learn
        profile_name = args.profile or (slugify(os.path.basename(target_path.rstrip('\\/')).split('.')[0]) or 'default')

        if not os.path.exists(target_path):
            print(f"[ERROR] Đường dẫn không tồn tại: {target_path}")
            sys.exit(1)

        sources = []
        texts = []

        if os.path.isfile(target_path):
            try:
                with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read().strip()
                if not content:
                    print(f"[ERROR] File mẫu trống: {target_path}")
                    sys.exit(1)
                sources.append(target_path)
                texts.append(content)
                print(f"[INFO] Đã đọc 1 file mẫu: {target_path} ({len(content.split()):,} âm tiết)")
            except Exception as e:
                print(f"[ERROR] Không thể đọc file mẫu {target_path}: {e}")
                sys.exit(1)
        elif os.path.isdir(target_path):
            print(f"[INFO] Đang quét thư mục mẫu: {target_path}")
            valid_exts = ('.txt', '.md')
            for root, _, files in os.walk(target_path):
                # Bỏ qua các thư mục output profile, git, caches
                if any(x in root for x in ['style_profiles', 'style_library', '.git', '__pycache__']):
                    continue
                for file in sorted(files):
                    if file.lower().endswith(valid_exts) and not file.startswith('STYLE_PROFILE'):
                        fp = os.path.join(root, file)
                        try:
                            with open(fp, 'r', encoding='utf-8', errors='replace') as f:
                                c = f.read().strip()
                            if c:
                                sources.append(fp)
                                texts.append(c)
                                print(f"  + Đã đọc: {file} ({len(c.split()):,} âm tiết)")
                            else:
                                print(f"  - Bỏ qua (file rỗng): {file}")
                        except Exception as e:
                            print(f"  ⚠ Lỗi đọc file {file}: {e}")
            if not texts:
                print(f"[ERROR] Không tìm thấy file văn bản hợp lệ (.txt, .md) nào trong {target_path}")
                sys.exit(1)
            print(f"[INFO] Tổng cộng đã nạp thành công {len(texts)} file mẫu.")

        target_scope = 'global' if scope == 'global' else 'story'
        if target_scope == 'story' and not paths:
            print("[INFO] Chưa chọn truyện, tự động lưu profile vào phạm vi toàn cục (global).")
            target_scope = 'global'

        print(f"\n[INFO] Đang phân tích văn phong 5 trục cho profile '{profile_name}' (Phạm vi: {target_scope.upper()})...")
        analysis = sa.analyze_texts(sources, texts, profile_id=profile_name, scope=target_scope)
        md_report = sa.generate_markdown_report(analysis)
        save_style_profile_data(paths, profile_name, analysis, md_report, scope=target_scope)
        return

    # Mặc định khi không có tham số: in trạng thái profile active
    active_info = get_active_style_profile_info(paths) if paths else None
    if active_info:
        print(f"=== PROFILE VĂN PHONG ĐANG HOẠT ĐỘNG: '{active_info['profile_id']}' ===")
        print(f"  Phiên bản : {active_info.get('version', '2.0.0')}")
        print(f"  Phạm vi   : {active_info.get('scope', 'story').upper()}")
        print(f"  File JSON : {active_info['json_path']}")
        print(f"  File MD   : {active_info['md_path']}\n")
        print("Dùng `python manage_story.py style --show` để xem toàn văn quy tắc.")
    else:
        print("[INFO] Chưa có profile nào được thiết lập. Dùng `python manage_story.py style --learn <path>` để tạo.")


# ─── NARRATIVE MEMORY ENGINE CLI ─────────────────────────────────────────────
def action_memory(args):
    paths = get_paths()
    if not paths:
        print("[ERROR] Chưa chọn truyện hoạt động. Hãy chạy lệnh 'select' hoặc 'init' trước.")
        sys.exit(1)

    engine = get_memory_engine(paths)
    if not engine:
        print("[ERROR] Không thể khởi tạo Narrative Memory Engine.")
        sys.exit(1)

    # 1. Add Fact
    if getattr(args, 'add_fact', False):
        if not args.subject or not args.predicate or not args.object:
            print("[ERROR] Thêm dữ kiện bắt buộc: --subject, --predicate, --object.")
            sys.exit(1)
        tags = args.tags.split(',') if getattr(args, 'tags', None) else None
        fact = engine.add_fact(
            subject=args.subject,
            predicate=args.predicate,
            obj=args.object,
            fact_type=args.type,
            state=args.state,
            chapter=args.chapter,
            quote=args.quote,
            tags=tags
        )
        print(f"[SUCCESS] Đã ghi nhận dữ kiện [{fact['fact_id']}] vào Canon ({fact['state'].upper()}):")
        print(f"  {fact['subject']} -> {fact['predicate']} -> {fact['object']}")
        if fact.get('provenance', {}).get('chapter'):
            print(f"  Nguồn: Chương {fact['provenance']['chapter']} | \"{fact['provenance'].get('quote','')}\"")
        return

    # 2. Timeline
    if getattr(args, 'timeline', False):
        tl = engine.get_timeline(up_to_chapter=args.chapter)
        print(f"=== TRỤC THỜI GIAN NHÂN QUẢ (TIMELINE) — {len(tl)} SỰ KIỆN ===")
        if not tl:
            print("  (Chưa có sự kiện nào được ghi nhận trong timeline)")
            return
        for e in tl:
            print(f"\n[Ch.{e.get('chapter', 0)}] {e.get('title')} ({e.get('status','confirmed').upper()})")
            print(f"  Tóm lược : {e.get('summary')}")
            if e.get('characters_involved'):
                print(f"  Nhân vật : {', '.join(e['characters_involved'])}")
            if e.get('lasting_changes'):
                for chg in e['lasting_changes']:
                    print(f"  👉 Di chứng/Hệ quả: {chg}")
        return

    # 3. Dynamic Character State
    if getattr(args, 'char_name', None):
        state = engine.get_character_state(args.char_name)
        print(f"=== TIẾN TRÌNH NHÂN VẬT: {args.char_name.upper()} (Chương {state.get('current_chapter',0)}) ===")
        print(f"- Mục tiêu chính : {state.get('goals',{}).get('primary', 'Chưa xác định')}")
        print(f"- Tâm trạng       : {state.get('emotional_state', 'Bình thường')}")
        phys = state.get('physical_state', {})
        print(f"- Vị trí hiện tại: {phys.get('location', 'Chưa rõ')}")
        injs = phys.get('injuries', [])
        print(f"- Chấn thương    : {', '.join(injs) if injs else 'Không có (khỏe mạnh)'}")
        inv = phys.get('inventory', [])
        print(f"- Đang mang theo : {', '.join(inv) if inv else 'Không có vật phẩm'}")
        rels = state.get('relationships', {})
        if rels:
            print("- Mối quan hệ    :")
            for target, rel in rels.items():
                print(f"  • Với {target}: {rel}")
        beliefs = state.get('beliefs', {})
        if beliefs:
            print("- Niềm tin & Nhận thức:")
            for b_name, b_val in beliefs.items():
                b_type = "Sự thật" if isinstance(b_val, dict) and b_val.get('is_world_truth') else "Chủ quan/Hiểu lầm"
                print(f"  • {b_name} [{b_type}]")
        return

    # 4. Secrets
    if getattr(args, 'secrets', False):
        secrets = engine.knowledge.get('secrets', [])
        print(f"=== MA TRẬN BÍ MẬT & THÔNG TIN ({len(secrets)} mục) ===")
        if not secrets:
            print("  (Chưa ghi nhận bí mật nào)")
            return
        for s in secrets:
            print(f"\n[{s.get('secret_id')}] \"{s.get('title')}\" [{s.get('status','concealed').upper()}]")
            print(f"  Chủ sở hữu      : {s.get('owner')}")
            print(f"  Người đã biết   : {', '.join(s.get('known_by', []))}")
            print(f"  Độc giả đã biết : {'Có' if s.get('reader_aware') else 'Chưa'}")
            if s.get('reveal_conditions'):
                print(f"  Điều kiện lộ    : {s.get('reveal_conditions')}")
        return

    # 5. Audit / Continuity
    if getattr(args, 'audit', False):
        config = load_config(paths)
        curr = config.get('current_chapter', 0)
        draft_content = ""
        if os.path.exists(paths['draft']):
            with open(paths['draft'], 'r', encoding='utf-8') as df:
                draft_content = df.read()
        issues = engine.audit_continuity(target_chapter=curr + 1, draft_text=draft_content)
        print(f"=== KIỂM ĐỊNH TÍNH NHẤT QUÁN & CONTINUITY (CHƯƠNG {curr + 1}) ===")
        if not issues:
            print("✅ Không phát hiện mâu thuẫn hoặc lỗ hổng continuity nào. Canon toàn vẹn!")
        else:
            print(f"⚠️ Phát hiện {len(issues)} vấn đề cần lưu ý:")
            for idx, iss in enumerate(issues, 1):
                sev = iss.get('severity', 'critical').upper()
                print(f"\n  [{idx}] [{sev}] {iss.get('message')}")
                if iss.get('evidence'):
                    print(f"      Minh chứng: {iss.get('evidence')}")
                if iss.get('suggestion'):
                    print(f"      Đề xuất: {iss.get('suggestion')}")
        return

    # 6. Query
    if getattr(args, 'query', None):
        facts = engine.query_facts(query=args.query)
        print(f"=== KẾT QUẢ TRUY VẤN TỪ KHÓA \"{args.query}\" ({len(facts)} dữ kiện) ===")
        if not facts:
            print("  Không tìm thấy dữ kiện nào khớp.")
        else:
            for f in facts:
                prov = f.get('provenance', {})
                ch_str = f"Chương {prov.get('chapter')}" if prov.get('chapter') else "Chưa rõ chương"
                print(f"- [{f.get('fact_id')}] [{f.get('state','confirmed').upper()}] {f.get('subject')} {f.get('predicate')} {f.get('object')}")
                if prov.get('quote'):
                    print(f"  👉 Minh chứng ({ch_str}): \"{prov.get('quote')}\"")
        return

    # Default overview
    config = load_config(paths)
    print(f"=== NARRATIVE MEMORY ENGINE — TỔNG QUAN BỘ NHỚ TRUYỆN ===")
    print(f"  Truyện đang chọn   : {paths['story_dir']}")
    print(f"  Chương hiện tại    : {config.get('current_chapter', 0)}")
    print(f"  Dữ kiện Canon      : {len(engine.canon)} facts")
    print(f"  Sự kiện Timeline   : {len(engine.events)} events")
    print(f"  Nhân vật tiến trình: {len(engine.characters)} nhân vật")
    print(f"  Bí mật đang quản lý: {len(engine.knowledge.get('secrets', []))} bí mật")
    print(f"  Mâu thuẫn mở       : {len(engine.get_open_conflicts())} mục tranh chấp")
    print("\n👉 Các lệnh truy vấn hữu ích:")
    print("  python manage_story.py memory --query <từ_khóa>")
    print("  python manage_story.py memory --timeline")
    print("  python manage_story.py memory --character <tên>")
    print("  python manage_story.py memory --secrets")
    print("  python manage_story.py memory --audit")


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

    # append-summary
    p = sub.add_parser('append-summary', help='Nối tóm tắt mốc nhiều chương vào rolling_summary.txt')
    p.add_argument('--from', dest='from_ch', type=int, required=True, help='Chương bắt đầu')
    p.add_argument('--to', dest='to_ch', type=int, required=True, help='Chương kết thúc')
    p.add_argument('--text', required=True, help='Nội dung tóm tắt')

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

    # check
    sub.add_parser('check', help='Kiểm tra chất lượng văn phong & khử AI-slop bản nháp')

    # dashboard
    sub.add_parser('dashboard', help='Mở giao diện Web Dashboard quản lý truyện')

    # style (Style Engine)
    p = sub.add_parser('style', help='Quản lý hồ sơ văn phong truyện mẫu (Style Engine)')
    p.add_argument('--learn', default=None, help='Đường dẫn file hoặc thư mục truyện mẫu để phân tích')
    p.add_argument('--profile', default=None, help='Tên profile cần tạo hoặc cập nhật')
    p.add_argument('--set', dest='set_profile', default=None, help='Chọn profile văn phong làm active')
    p.add_argument('--show', nargs='?', const='', default=None, help='Hiển thị chi tiết Style Profile')
    p.add_argument('--list', action='store_true', help='Liệt kê tất cả Style Profiles hiện có')
    p.add_argument('--scope', default='story', choices=['story', 'global', 'all'], help='Phạm vi profile: story (theo truyện), global (toàn cục), all (tất cả)')

    # memory (Narrative Memory Engine)
    p = sub.add_parser('memory', help='Quản lý và truy vấn bộ nhớ truyện dài (Narrative Memory Engine)')
    p.add_argument('--query', default=None, help='Truy vấn dữ kiện/sự kiện theo từ khóa')
    p.add_argument('--timeline', action='store_true', help='Xem trục thời gian sự kiện (Causal Timeline)')
    p.add_argument('--character', dest='char_name', default=None, help='Xem trạng thái tiến trình của nhân vật')
    p.add_argument('--secrets', action='store_true', help='Xem ma trận bí mật và thông tin nhân vật biết')
    p.add_argument('--audit', action='store_true', help='Kiểm định tính nhất quán và quét mâu thuẫn continuity')
    p.add_argument('--add-fact', dest='add_fact', action='store_true', help='Thêm dữ kiện mới vào Canon')
    p.add_argument('--subject', default='', help='Chủ thể của dữ kiện')
    p.add_argument('--predicate', default='', help='Vị ngữ/quan hệ của dữ kiện')
    p.add_argument('--object', default='', help='Đối tượng/nội dung dữ kiện')
    p.add_argument('--type', default='world_truth', choices=['world_truth', 'character_belief', 'character_deception'])
    p.add_argument('--state', default='confirmed', choices=['confirmed', 'draft', 'inferred', 'disputed', 'unresolved'])
    p.add_argument('--chapter', type=int, default=None, help='Chương nguồn')
    p.add_argument('--quote', default='', help='Đoạn trích minh chứng')
    p.add_argument('--tags', default='', help='Các thẻ phân loại (phân cách bằng dấu phẩy)')

    args = parser.parse_args()

    dispatch = {
        'init':           action_init,
        'select':         action_select,
        'stories':        action_stories,
        'save':           action_save,
        'append-summary': action_append_summary,
        'context':        action_context,
        'outline':        action_outline,
        'foreshadow':     action_foreshadow,
        'list':           action_list,
        'status':         action_status,
        'check':          action_check,
        'dashboard':      action_dashboard,
        'style':          action_style,
        'memory':         action_memory,
    }
    dispatch[args.command](args)


if __name__ == '__main__':
    main()
