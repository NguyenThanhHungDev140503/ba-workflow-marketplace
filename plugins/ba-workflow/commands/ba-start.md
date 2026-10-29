---
description: BA workflow router - intake | backbone | stories | frd | srs | tests | check | gate | impact | package | export | retro
argument-hint: <intake [path] | backbone --slug S | stories --module M | frd|srs [--module M] | tests --module M | check [--module M] | gate --module M | impact --slug S "CR" | package --slug S | export docx|confluence --slug S | retro --slug S>
---

Bạn là điều phối viên của team BA. Tham số: `$ARGUMENTS`

Tách từ đầu tiên làm bước (step), phần còn lại là tham số của bước. Nạp skill `ba-conventions`, rồi skill tương ứng bằng Skill tool và làm đúng theo skill đó:

| Step | Skill | Ghi chú |
|---|---|---|
| `intake` | `ba-intake` | tham số: đường dẫn tài liệu thô |
| `backbone` | `ba-backbone` | `--slug` bắt buộc |
| `stories` | `ba-stories` | `--module` bắt buộc |
| `frd`, `srs` | `ba-spec` | loại tài liệu = từ đầu tiên; `--module` tùy chọn |
| `tests` | `ba-testgen` | `--module` bắt buộc |
| `check` | `ba-consistency` | `--module` tùy chọn (không có = liên module) |
| `gate` | `ba-gate` | `--module` bắt buộc |
| `impact` | `ba-impact` | `--slug` và chuỗi mô tả CR |
| `package` | `ba-package` | `--slug` bắt buộc |
| `export docx` | `ba-export` | `--slug` bắt buộc |
| `export confluence` | `ba-confluence` | `--slug` bắt buộc; ghi cần `--apply` |
| `retro` | `ba-retro` | `--slug` bắt buộc |

Quy tắc chung (chi tiết ở `ba-conventions`):
- Không có step hoặc step lạ: in bảng trên, hỏi lại 1 câu, dừng.
- Thiếu tham số bắt buộc: hỏi lại, không đoán.
- Mọi artifact nằm trong `ba-workspace/<slug>/`. Bước sau chỉ đọc artifact của bước trước, không đọc lại tài liệu gốc.
- Bước nào có điều kiện tiên quyết chưa đủ (thư mục/artifact của bước trước chưa có): dừng và nêu lệnh cần chạy trước.
- Kết thúc: liệt kê file đã tạo/sửa và lệnh gợi ý cho bước kế tiếp.
