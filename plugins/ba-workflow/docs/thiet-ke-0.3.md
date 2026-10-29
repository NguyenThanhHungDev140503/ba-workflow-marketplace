# Thiết kế ba-workflow 0.3.0: test, consistency, export, retro, checkpoint

Trạng thái: **đã cài đặt trong 0.3.0**, trừ `ba-jira` (bỏ theo yêu cầu: team không dùng Jira; các mục Jira bên dưới chỉ để tham khảo). `ba-confluence` đã viết nhưng chưa thử với Atlassian MCP thật. Nguồn phân tích: các SKILL.md của olbboy/BA-Kit v3.5.0 (`ba-test-gen`, `ba-consistency`, `ba-export`, `ba-jira`, `ba-confluence`, `ba-retro`, `ba-checkpoint`, `ba-as-built`, `ba-learn`). BA-Kit là CC BY-NC 4.0: chỉ mượn ý tưởng, viết lại.

## 1. Phân tích BA-Kit: lấy gì, bỏ gì

| Tính năng | Cơ chế BA-Kit | Giữ | Điểm yếu của BA-Kit → cách ta tránh |
|---|---|---|---|
| test-gen | 7 loại test (happy, edge/BVA, error/EP, security, concurrency, data, perf); mỗi AC ≥ 1 TC; ID `TC-<US>-<AC>-<CODE>-<NN>`; điểm phủ có trọng số, ngưỡng 80% | AC→TC bắt buộc, BVA trên mọi trường số/ngày/độ dài, kết quả mong đợi cụ thể | Mã loại và mức ưu tiên không nhất quán (SC/SEC, P1/Critical); hai ngưỡng (80% và 95%) → ta dùng 1 bảng mã, 1 ngưỡng; giá trị biên chỉ lấy từ số có trong nguồn, không bịa |
| consistency | Chuỗi BRD→US→API→DB, 5 bước, bước phản biện loại false positive (trường tính toán, camel/snake, hoãn phạm vi) | Bước phản biện; bảng tóm tắt + bảng lỗi | Có cột severity nhưng không định nghĩa thang → ta định nghĩa H/M/L; không có script, dựa grep → ta đếm bằng lệnh |
| export DOCX | lint (placeholder, link, heading) → gen_docx.py/pandoc → kiểm file > 10KB; tên file có version+ngày | Lint trước, tên file chuẩn, kiểm placeholder = 0 | Sửa tay DOCX bị ghi đè; Mermaid cần ảnh nhưng không nêu công cụ; PDF chưa có → ta ghi rõ mmdc, chỉ DOCX/PDF qua pandoc |
| Jira | story→Summary/Description (Gherkin), MoSCoW→priority, US-ID→label, module→component; dedupe bằng JQL; xác nhận lô ≥ 50; báo Created/Skipped/Failed | Mapping, dedupe theo US-ID, xác nhận trước khi ghi | Dedupe theo `summary ~` mong manh; dry-run không định nghĩa; không có retry/rollback; PAT trong `.env` → ta dedupe theo label US-ID + file map, dry-run mặc định, dừng ở lỗi đầu và chạy lại được, xác thực qua MCP |
| Confluence | md→XHTML storage, TOC macro, nhãn, 5 gate (trùng, version, XHTML hợp lệ, placeholder, parent/space) | Gate trước khi ghi, nhãn, version +1 | Không phát hiện sửa tay trên Confluence → ta lưu version+hash đã đẩy, lệch thì dừng hỏi |
| retro | đọc luồng metric `.jsonl` do skill khác ghi + mtime; cửa sổ 7 ngày; snapshot JSON để tính delta; ≤ 3 action item; không đổ lỗi cá nhân | Cửa sổ, snapshot delta, ≤ 3 việc, không đổ lỗi, mỗi nhận xét trích dẫn sự kiện | Mâu thuẫn "mặc định theo module" vs cột Authors; churn bằng mtime (nhiễu) → ta ghi sự kiện thật vào `events.csv` |
| checkpoint | file md (frontmatter + 4 mục: đang làm, quyết định LOCKED/OPEN, 3 bước tiếp, lưu ý) ở `~/.ba-kit/`, theo branch | 4 mục, LOCKED/OPEN, resume theo branch | Lưu cục bộ nên người khác không tiếp tục được; không phát hiện cũ → ta lưu trong workspace (đi theo Git), resume so hash |
| as-built, learn | so spec với bằng chứng bàn giao; bộ nhớ JSONL + lọc PII | **Hoãn** sang 0.4 | — |

