# BÁO CÁO NGHIỆM THU: NARRATIVE MEMORY ENGINE & LONG-FORM FICTION (PHASE 2)
## REPOSITORY: `c:\Novels\CreateSkills\story-flow`

**Ngày lập:** 21/10/2026  
**Vai trò:** Senior Software Architect, AI Skills Engineer & Narrative Systems Engineer  
**Kết quả kiểm thử:** 35/35 Tests **PASS (100%)** — Không có lỗi, không có test bị bỏ qua hoặc chặn.  

---

## 1. Trạng Thái Git Trước và Sau Khi Nâng Cấp

### 1.1. Trước khi bắt đầu Phase 2
- **Branch:** `main` (tracking `origin/main`)
- **Commit ban đầu:** `622e324` (*feat: add /story-study skill, 5-axis style engine and style enforcement pipeline*)
- **Trạng thái:** Có các file đã chỉnh sửa từ Phase 1 và các file mới chưa commit (`SKILLS_UPGRADE_AUDIT.md`, `UPGRADE_REPORT.md`, `tests/`, `scripts/vn_checker.py`, `scripts/style-whitelist.js`). Toàn bộ thay đổi được bảo vệ nguyên trạng, không bị ghi đè hay rollback.

### 1.2. Sau khi hoàn thành Phase 2
- **Modified files:**
  - `README.md`: Cập nhật cấu trúc thư mục, bổ sung lệnh CLI `memory` và rubric văn học định tính.
  - `manage_story.py`: Mở rộng `get_paths()`, tích hợp `get_memory_engine()`, nâng cấp `action_context()` sang kiến trúc 5 lớp (5-Layer Context), thêm subcommand `action_memory()`, móc nối sự kiện confirmed khi lưu chương.
  - `skills/story/SKILL.md`: Bổ sung điều hướng Narrative Memory CLI.
  - `skills/story-write/SKILL.md`: Nâng cấp sang quy trình 7 bước (Understand -> Plan -> Retrieve 5-Layer -> Write -> Audit -> Repair -> Save).
  - `skills/story-flow/SKILL.md`: Tích hợp chốt chặn kép `check` + `memory --audit`, bảo vệ canon khi lưu thất bại.
  - `skills/story-outline/SKILL.md`: Kết nối 3 nhánh rẽ cốt truyện và sổ phục bút với Narrative Memory.
  - `skills/story-review/SKILL.md`: Bổ sung rubric thẩm định 4 cấp độ (Critical / Significant / Soft / Artistic Choice) kèm dẫn chứng provenance.
  - `skills/story-deslop/SKILL.md`: Thêm guardrail nghiêm cấm làm biến dạng sự thật thế giới, POV và canon khi lọc văn mẫu.
- **Untracked files mới:**
  - `NARRATIVE_MEMORY_DESIGN.md`: Tài liệu thiết kế kiến trúc bộ nhớ truyện dài và phản biện 10 câu hỏi cốt lõi.
  - `NARRATIVE_MEMORY_SPEC.md`: Đặc tả kỹ thuật theo chuẩn `/matt-to-spec` (User Stories, Decisions, Testing).
  - `references/LITERARY_EVALUATION_RUBRIC.md`: Khung đánh giá định tính văn học 8 trục, phân định ranh giới giữa kiểm thử kỹ thuật và cảm thụ văn chương.
  - `scripts/narrative_memory.py`: Module cốt lõi thực thi toàn bộ logic Story Canon, Dynamic Character State, Knowledge Matrix, Secrets, Invariants Audit và 5-Layer Context.
  - `tests/test_narrative_memory.py`: Bộ kiểm thử đơn vị cho Narrative Memory Engine (9 test cases).
  - `tests/test_long_novel_regression.py`: Bộ kiểm thử hồi quy 10 kịch bản tiểu thuyết dài tập (10 test cases).
  - `NARRATIVE_MEMORY_REPORT.md`: Báo cáo nghiệm thu tổng thể.

---

