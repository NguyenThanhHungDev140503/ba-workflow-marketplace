---
name: ba-impact
description: Bước 7 của workflow BA - phân tích ảnh hưởng khi khách hàng đổi yêu cầu (change request). Dùng khi chạy /ba-start impact --slug "[CR]".
---

# Impact

Nạp skill `ba-conventions` trước. Tham số: `--slug <slug>` và chuỗi mô tả CR trong dấu nháy.

## Cách làm
1. Đọc `traceability.csv`, `modules.md`, `status.md`, `baselines.csv`, stories và spec liên quan.
2. Xác định điểm chạm: từ khóa/khái niệm trong CR -> BR, US, FR, NFR bị ảnh hưởng, rồi lan sang module phụ thuộc (đi theo chuỗi trong `traceability.csv`, không chỉ theo từ khóa).
3. Kiểm tra ngược: artifact nào đã `Chờ review`, `Đã duyệt` hoặc có trong `baselines.csv` sẽ phải mở lại; đánh dấu riêng.
4. Tạo `ba-workspace/<slug>/changes/CR-<nnn>.md` (nnn = số kế tiếp trong `changes/`):
   - Mô tả thay đổi (nguyên văn + diễn giải).
   - Bảng ảnh hưởng: `Artifact | Loại (trực tiếp/lan truyền) | Đã duyệt? | Việc phải sửa | Owner`. Gồm cả test case bị ảnh hưởng (theo cột `TC-ID`) và trang Confluence đã đẩy (theo `export/confluence-map.csv`) cần cập nhật lại.
   - Ảnh hưởng tới code/API/DB đã có (nếu repo được cung cấp, chỉ liệt kê vùng chạm, không sửa code).
   - Rủi ro, ước lượng mức công việc (S/M/L) kèm lý do.
   - Tùy chọn: làm toàn bộ / làm một phần / hoãn, kèm đánh đổi.
   - Quyết định cần ai chốt.
5. Không tự sửa spec. Chỉ sửa sau khi người dùng chọn phương án; khi đó:
   - đổi các module bị ảnh hưởng sang `Cần sửa` trong `status.md`, ghi `events.csv` (`cr` với `CR-nnn`, `status` với `Đã duyệt>Cần sửa` hoặc trạng thái cũ tương ứng);
   - cập nhật artifact (hook sẽ hỏi xác nhận với file đã duyệt: đây là việc đúng, xác nhận một lần cho CR này);
   - ghi vào `changes/changelog.md`;
   - module phải đi lại gate -> review -> `Duyệt module` để có baseline version mới.

## Ràng buộc
- Ảnh hưởng nào chỉ là phỏng đoán thì ghi `[chưa xác minh]`.
- CR trùng hoặc mâu thuẫn với CR trước: nêu rõ ID.
- Thiếu `traceability.csv` hoặc chuỗi truy vết đứt: nói rõ phần nào phân tích bằng từ khóa, không bằng chuỗi.