## 2. Kiến trúc: thêm bao nhiêu, đặt ở đâu

Không đổi nguyên tắc: một router `/ba-start`, một command nhóm `/ba-collab`, quy ước dùng chung ở `ba-conventions`, mọi thứ là file trong workspace.

```
Bước 5  stories/spec ─┬─► tests   (ba-testgen)    modules/<m>/tests/
                      └─► check   (ba-consistency) consistency-report.md
Bước 6  gate ◄── đọc test coverage + consistency (không tự chạy lại)
Bước 8  package ──► export docx | jira | confluence   (ba-export, ba-jira, ba-confluence)
Xuyên suốt:  events.csv (ghi) ──► retro (đọc)      checkpoint ◄──► resume (ba-collab)
```

| Skill mới | Gọi bằng | Ghi |
|---|---|---|
| `ba-testgen` | `/ba-start tests --module M` | `modules/M/tests/test-cases.csv`, `test-summary.md` |
| `ba-consistency` | `/ba-start check [--module M]` | `modules/M/consistency-report.md` hoặc `consistency-report.md` (liên module) |
| `ba-export` | `/ba-start export docx --slug S [--module M]` | `export/<slug>-<doc>-v<n>-<yyyymmdd>.docx` |
| `ba-jira` | `/ba-start export jira --slug S [--apply]` | `export/jira-plan.csv`, `export/jira-map.csv` |
| `ba-confluence` | `/ba-start export confluence --slug S [--apply]` | `export/confluence/`, `export/confluence-map.csv` |
| `ba-retro` | `/ba-start retro --slug S [--since 7d]` | `retro/retro-<date>.md`, `retro/snapshot-<date>.json` |
| `ba-checkpoint` | `/ba-collab Lưu checkpoint [nhãn]`, `/ba-collab Tiếp tục [slug]` | `checkpoints/<yyyymmdd-hhmm>-<module>.md` |

Tổng: 9 → 16 skill. Router thêm các step `tests`, `check`, `export <docx|jira|confluence>`, `retro`.

## 3. Thay đổi quy ước chung (`ba-conventions`)

1. **Scenario ID**: mỗi scenario trong story có ID `US-012/S1`, `S2`... (`ba-stories` đánh số). Cần để AC→TC truy được; hiện scenario chỉ có tên.
2. **traceability.csv** thêm cột cuối `TC-ID` → `RAW-ID,BR-ID,module,US-ID,FR-ID,NFR-ID,TC-ID`. File cũ thiếu cột thì coi là rỗng, skill thêm cột khi ghi lần đầu.
3. **TC ID**: `TC-<US số>-<nn>`, vd `TC-012-03`. Loại test là cột, không nhét vào ID.
4. **Mã loại test (một bảng)**: `HP` happy · `BV` biên · `ER` lỗi/không hợp lệ · `AZ` phân quyền · `ST` trạng thái · `DI` toàn vẹn dữ liệu · `PF` hiệu năng. Ưu tiên chỉ `P1/P2/P3`.
5. **Thang severity** (consistency, gate): **H** mâu thuẫn số liệu/quy tắc hoặc đứt chuỗi truy vết · **M** thiếu đối ứng (US không FR, FR không endpoint, trường API không có thuộc tính) · **L** đặt tên/thuật ngữ.
6. **events.csv** (`ba-workspace/<slug>/events.csv`, chỉ thêm dòng): `date,event,module,detail`. Sự kiện: `claim`, `status` (detail `từ→đến`), `gate` (detail `verdict;score;hard`), `tests` (`cov%`), `check` (`H;M;L`), `cr` (CR-ID), `q-open`, `q-close`, `export` (`đích;số mục`), `checkpoint`. Skill nào làm việc đó thì ghi; thiếu thì retro nói rõ là thiếu dữ liệu, không suy đoán.
7. **open-questions** thêm cột `Ngày mở`, `Ngày đóng` (intake tạo, các bước đóng câu hỏi điền).
8. **Bảo mật**: không nhập/hiển thị token; xác thực Atlassian qua MCP (`/mcp`), không `.env`, không PAT trong chat hoặc file.
9. **Cổng bàn giao** (đã có trong `ba-package`) áp dụng nguyên cho mọi `export`: module chưa `Đã duyệt` hoặc lệch baseline thì chỉ xuất khi người dùng xác nhận, và đánh dấu `NHÁP`.

