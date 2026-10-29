# So sánh chi tiết: ba-workflow 0.3.0 vs olbboy/BA-Kit v3.5.0

Nguồn BA-Kit: README, `CLAUDE.md`, `docs/sprint-spine.md`, các SKILL.md `ba-quality-gate`, `ba-writing`, `ba-baseline`, `ba-test-gen`, `ba-consistency`, `ba-export`, `ba-jira`, `ba-confluence`, `ba-retro`, `ba-checkpoint`, `ba-as-built`, `ba-learn`, `.claude/commands/ba-validate.md` (đọc qua web; context7 không có thư viện BA-Kit). Các skill còn lại của BA-Kit (vd `ba-master`, `ba-validation`, `ba-traceability`, `ba-auditor`) chỉ biết qua README/sprint-spine, ghi chú bên dưới đánh dấu **(README)**. BA-Kit dùng CC BY-NC 4.0: ba-workflow chỉ mượn ý tưởng, nội dung viết lại.

## 1. Định vị
| | BA-Kit | ba-workflow |
|---|---|---|
| Mục tiêu | "Squad" 44 chuyên gia cho cá nhân BA; hỏi-đáp theo agent | Quy trình có thứ tự cho **team** BA, mỗi bước sinh artifact kiểm được |
| Đơn vị làm việc | agent (`@ba-xxx`) | bước (`/ba-start <step>`) trên workspace chung |
| Nền tảng | Antigravity, Claude Code, CoWork | Claude Code |
| Phân phối | chép `.agent/skills/*` vào `~/.claude/skills` hoặc `setup.sh` | plugin marketplace, cài một lệnh, có hook |
| Ngôn ngữ | EN + VI (README) | VI |
| Quy mô | 44 skill + 2 connector + 1 meta, 6 command, 14 template, 48 prompt, 831 mục tri thức | 15 skill, 2 command, 1 hook, 0 template, 0 tri thức |
| Giấy phép | CC BY-NC 4.0 | chưa chọn (trống) |
| Độ trưởng thành | ~140 commit, CI `e2e-skills.yml`, mẫu `mini-app-cham-cong` (12 module, 53 story) | chưa chạy end-to-end trên tài liệu thật, chưa có CI/mẫu |

## 2. Điều phối và kiểm soát quy trình
| | BA-Kit | ba-workflow |
|---|---|---|
| Điều phối | `@ba-master` phân loại rồi chuyển agent; sprint spine 7 pha (Discover → … → Reflect) | Router theo bước; mỗi skill kiểm artifact của bước trước, thiếu thì dừng |
| Gate giữa pha | Ghi là quy tắc; "runtime enforcement" là kế hoạch v2.0 | Verdict PASS/CONDITIONAL/REJECT chặn gửi review; trạng thái module có enum; hook chặn-hỏi khi sửa file đã duyệt |
| Hợp đồng vào/ra | frontmatter `phase/inputs/outputs/downstream` mới ở kế hoạch | điều kiện tiên quyết viết ngay trong mỗi skill |
| Chuỗi gợi ý bước kế | `downstream` (kế hoạch) / "Handover: Summon @…" | mỗi skill kết thúc bằng lệnh gợi ý cụ thể |

