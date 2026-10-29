---
name: ba-confluence
description: Bước 9 của workflow BA - đẩy gói BA lên Confluence (cây trang theo module) qua Atlassian MCP, hoặc xuất file trang để nhập tay; phát hiện trang bị sửa tay trước khi ghi đè. Dùng khi chạy /ba-start export confluence.
---

# Export Confluence

Nạp skill `ba-conventions` trước. Tham số: `confluence --slug <slug>` (bắt buộc), `--space <KEY>` và `--parent <pageId>` (hỏi nếu thiếu), `--apply` (không có thì chỉ lập plan). Ghi vào `ba-workspace/<slug>/export/`. Áp dụng cổng bàn giao của `ba-package`.

## Kết nối
1. Tìm tool Confluence bằng `ToolSearch` (từ khóa `confluence`) lúc chạy; không đoán tên tool, đọc schema body (markdown hay storage format) rồi chuyển đổi cho khớp.
2. Chưa có tool (Atlassian MCP chưa xác thực): nói người dùng cần `/mcp` để xác thực, và làm **chế độ file**: ghi mỗi trang thành `export/confluence/<tên-trang>.md` kèm `export/confluence-plan.csv` để nhập tay. Không hỏi mã/token trong chat.

## Cây trang
Gốc `<slug> - Gói BA` → mỗi module một trang con (`<module> - Stories`, `<module> - FRD`, `<module> - SRS`, `<module> - Test` nếu có) + `Truy vết` + `Tồn đọng`. Mermaid: đính kèm SVG nếu có `mmdc`, không thì khối mã. Footer mỗi trang: `Tạo bởi ba-workflow, baseline v<n>, <ngày>`. Nhãn: `ba-workflow`, loại tài liệu, `v<n>`.

## Plan trước, ghi sau
1. Kiểm tra `space` và `parent` tồn tại. Tìm từng tiêu đề trong space (CQL `type=page AND space="<KEY>" AND title="<tiêu đề>"`): có rồi thì `cập nhật`, chưa thì `tạo`.
2. Lint mọi trang: không `TBD|TODO|XXX|FIXME|{{`; nội dung hợp lệ với định dạng body.
3. Ghi `export/confluence-plan.csv` (`trang,hành động,page_id,lý do`), in cho người dùng, **hỏi xác nhận đúng số trang** trước khi ghi. Không `--apply` thì dừng ở đây.

## Phát hiện sửa tay (`export/confluence-map.csv`)
Cột `trang,page_id,version_đã_đẩy,sha_nội_dung`. Trước khi cập nhật trang đã có trong map: lấy version hiện tại của trang; khác `version_đã_đẩy` nghĩa là có người sửa trên Confluence. **Dừng ở trang đó**, cho xem khác biệt và hỏi: ghi đè / gộp tay / bỏ qua. Không ghi đè im lặng.

## Ghi
- Dừng ở lỗi đầu tiên; trang nào xong đã nằm trong map nên chạy lại thì tiếp tục, không tạo trùng.
- Không xóa trang, không đổi quyền, không đặt trang ở space khác.
- Sau khi ghi, đọc lại trang đã tạo: không có chuỗi `Unknown macro`/`Error rendering`.
- Báo `Đã tạo / Đã cập nhật / Bỏ qua / Lỗi` kèm link; ghi `events.csv`: `export` (`confluence;<số trang>`).