## 4. Thiết kế từng skill

### 4.1 `ba-testgen`
- **Vào**: stories của module (đã có scenario ID), FRD/SRS nếu có (phân quyền, trạng thái, NFR số). Thiếu stories thì dừng.
- **Làm**:
  1. Mỗi scenario → tối thiểu 1 TC. Happy→`HP`, edge→`BV`/`ST`, error→`ER`/`AZ`.
  2. Mỗi trường có ngưỡng/độ dài/ngày trong story hoặc spec → bộ biên `min-1, min, min+1, max-1, max, max+1` (chỉ giá trị suy ra từ số nguồn).
  3. Mỗi vai trò trong ma trận quyền → ít nhất 1 TC `AZ` (được và bị từ chối).
  4. Mỗi chuyển trạng thái trong state diagram, kể cả chuyển không hợp lệ → `ST`.
  5. Mỗi NFR có số → 1 TC `PF` (chỉ nêu tiêu chí, không viết kịch bản tải).
  6. Quy tắc thiếu số/thiếu kết quả → không bịa, ghi Q-ID và đánh dấu TC `[chờ Q-xxx]`.
- **Ra**: `test-cases.csv` cột `TC-ID,US-ID,Scenario,Loại,Ưu tiên,Tiền điều kiện,Bước,Dữ liệu,Kết quả mong đợi,Ghi chú`; `test-summary.md`; cập nhật `traceability.csv` (`TC-ID`) và `events.csv`.
- **Điểm phủ**: `% scenario có ≥ 1 TC` (đếm bằng lệnh). Ngưỡng 90%. Phụ: số trường có BV, số vai trò có AZ.
- **Cấm**: dữ liệu giả kiểu `test123`; "kết quả: hoạt động bình thường".
- **Xuống gate**: có thư mục `tests/` mà phủ < 90% → PASS hạ thành CONDITIONAL.

### 4.2 `ba-consistency`
- **Phạm vi mỗi module**: (a) US↔FR hai chiều; (b) FR↔endpoint trong SRS; (c) trường request/response↔thuộc tính thực thể ER; (d) số liệu cùng một quy tắc ở story vs spec vs NFR; (e) thuật ngữ vs `glossary.md`.
- **Liên module** (`check` không `--module`): thực thể định nghĩa ở nhiều module nhưng khác thuộc tính; phụ thuộc trong `modules.md` vs tham chiếu thực tế; trùng/xung đột `BR`.
- **Quy trình**: kiểm kê artifact → đối chiếu từng cặp → **bước phản biện** (loại: trường tính toán, khác quy ước camel/snake, phạm vi đã hoãn có Q-ID) → báo cáo.
- **Ra**: bảng tóm tắt `Kiểm tra | Số mục | Khớp | Lệch | %`; bảng lỗi `# | Loại | Nguồn | Đích | Lỗi | Severity | Cách sửa`; mỗi lỗi có file:dòng, không có thì không ghi.
- **Xuống gate**: còn lỗi **H** chưa sửa → CONDITIONAL; báo cáo cũ hơn artifact (so mtime) → gate ghi "consistency đã cũ", không tính.

### 4.3 `ba-export` (DOCX/PDF)
- **Vào**: `dist/` hoặc module; qua cổng bàn giao.
- **Làm**: lint (placeholder `TBD|TODO|XXX|{{`, link nội bộ hỏng, bậc heading nhảy cấp, thiếu metadata) → ghép md + YAML (`title, author, version, date, classification`) → render Mermaid thành SVG/PNG bằng `mmdc`; không có `mmdc` thì **dừng và nói**, không để mã Mermaid thô trong file → `pandoc` với `--toc`, `--reference-doc` nếu có `export/reference.docx` → kiểm file tồn tại, > 10KB, placeholder trong kết quả = 0.
- **Ràng buộc**: sửa trong md rồi xuất lại, không sửa tay DOCX (ghi vào footer/README). Môi trường hiện tại: có `pandoc`, **chưa có** `mmdc` và `python-docx`.

