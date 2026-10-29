# Kết quả chạy thử (2026-10-29)

Cách chạy: Claude chạy thủ công từng skill trong phiên này, trên thư mục thử `scratchpad/e2e` (git repo, tài liệu `yeu-cau-mau.md`), làm đúng văn bản SKILL.md. Riêng bước `intake` được chạy bằng `claude -p /ba-workflow:ba-start intake ...` (lệnh thật). Các lần chạy `claude -p` tiếp theo bị trình phân loại quyền chặn nên phần còn lại chạy trong phiên này. Đây là **mô phỏng bằng chính Claude**, không thay thế việc bạn chạy `/ba-start` trong phiên riêng.

## Đạt
| Nhóm | Kết quả |
|---|---|
| Intake (lệnh thật) | 20 RAW từ 11 ý; Q-002 ghi cả hai vế Lan/Minh; "nhanh/dễ dùng/ổn định/nhiều/không nhiều" đều thành Q, không tự đặt số; 6 Q `Mở, chặn`; `events.csv` có `q-open` |
| Backbone | 3 module theo nghiệp vụ; 20 RAW = 20 RAW trong `traceability.csv` |
| Claim | branch `ba/nghi-phep/don-nghi-phep`, `status.md`, `events.csv`, 1 commit cục bộ |
| Stories | 4 story, mỗi story ≥ 3 scenario có ID, có scenario "không đủ quyền", nhắc Q chặn bằng `[giả định: Q-xxx]` |
| Spec | FRD 10 FR, SRS có ER/API/NFR; NFR không số được gắn `chờ Q-xxx` |
| Tests | 15 TC, độ phủ 14/14 = 100%, TC phụ thuộc Q có `[chờ Q-xxx]` |
| Check | M=3, L=1, có mục "Đã loại" và "Chưa kiểm được" |
| Gate | CONDITIONAL 75.8 (còn Q chặn nên không thể PASS) |
| Duyệt + baseline | 9 file có hash; `package` kiểm lệch hash = 0, ID mồ côi = 0 |
| Impact | `CR-001` có bảng ảnh hưởng, cột "Đã duyệt?", `[chưa xác minh]`, không tự sửa spec |
| Package | HTML 27 KB (pandoc), số US/FR/BR khớp nguồn |
| Retro | `approved 1, CONDITIONAL 1, churn 1` khớp `events.csv` |
| Checkpoint | lưu có hash; sửa 1 file rồi kiểm lại, đúng file đó báo FAILED |

## Lỗi/thiếu đã tìm thấy và đã sửa
1. Python `csv` mặc định CRLF, lẫn với dòng `echo` (Git báo đổi dòng) -> bắt buộc `lineterminator="\n"` (`ba-conventions`).
2. RAW phi chức năng toàn hệ thống không có module để gắn -> thêm `module=ALL` và "module chủ NFR" (`ba-conventions`, `ba-backbone`).
3. `events.csv` ghi `00-intake` vào cột module -> dùng `-` cho sự kiện không thuộc module.
4. Gate chiều 3 phạt dòng NFR đã ghi `chờ Q-xxx` (phạt hai lần với chiều 6) -> miễn ở chiều 3.
5. Claim: artifact intake/backbone chưa commit thì nhánh người khác không có -> yêu cầu Lead BA commit trước.
6. Package dựa vào Python `markdown` (máy không có) -> ưu tiên `pandoc`, đã chạy được.

## Chưa kiểm được
- **Hook `guard` trong phiên có quyền**: hook **có được gọi** (log tạm xác nhận) và khi chạy tay trả đúng `ask`, nhưng phiên này chạy chế độ quyền tự động nên việc sửa file đã baseline không hiện hộp hỏi. Cần bạn thử trong phiên thường (nhờ Claude sửa 1 file đã duyệt).
- Không chạy: REJECT khi xóa scenario, nhận module lần hai, chạy lại intake (không ghi đè), `stories` trên module đã duyệt, `export docx` (Mermaid có trong spec, máy không có `mmdc` nên đúng quy trình là dừng và hỏi), `ba-confluence`.
- Hầu hết là Claude làm theo văn bản skill, nên độ hiểu đúng của một phiên chạy `/ba-start` độc lập vẫn chưa chứng minh.
