---
name: ba-flow
description: Bước 5a' của workflow BA - vẽ luồng chi tiết của một module (swimlane theo actor, nhánh lỗi, điểm gọi module khác) bằng Mermaid, gắn từng bước với scenario/FR và đo độ phủ. Dùng khi chạy /ba-start flow --module.
---

# Flow chi tiết module

Nạp skill `ba-conventions` trước. Tham số: `--module <slug>` (bắt buộc, hỏi nếu thiếu). Đầu vào: `modules/<module>/stories/` và `spec/frd.md` (thiếu một trong hai thì dừng, gợi ý `stories`/`frd`); `process-flows.md` và `modules.md` để biết điểm vào/ra và module phụ thuộc. Module `Đã duyệt` thì dừng: sửa phải đi qua `/ba-start impact`. Khác `process-flows.md` (mức dự án): file này là mức module, từng bước thao tác.

## Ghi `modules/<module>/spec/flows.md`
Mỗi quy trình trong module gồm:
1. **Luồng chính**: Mermaid `flowchart` có `subgraph` theo actor (Nhân viên, Quản lý, Hệ thống...) hoặc `sequenceDiagram` khi trao đổi nhiều bên. Mỗi bước có nhãn ID nguồn: `[US-001/S1]`, `[FR-005]`.
2. **Nhánh lỗi/ngoại lệ**: từ chối, thiếu quyền, dữ liệu sai, quá hạn, xung đột trạng thái. Vẽ trong cùng sơ đồ hoặc sơ đồ riêng; mỗi nhánh là một scenario `error`/`edge` có ID.
3. **Điểm tích hợp**: bước gọi sang module khác ghi `→ <module>` kèm FR; module đích phải có trong phần phụ thuộc của `modules.md` (không có thì ghi vào `open-questions.md`).
4. **Bảng chú giải**: `Bước | Actor | Mô tả | Nguồn (US/FR) | Trạng thái sau bước`.

## Ràng buộc
- Không thêm bước, vai trò hay quy tắc mà story/FRD không có. Chỗ luồng thiếu thông tin (vd hủy đơn đã duyệt) thì vẽ một nút `? Q-xxx` và ghi Q, không đoán.
- Trạng thái sau bước phải khớp state diagram trong `frd.md`; lệch thì ghi vào bảng lỗi, không tự sửa FRD.
- Giữ mỗi sơ đồ vừa đọc được (khoảng 15 nút); quá lớn thì tách theo quy trình con.
- Mermaid phải hợp lệ cú pháp; có `mmdc` thì thử render để bắt lỗi, không có thì rà bằng mắt và nói rõ chưa render.

## Độ phủ (đo bằng lệnh; mọi scenario và FR phải xuất hiện trong ít nhất một sơ đồ)
Chạy từ gốc workspace, thay `M`:

```
python3 - <<'EOF'
import glob, re
M = "modules/M"
rd = lambda f: open(f, encoding="utf-8").read()
need = set()
for f in glob.glob(f"{M}/stories/US-*.md"):
    need |= set(re.findall(r"\[(US-\d+/S\d+)\]", rd(f)))
need |= set(re.findall(r"^\| (FR-\d+) \|", rd(f"{M}/spec/frd.md"), re.M))
have = set(re.findall(r"US-\d+/S\d+|FR-\d+", rd(f"{M}/spec/flows.md"))) & need
print(len(have), "/", len(need), "phủ%", round(100 * len(have) / len(need)) if need else 0, "thiếu:", sorted(need - have))
EOF
```

Thiếu thì vẽ bổ sung hoặc giải thích vì sao không có luồng (vd FR thuần dữ liệu), ghi vào `flows.md` mục "Không vẽ". Ghi `events.csv`: `flow` (`phủ%;số sơ đồ`).

## Kiểm tra trước khi báo xong
Phủ 100% hoặc mọi mục thiếu đã giải thích; mọi nhánh lỗi có scenario ID; mọi nút `?` có Q-ID. Gợi ý `/ba-start tests --module <slug>` (TC `ST` lấy từ chuyển trạng thái trong luồng) rồi `check`/`gate`.