### 4.4 `ba-jira`
- **Ánh xạ**: module→**Epic** (nhãn `module:<slug>`); US→**Story** (Summary = tiêu đề; Description = "Là… tôi muốn… để…" + Gherkin; nhãn `US-012`, `ba:<slug>`; Component = module; priority Must/Should/Could→Highest/High/Medium); TC→**Sub-task** hoặc issue Test, chỉ khi có `--with-tests`.
- **Dedupe**: JQL `project = P AND labels = "US-012"`; có rồi thì Skipped (hoặc Update nếu `--update`). Kết quả luôn ghi `jira-map.csv` `ID,jira_key,url,ngày`.
- **An toàn**: luôn chạy **plan** trước (`jira-plan.csv`: tạo/bỏ qua/cập nhật); chỉ ghi khi `--apply` + người dùng xác nhận đúng số lượng. Dừng ở lỗi đầu tiên, mọi mục đã tạo đã nằm trong map nên chạy lại là tiếp tục, không trùng. Không xóa, không chuyển trạng thái ticket.
- **Kết nối**: Atlassian MCP nếu đã được cấp quyền (tên tool đọc bằng ToolSearch lúc chạy, không hard-code); chưa có thì xuất `jira-import.csv` cho Jira CSV importer. Hiện server `atlassian` cần `/mcp` xác thực.
- **Ra**: báo cáo Created / Skipped / Failed; `events.csv`.

### 4.5 `ba-confluence`
- **Cây trang**: gốc `<slug> - Gói BA` → mỗi module một trang con (Stories, FRD, SRS) + trang Truy vết + trang Tồn đọng. Cần `space` và `parent` do người dùng cung cấp, xác minh tồn tại trước.
- **Chuyển đổi**: theo định dạng mà tool MCP nhận (đọc schema lúc chạy); fallback xuất `export/confluence/*.md` + XHTML storage. Mermaid: đính kèm SVG nếu có `mmdc`, không thì khối mã; footer "Tạo bởi ba-workflow, baseline v<n>, <ngày>"; nhãn `ba-workflow`, loại tài liệu, version.
- **Gate**: không placeholder; space/parent đúng; tìm trang trùng tiêu đề bằng CQL → tạo mới hay cập nhật.
- **Phát hiện sửa tay**: `confluence-map.csv` lưu `ID,page_id,version_đã_đẩy,sha_nội_dung`. Trang hiện tại có version/hash khác → **dừng**, cho xem khác biệt, hỏi ghi đè, gộp, hay bỏ qua.
- **An toàn**: plan → xác nhận → ghi; không xóa trang.

### 4.6 `ba-retro`
- **Dữ liệu**: `events.csv` (chính), `changes/CR-*.md`, `open-questions.md` (có ngày), `gate-report` lịch sử qua `events.csv`. Git log chỉ khi `--git` và có `.git/`. Mặc định cửa sổ 7 ngày (`24h`, `14d`, `30d`, `--since`).
- **Chỉ số (định nghĩa cụ thể)**: số module đạt `Đã duyệt` trong kỳ; tỷ lệ `PASS / (PASS+CONDITIONAL+REJECT)` của các lần gate; số lần gate trung bình đến PASS; **cycle time** = trung vị `Đang soạn → Đã duyệt`; **churn** = số lần module quay `Cần sửa` + số CR chạm vào; chiều gate hay trượt nhất; tuổi trung vị câu hỏi mở và số Q chặn tồn > 5 ngày; số lần chặn bởi hook guard (nếu ghi).
- **Ra**: tóm tắt một dòng, đã bàn giao, churn, xu hướng so với `snapshot` kỳ trước (không có thì ghi "retro đầu tiên", bỏ delta), điểm hotspot (top 5 module), ≤ 3 việc tiếp theo, mỗi việc trỏ một lệnh cụ thể (vd lỗi từ mơ hồ lặp lại → `/ba-start stories --module X` + đóng Q-xxx).
- **Quy tắc**: mọi nhận xét trích một sự kiện/CR/file; theo module, **không** theo người trừ khi có `--by-owner`; không đủ dữ liệu thì nói thiếu gì.

