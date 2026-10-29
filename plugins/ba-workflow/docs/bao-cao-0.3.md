# Báo cáo: ba-workflow 0.3.0

## A. Tóm tắt
Cài đặt thiết kế [thiet-ke-0.3.md](thiet-ke-0.3.md): thêm 6 skill (`ba-testgen`, `ba-consistency`, `ba-export`, `ba-confluence`, `ba-retro`, `ba-checkpoint`), tổng 15 skill. Bỏ `ba-jira` theo yêu cầu (team không dùng Jira).

## B. Chi tiết cài đặt
| File | Nội dung / quyết định |
|---|---|
| [ba-conventions/SKILL.md](../skills/ba-conventions/SKILL.md) | Scenario ID `[US-nnn/Sn]`, cột `TC-ID` (7 cột), bảng mã test, thang severity H/M/L, `events.csv` kèm lệnh ghi có sẵn. Một nơi định nghĩa để các skill không lệch nhau |
| [ba-testgen/SKILL.md](../skills/ba-testgen/SKILL.md) | 7 quy tắc sinh TC; giá trị biên chỉ lấy từ số có trong nguồn, thiếu thì ghi Q-ID; độ phủ đo bằng đoạn Python nhúng sẵn, ngưỡng 90% |
| [ba-consistency/SKILL.md](../skills/ba-consistency/SKILL.md) | Kiểm (a)-(e) cho module + kiểm liên module; bước phản biện loại false positive; lỗi không dẫn được file:dòng thì không ghi |
| [ba-gate/SKILL.md](../skills/ba-gate/SKILL.md) | Giữ 6 chiều và trọng số; chỉ hạ PASS xuống CONDITIONAL khi phủ test < 90% hoặc còn lỗi H; báo cáo cũ thì không tính |
| [ba-checkpoint/SKILL.md](../skills/ba-checkpoint/SKILL.md) | Lưu trong workspace (đi theo Git); khi tiếp tục so `sha256` để nêu file đã đổi |
| [ba-export/SKILL.md](../skills/ba-export/SKILL.md) | Lint → (Mermaid qua `mmdc`) → ghép → `pandoc --toc` → kiểm sau build; dùng lại cổng bàn giao của `ba-package` |
| [ba-confluence/SKILL.md](../skills/ba-confluence/SKILL.md) | Plan trước, `--apply` mới ghi; `confluence-map.csv` lưu version để phát hiện sửa tay; không có MCP thì xuất file |
| [ba-retro/SKILL.md](../skills/ba-retro/SKILL.md) | Chỉ số tính từ `events.csv` bằng Python nhúng sẵn; ≤ 3 việc tiếp theo; không đổ lỗi cá nhân |
| collab, impact, package, intake, stories, backbone, router, README | Ghi `events.csv`, băm cả `tests/` khi duyệt, cột ngày cho Q, router thêm `tests`/`check`/`export`/`retro` |

## C. Kiểm thử
Thủ công trong thư mục tạm, chạy chính các đoạn lệnh trích từ SKILL.md:
- Độ phủ test: 3 scenario, 2 có TC → `2 / 3 phủ% 67 thiếu: ['US-001/S3']` (đúng; ô có dấu phẩy quote đúng).
- Retro: 7 sự kiện mẫu → `approved 1`, `pass_rate 50`, `cycle_days_median 5`, `churn m1 = 2` (khớp tính tay).
- Hook `guard`: file `tests/test-cases.csv` đã baseline → trả `ask` đúng.
- `pandoc` md → docx: 10,9 KB, nội dung `US-001` có trong `document.xml`.
- `claude plugin validate`: pass (chỉ cảnh báo thiếu LICENSE/icon, không ảnh hưởng dùng cục bộ).
- Không có test nào fail.

Chưa kiểm: toàn bộ luồng `/ba-start ...` bằng tài liệu thật; `ba-confluence` với Atlassian MCP thật; DOCX có Mermaid (máy chưa có `mmdc`).

## D. Khó khăn
- Atlassian MCP chưa xác thực nên không biết tên tool/định dạng body → skill buộc tra bằng `ToolSearch` lúc chạy và có chế độ file dự phòng.
- Cột `TC-ID` và scenario ID đổi định dạng 0.2.0 → ghi hướng dẫn nâng cấp trong README.

## E. Cải tiến
Không thêm chiều chấm điểm nên gate không phải tính lại trọng số; các phép đếm đều là lệnh chạy được; mọi thao tác ghi ra ngoài đều cần xác nhận.

## F. Công cụ
Markdown/YAML (skill, command), Python 3 (`csv`, `statistics`, hook), `pandoc`, `sha256sum`, `jq`, `claude plugin validate`.
