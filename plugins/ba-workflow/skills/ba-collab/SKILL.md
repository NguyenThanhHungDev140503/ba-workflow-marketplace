---
name: ba-collab
description: Cộng tác nhóm BA - nhận module (ghi owner, tách Git branch), gửi gói review cho Lead BA, Lead BA duyệt module (khóa baseline), lưu/nối checkpoint. Dùng khi chạy /ba-collab.
---

# Collab

Nạp skill `ba-conventions` trước (workspace, trạng thái, baseline). Module slug lấy từ `01-backbone/modules.md`.

## Chế độ claim ("Tôi nhận module [slug]")
1. Module phải tồn tại và `status.md` ghi `Chưa nhận`. Đã có owner thì dừng và báo.
2. Trước khi nhận, kiểm tra người khác đã nhận chưa trên remote (chỉ đọc): `git fetch --prune` rồi `git branch -a --list "*ba/<slug>/<module>*"`. Thấy branch của người khác thì dừng và báo, vì `status.md` chỉ cập nhật khi branch được merge nên không đủ để chặn nhận trùng. Không có remote thì nói rõ là chỉ kiểm tra được cục bộ.
   Workspace (intake, backbone) chưa được commit trên branch gốc thì dừng và nói Lead BA commit trước: branch module tách từ branch hiện tại, nên artifact chưa commit sẽ không có ở nhánh của người khác.
3. Tên người nhận lấy từ `git config user.name`; không có thì hỏi.
4. Là git repo: tạo branch `ba/<slug>/<module>` từ branch hiện tại và checkout. Không phải git repo: bỏ qua và nói rõ.
5. Cập nhật `status.md`: owner, branch, `Đang soạn`, ngày nhận. Ghi `events.csv`: `claim` (tên người nhận) và `status` (`Chưa nhận>Đang soạn`).
6. Tạo `modules/<module>/` với `stories/`, `spec/`, `notes.md`.
7. Một commit cục bộ cho thay đổi trên. Không push.

## Chế độ review packet ("Gửi module review [slug]")
1. Cần `modules/<module>/gate-report.md` mới nhất. Chưa có thì dừng, gợi ý `/ba-start gate --module <module>`. Verdict `REJECT` thì dừng, không gửi.
2. Tạo `modules/<module>/review-packet.md`: tóm tắt module (<= 10 dòng), danh sách artifact kèm đường dẫn, verdict + bảng điểm từ gate-report, câu hỏi mở còn lại, rủi ro, quyết định cần Lead BA chốt. Lỗi còn tồn tại thì ghi nguyên, không che.
3. Đổi trạng thái thành `Chờ review` (ghi `events.csv`: `status`, `Đang soạn>Chờ review`).
4. Không tự gửi tin hay push. In packet và hỏi người dùng muốn gửi qua kênh nào.

## Chế độ duyệt ("Duyệt module [slug]") - dành cho Lead BA
1. Module phải ở `Chờ review` và có gate-report `PASS`, hoặc `CONDITIONAL` mà người duyệt nêu rõ chấp nhận các lỗi còn lại (ghi vào `review-packet.md`).
2. Hỏi tên người duyệt, xác nhận một lần rồi mới làm tiếp.
3. Với mọi file trong `modules/<module>/stories/`, `spec/` và `tests/`: tính `sha256sum`, thêm dòng vào `baselines.csv` (version 1, hoặc version kế nếu đã có).
4. Đổi trạng thái thành `Đã duyệt` (ghi `events.csv`: `status`, `Chờ review>Đã duyệt`). Một commit cục bộ. Không push.
5. Cần sửa lại: đổi trạng thái `Cần sửa` kèm lý do trong `notes.md` (ghi `events.csv`: `status`, `<từ>Cần sửa`).

## Chế độ checkpoint ("Lưu checkpoint [nhãn]", "Tiếp tục [slug]")
Nạp skill `ba-checkpoint` và làm theo.

## Kiểm tra trước khi báo xong
Trạng thái trong `status.md` đúng một trong các giá trị chuẩn; branch/commit khớp những gì đã nói; không có lệnh ghi remote nào đã chạy.