### 4.7 `ba-checkpoint` (qua `/ba-collab`)
- **Lưu**: `checkpoints/<yyyymmdd-hhmm>-<module>.md`. Frontmatter: `ts, branch, module, step, active_artifact, label`. Thân: *Đang làm*; *Quyết định* (LOCKED/OPEN); *3 bước tiếp* (đủ cụ thể để làm mà không đọc lại ghi chú); *Lưu ý*. Thêm khối tự tính: trạng thái module, verdict gate gần nhất, Q chặn đang mở, `sha256` của `status.md` và các file stories/spec.
- **Tiếp tục**: lấy checkpoint mới nhất của branch/module; so `sha256` hiện tại với lúc lưu; nêu **file đã đổi từ checkpoint** (do người khác hoặc phiên khác) trước khi đề xuất bước tiếp; module đã đổi trạng thái thì cảnh báo.
- **Khác BA-Kit**: nằm trong workspace nên commit cùng branch → BA khác nhận bàn giao module đọc được. Không commit tự động ngoài lệnh claim/duyệt; checkpoint chỉ ghi file, người dùng tự commit. Tự động lưu để dành sau (hook `PreCompact`), chưa làm.

## 5. Gate, package, impact, collab: sửa gì

- `ba-gate`: thêm 2 điều kiện hạ bậc (phủ test < 90%, lỗi H còn mở) và ghi `events.csv`. **Không** thêm chiều chấm điểm → trọng số hiện tại giữ nguyên, không phải tính lại.
- `ba-package`: thêm mục "Test" và "Báo cáo nhất quán" nếu có; làm chỗ chung gọi `export`.
- `ba-impact`: ghi `cr` vào `events.csv`; liệt kê TC bị ảnh hưởng (qua cột `TC-ID`) và trang Jira/Confluence cần cập nhật (qua các map).
- `ba-collab`: thêm chế độ `checkpoint`/`tiếp tục`; ghi `claim`/`status` vào `events.csv`; chế độ "Duyệt" băm thêm `tests/` (hiện chỉ `stories/` và `spec/`).
- `hooks/guard.py`: không đổi; tự bảo vệ `tests/*.csv` sau khi chúng nằm trong `baselines.csv`.

## 6. Thứ tự cài đặt đề xuất (mỗi bước độc lập, kiểm được)

1. `ba-conventions` (scenario ID, cột `TC-ID`, `events.csv`, severity) + `ba-stories` đánh số scenario + `ba-intake` thêm ngày câu hỏi.
2. `ba-testgen` → 3. `ba-consistency` → 4. nối vào `ba-gate`.
5. `ba-checkpoint` + `ba-collab` (nhỏ, không phụ thuộc ngoài).
6. `ba-export` DOCX (cần `pandoc`; `mmdc` tùy chọn).
7. `ba-retro` (cần `events.csv` đã được ghi vài chu kỳ mới có ý nghĩa).
8. `ba-jira`, `ba-confluence` cuối (cần Atlassian MCP và sandbox để thử).

## 7. Rủi ro và việc chưa rõ

- Jira/Confluence chưa thể thử thật trong phiên này (chưa xác thực Atlassian MCP); phải thử trên project/space nháp, `--apply` mặc định tắt.
- Tên tool và định dạng body của Atlassian MCP chưa xác minh; skill phải đọc schema lúc chạy.
- `mmdc` chưa cài: DOCX không có sơ đồ cho đến khi cài (`npm i -g @mermaid-js/mermaid-cli`).
- Cột `TC-ID` và scenario ID làm thay đổi định dạng artifact của 0.2.0 → dự án cũ cần chạy lại `stories` hoặc để skill tự đánh số bổ sung.
- 16 skill làm tăng chi phí nạp mô tả; giữ `description` mỗi skill ≤ 2 câu.
