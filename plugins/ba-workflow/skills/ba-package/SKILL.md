---
name: ba-package
description: Bước 8 của workflow BA - đóng gói toàn bộ sản phẩm BA của một dự án thành một file HTML tự chứa để bàn giao. Dùng khi chạy /ba-start package --slug.
---

# Package

Nạp skill `ba-conventions` trước. Đầu vào: `ba-workspace/<slug>/`. Đầu ra: `ba-workspace/<slug>/dist/<slug>-ba-package.html`.

## Trước khi đóng gói (gate; `ba-export` và `ba-confluence` dùng lại đúng phần này)
1. Mọi module trong `status.md` phải `Đã duyệt`. Module chưa duyệt: liệt kê và hỏi có đóng gói bản nháp không (đánh dấu "NHÁP" trên đầu trang và cạnh module đó).
2. Với mỗi file trong `baselines.csv`: so `sha256sum` hiện tại với dòng mới nhất. Lệch nghĩa là file bị sửa sau khi duyệt: liệt kê, coi module đó là chưa duyệt.
3. `traceability.csv` không có ID mồ côi (US/FR/NFR không truy ngược được tới RAW/BR). Kiểm bằng lệnh.
4. Open-questions còn mở: liệt kê thành phụ lục "Tồn đọng".

## Nội dung file HTML
- Mục lục cố định bên trái, tìm kiếm theo ID (US-, FR-, BR-...).
- Các phần: tổng quan và phạm vi, module, stories + Gherkin, FRD/SRS, test case (`tests/test-cases.csv`, nếu có), ma trận truy vết, báo cáo nhất quán (nếu có), câu hỏi còn mở, lịch sử thay đổi (CR).
- Một file, in ra PDF được, mở offline được.
- Mermaid: nếu có `mmdc` thì render sẵn thành SVG nhúng vào; không có thì giữ khối mã Mermaid kèm dòng chú thích "sơ đồ, cần Mermaid để vẽ" và nói rõ với người dùng. Không nhúng link CDN rồi gọi là offline.

## Cách làm
Ghép Markdown vào một file tạm (ngoài workspace) rồi chuyển bằng `pandoc -s --toc --embed-resources` (cũng là công cụ của `ba-export`; đã thử chạy được, ra một file HTML tự chứa). Không có `pandoc` mới dùng Python + `markdown` (kiểm tra đã cài; chưa có thì hỏi trước khi cài). Mục lục tìm theo ID cần thêm script nhỏ ngoài `pandoc`; nếu bỏ qua, nói rõ. Chạy, đọc lại file kết quả và đếm số mục (US, FR, BR, câu hỏi mở) đối chiếu với nguồn, rồi báo đường dẫn. Không gửi đi đâu.
