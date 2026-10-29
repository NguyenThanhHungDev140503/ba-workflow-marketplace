---
name: ba-export
description: Bước 9 của workflow BA - xuất FRD/SRS/stories ra file DOCX bàn giao cho khách hàng (pandoc), có lint trước. Dùng khi chạy /ba-start export docx.
---

# Export DOCX

Nạp skill `ba-conventions` trước. Tham số: `docx --slug <slug>` (bắt buộc), tùy chọn `--module <slug>` (không có thì mọi module), `--doc frd|srs|stories|all` (mặc định `all`). Ghi vào `ba-workspace/<slug>/export/`. Chỉ xuất ra file cục bộ; không gửi đi đâu.

## Cổng bàn giao
Áp dụng đúng phần "Trước khi đóng gói" của `ba-package` (module chưa `Đã duyệt`, file lệch baseline, ID mồ côi, câu hỏi tồn đọng). Module chưa duyệt chỉ xuất khi người dùng xác nhận; khi đó đặt `classification: NHÁP` trong metadata và ghi chữ NHÁP ở tiêu đề.

## Các bước
1. **Công cụ**: `command -v pandoc` (bắt buộc), `command -v mmdc` (cần nếu tài liệu có Mermaid). Thiếu `pandoc` thì dừng và nói cách cài.
2. **Lint** trên các file nguồn, mỗi lỗi ghi file:dòng; còn lỗi thì dừng, không xuất:
   - Placeholder: `grep -nE 'TBD|TODO|XXX|FIXME|\{\{'`.
   - Link nội bộ `](...)` trỏ file không tồn tại.
   - Bậc heading nhảy cấp (`#` rồi `###`).
   - Từ mơ hồ không số đo (danh sách ở `ba-conventions`) trong FR/NFR.
3. **Mermaid**: có khối ```` ```mermaid ```` thì cần `mmdc`; render từng khối ra SVG/PNG trong thư mục tạm rồi thay bằng ảnh trong bản sao tạm của nguồn. Không có `mmdc`: dừng và hỏi người dùng cài (`npm i -g @mermaid-js/mermaid-cli`) hoặc đồng ý xuất với sơ đồ là mã (ghi rõ điều này ở đầu tài liệu). Không để mã Mermaid thô mà không báo.
4. **Ghép**: tạo bản sao tạm (ngoài workspace) gồm YAML đầu file `title`, `author`, `version`, `date`, `classification`, rồi nội dung theo thứ tự: tổng quan (`vision-scope.md`) → với mỗi module: stories, FRD, SRS → phụ lục truy vết và tồn đọng. `version` lấy từ version baseline cao nhất của module (không có baseline thì `nháp`). `author` hỏi nếu không rõ.
5. **Build**: `pandoc <file ghép> -o export/<slug>-<doc>-v<version>-<yyyymmdd>.docx --toc --toc-depth=3`, thêm `--reference-doc=export/reference.docx` nếu file đó có (mẫu thương hiệu của khách; không có thì nói đang dùng mẫu mặc định).
6. **Kiểm sau build**: file tồn tại, lớn hơn 10 KB, không có stderr; giải nén `word/document.xml` (`unzip -p`) đếm lại số `US-`/`FR-`/`NFR-` so với nguồn; không còn placeholder nào. Báo đường dẫn và số liệu.

## Ràng buộc
- Sửa trong Markdown rồi xuất lại; sửa tay DOCX sẽ mất ở lần xuất sau, ghi câu này vào báo cáo cuối.
- Ghi `events.csv`: `export` (`docx;<số mục>`).
- Chỉ DOCX. PDF: dùng gói HTML của `ba-package` rồi in ra PDF.
