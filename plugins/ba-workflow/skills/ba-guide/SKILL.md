---
name: ba-guide
description: Hướng dẫn và điều hướng workflow BA. Dùng khi người dùng hỏi về plugin/workflow BA, "dùng plugin BA", "bắt đầu dự án BA", "làm gì tiếp theo", "đang ở bước nào" - đọc trạng thái ba-workspace rồi chỉ ra bước kế tiếp.
---

# Hướng dẫn workflow BA

Nạp skill `ba-conventions` trước. Mục tiêu: xác định đang ở đâu trong workflow rồi chỉ **đúng một bước kế tiếp**, không giảng cả quy trình trừ khi người dùng hỏi tổng quan. Hỏi xác nhận trước khi chạy bước; không tự chạy bước ghi ra ngoài (push, Confluence).

## 1. Đọc trạng thái (chỉ đọc, bằng lệnh)
- `ls ba-workspace/`; có nhiều dự án thì hỏi, một dự án thì dùng nó.
- `01-backbone/status.md`, `open-questions.md` (đếm Q `Mở, chặn`), `baselines.csv`, `events.csv` (dòng cuối), `git branch --show-current` (dạng `ba/<slug>/<module>` cho biết module đang làm), `git config user.name`.
- Chưa rõ vai trò (BA hay Lead BA) thì hỏi một câu.

## 2. Chọn bước kế tiếp (lấy điều kiện đầu tiên đúng)
| Trạng thái | Việc kế tiếp |
|---|---|
| Không có `ba-workspace/` | Hỏi đường dẫn tài liệu thô -> `/ba-start intake <path>` |
| Có `00-intake`, chưa có `01-backbone` | Nhắc số Q chặn; `/ba-start backbone --slug <slug>` |
| Có backbone, workspace chưa commit | Lead BA commit workspace trước khi BA nhận module |
| BA chưa có branch module | Liệt kê module `Chưa nhận` -> `/ba-collab Tôi nhận module <slug>` |
| Module `Đang soạn` hoặc `Cần sửa`, thiếu stories | `/ba-start stories --module <m>` |
| ... có stories, thiếu `spec/` | `/ba-start frd --module <m>` rồi `srs` |
| ... có spec, thiếu `tests/` | `/ba-start tests --module <m>` |
| ... có tests, chưa có hoặc cũ `consistency-report.md` | `/ba-start check --module <m>` |
| ... chưa có hoặc cũ `gate-report.md` | `/ba-start gate --module <m>` |
| Gate `REJECT` | Sửa theo bảng lỗi trong gate-report rồi chạy lại gate |
| Gate `PASS`/`CONDITIONAL`, module chưa `Chờ review` | `/ba-collab Gửi module review <m>` |
| Module `Chờ review` (Lead BA) | `/ba-collab Duyệt module <m>` |
| Mọi module `Đã duyệt` | `/ba-start package --slug <slug>`, `export docx`, `export confluence` |
| Khách đổi yêu cầu | `/ba-start impact --slug <slug> "<CR>"` |
| Dừng giữa chừng / đổi người | `/ba-collab Lưu checkpoint` / `Tiếp tục` |
| Cuối kỳ | `/ba-start retro --slug <slug>` |

"Cũ" nghĩa là có file nguồn (stories/spec) sửa sau báo cáo; so thời gian sửa file.

## 3. Trả lời
Ngắn: (1) đang ở bước nào (một dòng, kèm số liệu: module, trạng thái, Q chặn); (2) bước kế tiếp với lệnh chính xác; (3) hỏi có chạy luôn không. Người dùng hỏi tổng quan thì mới đưa bảng vòng đời: `Chưa nhận -> Đang soạn -> Chờ review -> Đã duyệt` (hoặc `Cần sửa`) và hai vai Lead BA / BA, trỏ tới README của plugin.
