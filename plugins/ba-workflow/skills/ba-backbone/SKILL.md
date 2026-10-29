---
name: ba-backbone
description: Bước 2 của workflow BA - dựng cấu trúc cốt lõi dự án (mục tiêu, phạm vi, module, actor, luồng chính) từ kết quả intake. Dùng khi chạy /ba-start backbone --slug.
---

# Backbone

Nạp skill `ba-conventions` trước. Đầu vào: `ba-workspace/<slug>/00-intake/`. Thiếu thư mục này thì dừng và gợi ý chạy intake. `01-backbone/` đã có nội dung thì không ghi đè: hỏi cập nhật hay dừng.

## Tạo trong `ba-workspace/<slug>/01-backbone/`
- `vision-scope.md`: mục tiêu nghiệp vụ (BR-001...), in-scope, out-of-scope, giả định, ràng buộc.
- `modules.md`: danh sách module, mỗi module có `slug`, mô tả 1-2 câu, actor chính, các RAW-ID thuộc về nó, phụ thuộc module khác. Đây là danh sách để thành viên "nhận module".
- `actors.md`: actor/vai trò và quyền ở mức nghiệp vụ.
- `process-flows.md`: luồng chính dạng Mermaid (flowchart hoặc sequence), một luồng mỗi quy trình lớn.
- `status.md`: bảng theo `ba-conventions`, mỗi module một dòng, trạng thái `Chưa nhận`, owner/branch để trống.
- `ba-workspace/<slug>/traceability.csv`: theo schema trong `ba-conventions`, một dòng `RAW,BR,module,,,,` (7 cột) cho mỗi liên kết. Mọi RAW-ID phải map vào một module hoặc `OUT-OF-SCOPE`.

## Ràng buộc
- Ranh giới module theo nghiệp vụ, tránh cắt theo màn hình.
- Không tách module quá nhỏ: mục tiêu là mỗi module một BA nhận được trong vài ngày.
- Phụ thuộc giữa module không được vòng tròn; có vòng thì gộp hoặc cắt lại và nói rõ.
- RAW/BR toàn hệ thống (phi chức năng, ràng buộc chung) ghi `module=ALL`; chọn đúng một module làm `(chủ NFR)` trong `modules.md` để chứa NFR của chúng.
- RAW-ID nào chưa xếp được thì liệt kê ở cuối `modules.md` mục "Chưa phân loại" và hỏi người dùng.
- Kiểm tra bằng lệnh: số RAW trong `raw-requirements.md` = số RAW duy nhất trong `traceability.csv`.
- Gợi ý bước kế: `/ba-collab Tôi nhận module <slug>`.