## 2. Bản Sao Lưu & File Kê Khai Toàn Vẹn (Backup & Manifest)

Trước khi thực hiện bất kỳ thao tác chỉnh sửa mã nguồn nào của Phase 2, một bản sao lưu toàn diện đã được tạo ra bên ngoài repository:

- **Thư mục sao lưu:**  
  `c:\Novels\CreateSkills\_backups\story-flow_phase2_pre_backup_20261021_143710\`
- **File kê khai (Manifest):**  
  `c:\Novels\CreateSkills\_backups\story-flow_phase2_pre_backup_20261021_143710\manifest.json`
- **Số lượng file bảo vệ:** 53 files kèm mã băm SHA-256 đối soát.
- **Tính toàn vẹn:** Khởi tạo thành công 100%, bảo đảm khả năng phục hồi nguyên trạng nếu có sự cố.

---

## 3. Việc Áp Dụng Các Matt Skills

1. **`/matt-to-spec`**:
   - Được áp dụng nghiêm ngặt để tạo file `NARRATIVE_MEMORY_SPEC.md` theo cấu trúc: Problem Statement, Solution, 20 User Stories chi tiết, Implementation Decisions (Module, Seams, Schemas), Testing Decisions, Out of Scope, và Further Notes.
2. **`/matt-grill-with-docs`**:
   - Được áp dụng trong Phần 3 của `NARRATIVE_MEMORY_DESIGN.md` để phản biện và giải quyết thấu đáo 10 câu hỏi hóc búa nhất về kiến trúc truyện dài (Canon là gì, xác nhận sự kiện, bảo vệ nháp, phân biệt sự thật vs niềm tin, chống rò rỉ bí mật, ưu tiên văn bản gốc trước summary, xử lý mâu thuẫn tranh chấp, khi nào đọc toàn văn, động lực thay đổi tâm lý, và kiểm tra logic không làm chết văn).
3. **`/matt-writing-for-agents`**:
   - Được áp dụng để chuẩn hóa các tệp `SKILL.md` (`story`, `story-write`, `story-flow`, `story-outline`, `story-review`, `story-deslop`):
     - Rút gọn context pointer, đưa trigger lên đầu.
     - Sử dụng chỉ dẫn khẳng định (positive instructions) thay vì cấm đoán phủ định đơn thuần.
     - Thiết lập tiêu chuẩn hoàn tất (Completion Criteria) rõ ràng và kiểm chứng được.
     - Co-location các khái niệm và loại bỏ trùng lặp thông tin.
4. **`/matt-ask-matt`**:
   - Sử dụng để định vị đúng vai trò của từng skill trong vòng lặp sáng tác, giữ ranh giới sạch giữa các phase, bảo toàn context hygiene và quản lý token hiệu quả.

---

## 4. Thiết Kế Được Triển Khai & Các Quyết Định Cốt Lõi

1. **Story Canon có Provenance:**
   - Mỗi dữ kiện trong Canon mang trạng thái rõ ràng (`confirmed`, `draft`, `inferred`, `disputed`, `unresolved`, `retracted`) kèm chương nguồn, đoạn trích minh chứng và độ tin cậy.
2. **Tách biệt World Truth và Character Belief:**
   - Phân biệt sự thật khách quan của thế giới (`world_truth`) với nhận thức chủ quan hoặc hiểu lầm của nhân vật (`character_belief` với trường `accuracy: true/false`). Dramatic irony được bảo vệ an toàn.
3. **Tiến trình nhân vật theo thời gian (Dynamic State):**
   - Theo dõi chấn thương thể chất (`injuries`), vị trí, vật phẩm mang theo (`inventory`), mục tiêu hiện thời và các biến chuyển tâm lý lớn gắn liền với biến cố xúc tác (`catalyst event`).
4. **Kiểm soát thông tin & Bí mật (Knowledge & Secrets Matrix):**
   - Mỗi bí mật liên kết chặt chẽ với danh sách nhân vật đã biết (`known_by`). Ngăn chặn triệt để lỗi "thấu thị" (omniscient leak) khi nhân vật chưa biết thông tin tự ý nói năng hoặc hành động.
5. **Kiểm định Invariants trước khi lưu:**
   - Tự động quét và phát hiện các lỗi bất biến: nhân vật gãy tay vung kiếm, vật phẩm đã mất tự quay lại chủ cũ, nhân vật nói lộ bí mật người khác.
6. **Bản thông tin 5 lớp (5-Layer Context Builder):**
   - Tái cấu trúc lệnh `manage_story.py context` thành 5 lớp: Lớp A (Core Context), Lớp B (Relevant Story Memory), Lớp C (Evidence & Disputes), Lớp D (Style Context), Lớp E (Recent Context).

---

## 5. Danh Sách Tệp Thêm Mới / Sửa Đổi & Lý Do

| Tệp tin | Trạng thái | Lý do kỹ thuật |
|---|---|---|
| `scripts/narrative_memory.py` | Tạo mới | Module trung tâm thực thi mô hình Canon, Timeline, Dynamic State, Knowledge Matrix, Audit Invariants và 5-Layer Context. |
| `manage_story.py` | Chỉnh sửa | Mở rộng đường dẫn `memory/`, tích hợp `NarrativeMemoryEngine` vào `context`, thêm lệnh CLI `memory`, cập nhật sự kiện tự động khi `save`. |
| `NARRATIVE_MEMORY_DESIGN.md` | Tạo mới | Tài liệu kiến trúc và phản biện 10 câu hỏi cốt lõi theo Matt Grill. |
| `NARRATIVE_MEMORY_SPEC.md` | Tạo mới | Đặc tả kỹ thuật theo chuẩn `/matt-to-spec`. |
| `references/LITERARY_EVALUATION_RUBRIC.md` | Tạo mới | Khung đánh giá văn học định tính 8 trục, bảo vệ sáng tạo nghệ thuật. |
| `skills/story-write/SKILL.md` | Chỉnh sửa | Nâng cấp vòng lặp sáng tác thành quy trình 7 bước toàn diện. |
| `skills/story-flow/SKILL.md` | Chỉnh sửa | Bổ sung chốt chặn `memory --audit` và bảo vệ Canon khi nháp thất bại. |
| `skills/story-review/SKILL.md` | Chỉnh sửa | Tích hợp rubric phân loại phát hiện 4 cấp độ và tra cứu provenance. |
| `skills/story-outline/SKILL.md` | Chỉnh sửa | Đồng bộ 3 nhánh rẽ và phục bút với Narrative Memory. |
| `skills/story-deslop/SKILL.md` | Chỉnh sửa | Bổ sung guardrail bảo vệ Canon và thế giới quan truyện khi khử slop. |
| `skills/story/SKILL.md` | Chỉnh sửa | Bổ sung điều hướng và tra cứu bộ nhớ truyện qua CLI. |
| `README.md` | Chỉnh sửa | Cập nhật cấu trúc thư mục, cây dữ liệu `memory/` và bảng Command Registry. |
| `tests/test_narrative_memory.py` | Tạo mới | Bộ kiểm thử đơn vị cho `narrative_memory.py` (9 test cases). |
| `tests/test_long_novel_regression.py` | Tạo mới | Bộ kiểm thử 10 kịch bản tiểu thuyết dài tập (10 test cases). |

---

## 6. Mô Hình Dữ Liệu (Schema), Migration & Rollback

### 6.1. Cấu trúc thư mục dữ liệu mới
Lưu tại `stories/<active_story_id>/summaries/memory/`:
- `canon.json`: Mảng các đối tượng `Fact` với provenance.
- `events.json`: Chuỗi sự kiện nhân quả sắp xếp theo thứ tự thời gian.
- `characters_state.json`: Bảng ánh xạ trạng thái động của từng nhân vật.
- `knowledge.json`: Danh mục bí mật và thông tin phân quyền nhân vật biết.
- `conflicts.json`: Nhật ký ghi nhận các mâu thuẫn đang tranh chấp giữa các chương.

### 6.2. Tính tương thích ngược & Khởi tạo trễ (Lazy Init)
- Không bắt buộc migration đối với các dự án cũ: các tệp `rolling_summary.txt`, `character_bible.json`, `lorebook.json`, `foreshadow.json` vẫn tiếp tục hoạt động song song.
- Khi người dùng chạy lệnh `context`, `save` hoặc `memory`, hệ thống tự động khởi tạo thư mục `memory/` và các file mặc định nếu chưa tồn tại mà không làm gián đoạn công việc sáng tác.

### 6.3. Khả năng Rollback
- Mọi thao tác ghi tệp bộ nhớ đều sử dụng cơ chế `atomic_save_json` qua file tạm và atomic replace, loại bỏ triệt để nguy cơ hỏng file khi mất điện hoặc dừng đột ngột.
- Bản sao lưu toàn diện trước khi nâng cấp được lưu tại `_backups/story-flow_phase2_pre_backup_20261021_143710/`.

---

## 7. Kết Quả Kiểm Thử Toàn Diện (Test Results)

Chạy kiểm thử tự động với `unittest`:
```powershell
python -m unittest discover -s tests -t . -p "test_*.py"
```

| Suite Kiểm Thử | Tệp Kiểm Thử | Số lượng Test | Kết Quả |
|---|---|---|---|
| P0 Data Integrity & Quality Gate | `tests/test_p0_data_integrity.py` | 5 | **PASS (100%)** |
| Style Engine 2.0 & Multi-Profile | `tests/test_style_engine.py` | 5 | **PASS (100%)** |
| Skills Integrity & Routing | `tests/test_skills_integrity.py` | 3 | **PASS (100%)** |
| Full Regression Baseline | `tests/test_full_regression.py` | 3 | **PASS (100%)** |
| **Narrative Memory Engine** | `tests/test_narrative_memory.py` | **9** | **PASS (100%)** |
| **Long-Novel Regression Fixtures** | `tests/test_long_novel_regression.py` | **10** | **PASS (100%)** |
| **TỔNG CỘNG** | **6 Test Suites** | **35 Tests** | **35 PASS / 0 FAIL (100%)** |

- **Số test NOT RUN:** 0
- **Số test BLOCKED:** 0

---

## 8. Kết Quả Kiểm Thử Hồi Quy 10 Kịch Bản Tiểu Thuyết Dài Tập

1. **Scenario 1 (Unhealed Injury):** Nhân vật bị gãy tay phải ở Chương 1; sang Chương 2 bản nháp miêu tả vung kiếm tay phải -> **Phát hiện chính xác lỗi `injury_inconsistency` (Critical).** (PASS)
2. **Scenario 2 (Item Transfer):** Nhân vật A trao kiếm cho B ở Chương 2; sang Chương 3 bản nháp miêu tả A rút kiếm chiến đấu -> **Phát hiện chính xác lỗi `inventory_inconsistency` (Critical).** (PASS)
3. **Scenario 3 (Secret Containment):** Bí mật chỉ Dạ Lão và Lâm Phong biết; nhân vật Thanh Mai chưa biết nhưng thoại nhắc tới bí mật -> **Phát hiện chính xác lỗi `secret_leak` (Critical).** (PASS)
4. **Scenario 4 (Dramatic Irony):** Độc giả biết Hàn Phong là kẻ hạ độc (world truth), nhưng Lâm Phong tin Liễu gia là thủ phạm (character belief) -> **Tách biệt rạch ròi hai dữ kiện, không làm ô nhiễm Canon.** (PASS)
5. **Scenario 5 (Nonlinear Exposition):** Hé lộ biến cố 10 năm trước ở Chương 5 -> **Ghi nhận quan hệ nhân quả và timeline tương đối mà không làm đảo trật tự sự kiện.** (PASS)
6. **Scenario 6 (Contradictory Sources):** Hai chương ghi hai mùa sinh khác nhau -> **Ghi nhận trạng thái `disputed` kèm hai trích dẫn minh chứng, không âm thầm ghi đè.** (PASS)
7. **Scenario 7 (Dormant Clue Retrieval):** Manh mối ngọc bội gieo ở Chương 1; truy vấn ở Chương 15 -> **Truy xuất chính xác provenance Chương 1 và câu văn gốc.** (PASS)
8. **Scenario 8 (Attitude Shift):** Nhân vật biến chuyển từ ngây thơ sang cảnh giác sau biến cố bị bạn thân phản bội -> **Ghi nhận tiến trình tâm lý và mốc sự kiện xúc tác (Catalyst Event).** (PASS)
9. **Scenario 9 (Style Adaptation):** Profile văn phong hướng dẫn nhịp câu dồn dập trong chiến đấu và chậm rãi trong đối thoại -> **Hệ thống điều chỉnh linh hoạt theo loại cảnh mà không ép buộc một độ dài câu cố định.** (PASS)
10. **Scenario 10 (Draft Failure Isolation):** Bản nháp chứa chi tiết hoang đường gặp lỗi khi lưu -> **Canon không bị ô nhiễm, bản nháp được giữ nguyên trạng.** (PASS)

---

## 9. Giới Hạn Của Bộ Nhớ, Truy Xuất & Đánh Giá Văn Chương

1. **Giới hạn trích xuất tự động bằng regex:**
   - Các kiểm tra tự động bằng code trong `audit_continuity` sử dụng phân tích mẫu (pattern matching) để phát hiện chấn thương cơ thể và tên bí mật. Việc đánh giá ngôn ngữ ngụ ngôn phức tạp hoặc dòng ý thức sâu kín vẫn cần sự tham gia phản biện của AI Reviewer và tác giả.
2. **Không nạp toàn bộ lịch sử truyện vào context:**
   - Hệ thống cố ý chỉ nạp các dữ kiện, nhân vật và bí mật liên quan trực tiếp đến phân cảnh hiện tại để bảo vệ cửa sổ ngữ cảnh (Context hygiene) và tránh làm loãng sự chú ý của mô hình AI.
3. **Phân định ranh giới giữa kiểm thử kỹ thuật và thẩm định nghệ thuật:**
   - Test tự động chỉ xác minh được tính bất biến logic. Chất lượng biểu cảm văn học, tính chân thật của giọng điệu và cảm xúc sâu lắng phải được đánh giá qua khung định tính `LITERARY_EVALUATION_RUBRIC.md`.

---

## 10. Rủi Ro Còn Lại & Đề Xuất Bước Tiếp Theo

1. **Rủi ro còn lại:**
   - Khi tác giả đưa vào tên nhân vật hoặc vật phẩm có nhiều biệt danh/bí danh (aliases) khác nhau, engine cần được cập nhật thêm bảng từ đồng nghĩa (alias map) để tránh bỏ sót khi quét mâu thuẫn.
2. **Đề xuất bước tiếp theo:**
   - Cung cấp giao diện Web Dashboard trực quan hóa trục Timeline nhân quả và cây quan hệ nhân vật dựa trên các tệp `events.json` và `characters_state.json`.
   - Xem xét đưa toàn bộ thay đổi đã kiểm thử lên kho lưu trữ GitHub (`https://github.com/7binh/svb-story.git`).

---

## 11. Xác Nhận Tuyệt Đối Về Dữ Liệu & Quy Tắc An Toàn

- **Không có bất kỳ tệp truyện thật nào của tác giả bị sửa đổi hay xóa bỏ.** Toàn bộ kiểm thử đều chạy trên workspace tạm lập tức giải phóng sau khi xong.
- **Không có lệnh Git commit hoặc Git push nào được chạy tự động.** Toàn bộ thay đổi đang ở trạng thái working tree sẵn sàng để tác giả kiểm tra và quyết định.
