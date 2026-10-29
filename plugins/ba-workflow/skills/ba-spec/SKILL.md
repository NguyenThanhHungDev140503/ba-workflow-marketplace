---
name: ba-spec
description: Bước 5 của workflow BA - biên dịch story thành FRD (đặc tả nghiệp vụ) hoặc SRS (đặc tả kỹ thuật cho dev). Dùng khi chạy /ba-start frd hoặc /ba-start srs.
---

# FRD & SRS

Nạp skill `ba-conventions` trước. Tham số: `frd` hoặc `srs`, kèm `--module <slug>` (không có thì áp dụng cho các module đã có stories). Đầu vào là stories và backbone; thiếu stories thì dừng. Module `Đã duyệt` thì dừng: sửa phải đi qua `/ba-start impact`.

## FRD -> `modules/<module>/spec/frd.md`
- Tổng quan module, actor, điều kiện tiên quyết.
- Yêu cầu chức năng `FR-xxx`, mỗi FR trỏ về US và BR.
- Quy tắc nghiệp vụ (bảng quyết định nếu có nhiều điều kiện), vòng đời trạng thái (Mermaid state diagram nếu có).
- Báo cáo/biểu mẫu đầu ra, phân quyền theo vai trò.

## SRS -> `modules/<module>/spec/srs.md`
Chưa có `frd.md` thì tạo FRD trước (SRS dựa trên FRD), nói rõ với người dùng.
- Mọi nội dung FRD ở dạng kiểm chứng được cho dev: dữ liệu vào/ra, validation, thông báo lỗi.
- Mô hình dữ liệu mức logic (thực thể, thuộc tính, quan hệ; Mermaid ER).
- Hợp đồng API ở mức endpoint, request/response, mã lỗi (không dựng code).
- Yêu cầu phi chức năng `NFR-xxx` có số đo: hiệu năng, bảo mật, audit log, khả năng dùng offline nếu liên quan.
- Ma trận truy vết FR/NFR -> US -> BR.

## Ràng buộc
- Không thêm yêu cầu mới ngoài story. Thấy thiếu thì ghi vào open-questions.
- Mỗi FR/NFR kiểm chứng được. Từ mơ hồ (xem `ba-conventions`) không được xuất hiện nếu không có số.
- NFR mà nguồn không có số: ghi `NFR-xxx` kèm Q-ID đòi số, không tự đặt con số.
- Cập nhật `traceability.csv` theo `ba-conventions` (điền `FR-ID`/`NFR-ID`).
- Báo cuối: số FR, số NFR, số FR không truy ngược được (phải 0). Gợi ý `/ba-start gate --module <slug>`.
