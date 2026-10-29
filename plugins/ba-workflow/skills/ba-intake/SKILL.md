---
name: ba-intake
description: Bước 1 của workflow BA - bóc tách yêu cầu thô (email, biên bản họp, SRS cũ, ghi chú) thành danh sách yêu cầu có cấu trúc. Dùng khi chạy /ba-start intake.
---

# Intake

Nạp skill `ba-conventions` trước. Đầu vào: đường dẫn file hoặc thư mục tài liệu thô. Nếu không có path, hỏi người dùng.

## Việc cần làm
1. Đọc toàn bộ nguồn. Với file không đọc được trực tiếp (docx, pdf, xlsx), chuyển sang text trước.
2. `<slug>`: hỏi người dùng hoặc đề xuất từ tên dự án (kebab-case).
   - `ba-workspace/<slug>/00-intake/` đã có nội dung: không ghi đè. Hỏi chạy bổ sung (thêm RAW/Q mới, đánh tiếp số, giữ ID cũ) hay dừng.
3. Rút ra và ghi vào `ba-workspace/<slug>/00-intake/`:
   - `raw-requirements.md`: bảng `ID | Yêu cầu (theo nguồn) | Nguồn (file + vị trí) | Ghi chú`, ID `RAW-001...`, mỗi ý của nguồn một dòng.
   - `stakeholders.md`: ai, vai trò, quan tâm gì, ai quyết định. Có mục ghi người dùng cuối nào chưa được hỏi ý kiến.
   - `glossary.md`: thuật ngữ nghiệp vụ gặp trong nguồn, giữ đúng cách gọi của khách hàng, cột "cần xác nhận".
   - `open-questions.md`: bảng `ID | Câu hỏi | Liên quan RAW | Hỏi ai | Trạng thái | Ngày mở | Ngày đóng` (ngày dạng `YYYY-MM-DD`, ngày đóng để trống đến khi có câu trả lời). Mâu thuẫn, mơ hồ, thông tin thiếu, ngoài ra có câu hỏi về phạm vi (áp dụng cho đơn vị/địa điểm nào).

## Ràng buộc
- Chỉ chép lại điều nguồn nói. Suy luận của bạn đánh dấu `[suy luận]`.
- Từ mơ hồ (danh sách ở `ba-conventions`) vẫn ghi RAW đúng nguyên văn, nhưng cột Ghi chú trỏ tới một Q-ID đòi số đo cụ thể. Không tự đặt con số.
- Nguồn tự mâu thuẫn (hai người nói hai mức khác nhau): ghi cả hai vế kèm tên người nói vào cùng một Q, không chọn bên nào.
- Câu hỏi mà trả lời sẽ làm đổi story hoặc spec (mức ngưỡng, quy tắc tính, phạm vi) gắn nhãn `Mở, chặn bước stories` trong cột Trạng thái. Bước `stories` phải nhắc các câu này trước khi viết.
- Kiểm tra độ phủ trước khi kết thúc: mỗi ý trong nguồn có ít nhất một RAW, mỗi Q liên quan ít nhất một RAW hoặc ghi "toàn bộ". Đếm bằng lệnh, không ước chừng.
- Mỗi Q mới ghi một dòng `q-open` vào `events.csv` (xem `ba-conventions`; cột `module` là `-` ở bước intake, hoặc tên module khi Q phát sinh từ một module). Bước nào đóng Q thì điền `Ngày đóng` và ghi `q-close`.
- Cuối cùng báo số yêu cầu, số câu hỏi mở, số câu đang chặn, và gợi ý `/ba-start backbone --slug <slug>`.
