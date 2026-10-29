# ba-workflow-marketplace

Marketplace Claude Code `ba-team` chứa plugin **ba-workflow**: quy trình làm việc cho team Business Analyst, từ tài liệu yêu cầu thô đến gói bàn giao, có phân công module qua Git, gate chất lượng và baseline.

Ý tưởng điều phối tham khảo [olbboy/BA-Kit](https://github.com/olbboy/BA-Kit) (CC BY-NC 4.0); nội dung viết mới, không sao chép.

## Cài đặt
```bash
claude plugin marketplace add NguyenThanhHungDev140503/ba-workflow-marketplace
claude plugin install ba-workflow@ba-team
```
Repo đang private: máy cài cần đăng nhập GitHub có quyền (ví dụ `gh auth login`). Trong phiên Claude Code đang mở, chạy `/reload-plugins`.

Yêu cầu: `python3` (hook, độ phủ test, retro), `git` (phân công module). Tùy chọn: `pandoc` (export DOCX, gói HTML), `mmdc` (render Mermaid), Atlassian MCP đã xác thực qua `/mcp` (export Confluence).

## Bắt đầu nhanh
Mở Claude Code trong thư mục dự án và nhắn "dùng plugin BA" (hoặc `/ba-workflow:ba-guide`): skill `ba-guide` đọc `ba-workspace/` và chỉ bước kế tiếp. Chưa có gì thì:
```
/ba-start intake <đường-dẫn-tài-liệu>
```
`ba-workspace/<slug>/` được tạo tự động; không cần tạo tay. Git không bắt buộc (chỉ cần để nhận module bằng branch).

## Quy trình
Hai vai: **Lead BA** dựng khung và duyệt, **BA** nhận từng module.

| Bước | Lệnh | Kết quả |
|---|---|---|
| 1 | `/ba-start intake <path>` | yêu cầu thô (RAW), bên liên quan, thuật ngữ, câu hỏi mở |
| 2 | `/ba-start backbone --slug <slug>` | phạm vi, module, actor, luồng, `status.md`, `traceability.csv` |
| 3 | `/ba-collab Tôi nhận module <slug>` | branch `ba/<slug>/<module>`, ghi owner |
| 4 | `/ba-start stories --module <slug>` | user story + Gherkin, mỗi scenario có ID |
| 5a | `/ba-start frd` / `srs` (`--module`) | đặc tả nghiệp vụ / kỹ thuật |
| 5b | `/ba-start tests --module <slug>` | test case từ AC, đo độ phủ |
| 5c | `/ba-start check [--module <slug>]` | kiểm nhất quán chéo, lỗi H/M/L |
| 6a | `/ba-start gate --module <slug>` | PASS / CONDITIONAL / REJECT |
| 6b | `/ba-collab Gửi module review <slug>` → Lead: `/ba-collab Duyệt module <slug>` | gói review, baseline hash |
| 7 | `/ba-start impact --slug <slug> "<CR>"` | phân tích ảnh hưởng thay đổi yêu cầu |
| 8 | `/ba-start package --slug <slug>` | gói HTML tự chứa |
| 9 | `/ba-start export docx|confluence --slug <slug>` | DOCX / trang Confluence |
| định kỳ | `/ba-start retro --slug <slug>` | số liệu kỳ + tối đa 3 việc tiếp theo |
| mọi lúc | `/ba-collab Lưu checkpoint` · `Tiếp tục` | lưu / nối lại trạng thái làm việc |

Trạng thái module: `Chưa nhận` → `Đang soạn` → `Chờ review` → `Đã duyệt` (hoặc `Cần sửa`).

## Điểm chính
- **Truy vết:** `traceability.csv` nối RAW → BR → US → FR/NFR → TC; mọi bước cập nhật.
- **Gate:** chấm 6 chiều, đo bằng lệnh; còn câu hỏi chặn thì không thể PASS.
- **Baseline + hook `guard`:** duyệt module ghi hash vào `baselines.csv`; hook hỏi xác nhận trước khi sửa file đã duyệt. Hook không bắt lệnh sửa qua Bash (`sed -i`).
- **An toàn:** không bịa số liệu (thiếu thì tạo câu hỏi mở), không tự `git push`, mọi thao tác ghi ra ngoài (Confluence) cần xác nhận, không lưu token.

## Cấu trúc repo
```
.claude-plugin/marketplace.json
plugins/ba-workflow/
  .claude-plugin/plugin.json
  commands/        ba-start, ba-collab
  skills/          ba-intake … ba-guide, ba-conventions (quy ước chung)
  hooks/           hooks.json, guard.py
  docs/            so sánh BA-Kit, thiết kế 0.3, báo cáo, e2e/ (tài liệu mẫu + checklist)
```
Chi tiết plugin: [plugins/ba-workflow/README.md](plugins/ba-workflow/README.md).

## Tình trạng
Phiên bản 0.3.0. Đã chạy thử luồng intake → checkpoint trên tài liệu mẫu ([kết quả](plugins/ba-workflow/docs/e2e/ket-qua.md)), phần lớn do Claude làm theo skill. **Chưa kiểm:** hộp hỏi của hook trong phiên không tự động, `export confluence` với MCP thật, `export docx` có sơ đồ Mermaid. Muốn tự kiểm: chạy theo [checklist](plugins/ba-workflow/docs/e2e/checklist.md).

## Giấy phép
Chưa chọn giấy phép.
