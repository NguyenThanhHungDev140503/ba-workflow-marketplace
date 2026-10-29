---
name: ba-consistency
description: Bước 5c của workflow BA - kiểm tra nhất quán chéo giữa story, FRD/SRS (endpoint, thực thể) và giữa các module, phân loại lỗi H/M/L. Dùng khi chạy /ba-start check.
---

# Consistency

Nạp skill `ba-conventions` trước. Tham số: `--module <slug>` (một module) hoặc không có (liên module). Chỉ đọc, chỉ ghi báo cáo; không tự sửa artifact. Thiếu stories thì dừng; thiếu SRS thì chỉ chạy phần (a), (d), (e) và nói rõ.

## Kiểm tra mỗi module
- (a) US ↔ FR hai chiều: US không có FR (M); FR không trỏ US nào (M).
- (b) FR ↔ endpoint trong SRS: FR cần API mà SRS không có (M); endpoint không FR nào dùng (M).
- (c) Trường request/response ↔ thuộc tính thực thể trong ER: trường không có thuộc tính (M); kiểu dữ liệu khác nhau (H).
- (d) Cùng một quy tắc/số liệu ở story, FR, NFR, TC: giá trị khác nhau (H).
- (e) Thuật ngữ so với `glossary.md`: một khái niệm hai tên gọi (L); thuật ngữ không có trong glossary (L).

## Kiểm tra liên module (`check` không `--module`)
- Thực thể xuất hiện ở nhiều module nhưng thuộc tính/kiểu khác nhau (H).
- Phụ thuộc khai trong `modules.md` mà spec không dùng, hoặc spec dùng module không khai (M).
- BR xung đột giữa hai module (H).
- Module có trạng thái khác nhau nhưng phụ thuộc lẫn nhau, vd module `Đã duyệt` phụ thuộc module `Đang soạn` (M).

## Quy trình
1. Kiểm kê artifact từng module (đếm story, FR, endpoint, thực thể bằng lệnh); thiếu artifact nào ghi vào mục "Chưa kiểm được".
2. Đối chiếu từng cặp, mỗi phát hiện ghi file:dòng cả hai phía.
3. **Phản biện, loại false positive** trước khi báo: trường tính toán không cần cột; khác quy ước camelCase/snake_case đã ghi trong spec; phạm vi đã hoãn có Q-ID hoặc ghi "ngoài phạm vi". Mỗi cái loại bỏ ghi lại một dòng kèm lý do.
4. Phát hiện không dẫn được file:dòng thì không ghi.

## Báo cáo
`modules/<module>/consistency-report.md` (hoặc `consistency-report.md` ở gốc workspace cho liên module):
- Bảng tóm tắt: `Kiểm tra | Số mục | Khớp | Lệch | %`.
- Bảng lỗi: `# | Loại | Nguồn | Đích | Lỗi | Severity | Cách sửa`.
- Mục "Đã loại (false positive)" và "Chưa kiểm được".
Ghi `events.csv` dòng `check` với `H;M;L` còn lại. Gợi ý `/ba-start gate --module <slug>`; còn lỗi H thì gate sẽ hạ PASS xuống CONDITIONAL.
