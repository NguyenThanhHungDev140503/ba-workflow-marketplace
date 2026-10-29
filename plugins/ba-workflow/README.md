# ba-workflow

Bộ lệnh Claude Code cho team BA: intake -> backbone -> claim module -> stories -> FRD/SRS -> tests + check -> gate + review + duyệt -> impact -> package/export.
Viết mới, lấy ý tưởng điều phối từ [olbboy/BA-Kit](https://github.com/olbboy/BA-Kit) (không chép nội dung, vì BA-Kit dùng CC BY-NC 4.0). So sánh: [docs/so-sanh-ba-kit.md](docs/so-sanh-ba-kit.md). Thiết kế 0.3: [docs/thiet-ke-0.3.md](docs/thiet-ke-0.3.md).

## Cài
```
/plugin marketplace add <đường-dẫn-tới-thư-mục-ba-workflow-marketplace>
/plugin install ba-workflow@ba-team
```
Cần `python3` (hook guard, retro, độ phủ test) và `pandoc` (export DOCX). Tùy chọn: `mmdc` (render Mermaid cho DOCX/gói HTML), Atlassian MCP đã xác thực qua `/mcp` (export Confluence).

## Không nhớ lệnh?
Nói "dùng plugin BA" / "làm gì tiếp theo" (hoặc `/ba-workflow:ba-guide`): skill `ba-guide` đọc `ba-workspace`, cho biết đang ở bước nào và lệnh kế tiếp.

## Lệnh
| Bước | Lệnh |
|---|---|
| 1 | `/ba-start intake <path>` |
| 2 | `/ba-start backbone --slug <slug>` |
| 3 | `/ba-collab Tôi nhận module <slug>` |
| 4 | `/ba-start stories --module <slug>` |
| 5a | `/ba-start frd` hoặc `/ba-start srs` (`--module <slug>`) |
| 5b | `/ba-start tests --module <slug>` (test case từ AC, đo độ phủ) |
| 5c | `/ba-start check [--module <slug>]` (nhất quán chéo, lỗi H/M/L) |
| 6a | `/ba-start gate --module <slug>` (PASS / CONDITIONAL / REJECT) |
| 6b | `/ba-collab Gửi module review <slug>` rồi Lead BA: `/ba-collab Duyệt module <slug>` |
| 7 | `/ba-start impact --slug <slug> "<CR>"` |
| 8 | `/ba-start package --slug <slug>` (gói HTML) |
| 9 | `/ba-start export docx --slug <slug>` · `/ba-start export confluence --slug <slug> [--space K --parent ID] [--apply]` |
| định kỳ | `/ba-start retro --slug <slug> [--since 7d]` |
| mọi lúc | `/ba-collab Lưu checkpoint [nhãn]` · `/ba-collab Tiếp tục [slug]` |

## Vòng đời module
`Chưa nhận` -> `Đang soạn` -> `Chờ review` -> `Đã duyệt`; trượt review hoặc có CR thì `Cần sửa`.
Khi `Đã duyệt`, file stories/spec/tests được ghi hash vào `baselines.csv`; hook `guard` hỏi xác nhận trước khi ai đó sửa lại, và `package`/`export` phát hiện file lệch baseline.

## Cấu trúc
```
ba-workspace/<slug>/
  00-intake/   01-backbone/   modules/<module>/{stories,spec,tests,gate-report.md,consistency-report.md,review-packet.md}
  traceability.csv   baselines.csv   events.csv   changes/   checkpoints/   retro/   export/   dist/
plugin: commands/  skills/ba-*  hooks/{hooks.json,guard.py}
```
Quy ước chung (ID, scenario ID, trạng thái, schema traceability, events.csv, severity, từ mơ hồ) nằm ở `skills/ba-conventions`.

## Nâng cấp từ 0.2.0
Story cũ cần scenario ID `[US-nnn/Sn]` trước khi chạy `tests`; `traceability.csv` cũ tự được thêm cột `TC-ID` khi ghi lần đầu.