## 3. Từng nhóm tính năng
| Tính năng | BA-Kit | ba-workflow | Ai tốt hơn |
|---|---|---|---|
| Elicit / phân tích bên liên quan | `ba-identity`, `ba-elicitation`, `ba-questioning`, `ba-facilitation` **(README)** | `ba-intake`: RAW-ID, stakeholders, glossary, Q có nhãn chặn, mâu thuẫn ghi cả hai vế | BA-Kit rộng hơn; ta chặt hơn ở truy vết nguồn |
| Viết yêu cầu / story | `ba-writing`: 2 kiểu AC (Gherkin hoặc bullet), RBAC matrix, ≥ 3 AC, bảng "lý do lười" | `ba-stories`: Gherkin, ≥ 3 scenario, scenario ID, INVEST, cấm tự đặt số | Hòa; BA-Kit có phản bác lý do lười, ta có scenario ID |
| FRD/SRS/NFR | `ba-writing`, `ba-nfr`, 14 template **(README)** | `ba-spec`: FRD/SRS từ story, NFR phải có số | BA-Kit có template; ta ràng buộc chặt hơn |
| Chấm chất lượng | `ba-quality-gate`: 8 chiều (BRD), 5 gate theo loại artifact, PASS ≥ 80 | `ba-gate`: 6 chiều, PASS ≥ 85, lỗi cứng ép REJECT, hạ bậc theo test/consistency | BA-Kit phủ nhiều loại artifact (US, API, DB); ta chặt hơn và có lỗi cứng |
| Test case | `ba-test-gen`: 7 loại, BVA, điểm phủ có trọng số | `ba-testgen`: 7 mã loại, BVA từ số nguồn, đo phủ scenario bằng lệnh, ngưỡng 90% | Ta nhất quán hơn (BA-Kit lẫn mã/ưu tiên/hai ngưỡng); BA-Kit có kỹ thuật bổ sung (decision table) |
| Nhất quán chéo | `ba-consistency`: US↔API↔DB↔BRD, phản biện false positive, severity không định nghĩa | `ba-consistency`: (a)-(e) + liên module, phản biện, H/M/L có định nghĩa | Ta rõ hơn; BA-Kit có DB schema thật |
| Truy vết | `ba-traceability` (RTM) **(README)**, `coverage_checker.py` | `traceability.csv` một schema xuyên suốt, mọi bước cập nhật | Ta dễ kiểm bằng máy |
| Baseline / thay đổi | `ba-baseline` (manifest + history), `ba-guard` nhắc, `ba-change` | `baselines.csv` + hook thật chặn-hỏi, duyệt module, `ba-impact` theo chuỗi truy vết | Ta thực thi được; BA-Kit có lịch sử supersede |
| Cộng tác nhóm | không có | claim bằng branch, kiểm branch remote, review packet, Lead BA duyệt, checkpoint chia sẻ qua Git | Ta |
| Checkpoint | `ba-checkpoint`: `~/.ba-kit`, cục bộ, không kiểm cũ | trong workspace (đi theo Git), so hash khi tiếp tục | Ta |
| Retro | `ba-retro`: metric jsonl + mtime, snapshot delta, ≤ 3 việc | `ba-retro`: `events.csv`, chỉ số có định nghĩa, snapshot, ≤ 3 việc, không đổ lỗi | Ta (BA-Kit tự mâu thuẫn về theo-tác-giả, churn bằng mtime) |
| Xuất DOCX | `gen_docx.py`/pandoc, lint, tên file chuẩn | pandoc, lint, tên file chuẩn, bắt buộc `mmdc` hoặc xác nhận | BA-Kit có script tiếng Việt/watermark; ta chưa có mẫu reference.docx |
| Confluence | md→XHTML, 5 gate, nhãn, CQL | qua MCP, plan trước, map version để phát hiện sửa tay | Ta an toàn hơn (chưa thử thật); BA-Kit có script chạy sẵn |
| Jira | `ba-jira` + scripts (PAT trong `.env`) | **không có** (team không dùng) | — |
| Tri thức / học | BM25 831 mục, `ba-wiki`, `ba-learn` (JSONL, PII) | không có | BA-Kit |
| Sau bàn giao | `ba-as-built` (spec vs bằng chứng giao), `ba-auditor`, `ba-metrics` | không có | BA-Kit |
| Chiến lược / UX / data / diagram | `ba-strategy`, `ba-ux`, `ba-data`, `ba-diagram`, … **(README)** | không có (Mermaid trong backbone/spec) | BA-Kit |
| Đóng gói bàn giao | export, Confluence, Jira | gói HTML một file, kiểm baseline trước khi đóng | Hòa |

## 4. An toàn và chất lượng kỹ thuật
| | BA-Kit | ba-workflow |
|---|---|---|
| Ghi ra ngoài | gate "dừng nếu fail", xác nhận lô ≥ 50; thông tin đăng nhập qua `.env` | luôn xác nhận; plan trước; không token trong chat/file; xác thực qua MCP |
| Idempotent / chạy lại | Jira: dedupe theo `summary ~`; không rollback | map file + dừng ở lỗi đầu, chạy lại không tạo trùng |
| Đo bằng lệnh | có nguyên tắc "verify math with Python" | bắt buộc và có đoạn mã nhúng đã chạy thử (độ phủ, retro) |
| Chống tự lừa | bảng "Common Rationalizations", "Red Flags" ở 33/44 skill | có trong gate; chưa có ở các skill khác |
| Kiểm thử bản thân | CI e2e cho skill | chỉ test thủ công từng đoạn; chưa có eval |

## 5. Kết luận
- **Ta hơn:** làm việc nhóm, thực thi gate bằng hook, một schema truy vết/sự kiện dùng chung, an toàn khi ghi ra ngoài, định nghĩa chỉ số rõ.
- **BA-Kit hơn:** bề rộng (chiến lược, UX, data, compliance), kho tri thức + template + prompt, as-built/learn, kinh nghiệm chạy thật và CI.
- **Rủi ro lớn nhất của ta:** chưa có bằng chứng chạy thật. Skill dài vài chục dòng có thể bị hiểu lệch; cần ca test thực.
- **Học thêm từ BA-Kit nếu cần:** bảng "lý do lười/dấu hiệu sai" cho mọi skill, 14 template, `ba-as-built`.
- **Không nên bắt chước:** 44 agent tự do (khó dự đoán), hai ngưỡng điểm, lưu checkpoint cục bộ.

## 6. Đã tối ưu so với 0.1.0
README cài sai → lệnh plugin thật · thêm duyệt module (trước đó không bước nào đặt `Đã duyệt`) · claim kiểm branch remote · schema traceability cố định · enum trạng thái · slug tự xác định · Mermaid offline nói đúng · intake/backbone không ghi đè.
