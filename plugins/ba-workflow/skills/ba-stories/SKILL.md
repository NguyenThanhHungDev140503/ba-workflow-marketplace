---
name: ba-stories
description: Bước 4 của workflow BA - sinh User Story và kịch bản Gherkin cho một module. Dùng khi chạy /ba-start stories --module.
---

# Stories

Nạp skill `ba-conventions` trước. Đầu vào: `01-backbone/modules.md` và các RAW/BR của module `--module`. Thiếu `--module` thì hỏi. Module chưa có owner (`Chưa nhận`) thì cảnh báo và gợi ý `/ba-collab Tôi nhận module <slug>` trước. Module `Đã duyệt` thì dừng: sửa phải đi qua `/ba-start impact`.

## Trước khi viết
Đọc `00-intake/open-questions.md`. Liệt kê các câu `chặn bước stories` thuộc module này. Còn câu chưa đóng thì báo người dùng và hỏi: chờ trả lời, hay viết story ở dạng nháp với giả định ghi rõ (đánh dấu `[giả định: Q-xxx]` trong từng scenario liên quan).

## Tạo trong `ba-workspace/<slug>/modules/<module>/stories/`
Mỗi story một file `US-xxx-<tên-ngắn>.md`:

```
# US-012 <tiêu đề>
Là <actor>, tôi muốn <hành động>, để <giá trị>.
Nguồn: RAW-007, BR-002
Ưu tiên: Must | Should | Could

## Acceptance Criteria
Feature: <tên>
  Scenario: [US-012/S1] <happy path>
    Given ...
    When ...
    Then ...
  Scenario: [US-012/S2] <edge case>
  Scenario: [US-012/S3] <error / không đủ quyền / dữ liệu sai>
```

Scenario ID đánh liên tục `S1, S2...` trong từng story, không đánh lại khi xóa/thêm (xem `ba-conventions`).

Kèm `stories-index.md` liệt kê US, ưu tiên, nguồn.

## Ràng buộc
- Tối thiểu 3 scenario mỗi story: happy, edge, error.
- Story theo INVEST. Story quá lớn thì tách, ghi lý do.
- Gherkin viết ở mức hành vi nghiệp vụ, không nhắc tên nút, bảng DB, API.
- Quy tắc nghiệp vụ có số liệu (làm tròn, hạn mức, trạng thái) phải nêu số cụ thể; nguồn không có số thì ghi vào open-questions, không tự đặt.
- Hành động có phân quyền thì phải có scenario "không đủ quyền", kể cả khi chỉ có một vai trò chính.
- Cập nhật `traceability.csv` theo `ba-conventions` (thêm dòng có `US-ID`).

## Kiểm tra trước khi báo xong
Đếm bằng lệnh: số story, số story có < 3 scenario (phải 0), số scenario thiếu ID (phải 0), số từ mơ hồ còn sót. Gợi ý `/ba-start frd --module <slug>` hoặc `/ba-start tests --module <slug>`.
