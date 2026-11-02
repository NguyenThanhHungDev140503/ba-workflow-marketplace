---
name: ba-flow
description: Bước 5a' của workflow BA - vẽ bộ diagram hành vi của một module cho team code (luồng swimlane, máy trạng thái, sơ đồ trình tự) bằng Mermaid, chỉ vẽ loại đủ điều kiện, gắn ID nguồn và đo độ phủ. Dùng khi chạy /ba-start flow --module.
---

# Diagram hành vi của module

Nạp skill `ba-conventions` trước (mục "Bộ diagram": loại, điều kiện, giới hạn, quy ước nhãn). Tham số: `--module <slug>` (bắt buộc, hỏi nếu thiếu). Đầu vào: `modules/<module>/stories/` và `spec/frd.md` (thiếu một trong hai thì dừng, gợi ý `stories`/`frd`); `01-backbone/modules.md`; `spec/srs.md` nếu có (D3 cần bảng API). Module `Đã duyệt` thì dừng: sửa phải đi qua `/ba-start impact`. Khác `process-flows.md` (mức dự án): file này là mức module.

## Ghi `modules/<module>/spec/flows.md`
Với từng loại, kiểm điều kiện kích hoạt rồi mới vẽ; không đủ điều kiện thì ghi vào mục "Không vẽ".

1. **D1 Luồng (bắt buộc)**: mỗi quy trình nghiệp vụ một `flowchart` có `subgraph` theo actor. Có nhánh quyết định, nhánh lỗi (mỗi nhánh là một scenario `error`/`edge` có ID), nút gắn `[US-nnn/Sn]`/`[FR-nnn]`. Bước gọi module khác viết `→ <slug>` (slug phải nằm trong cột "Phụ thuộc" của `modules.md`).
2. **D2 Máy trạng thái**: mỗi thực thể có trường trạng thái ≥ 3 giá trị. Dùng mã enum làm tên trạng thái, nhãn mũi tên là sự kiện; nêu điều kiện/actor được phép ngay dưới sơ đồ nếu không ghi vừa trong nhãn. Chuyển không hợp lệ bị từ chối (vd duyệt hai lần) liệt kê dưới sơ đồ.
3. **D3 Trình tự**: mỗi bước vượt ranh giới (gọi module khác, hệ thống ngoài, bất đồng bộ). ≤ 8 thông điệp, mỗi thông điệp `METHOD /path` đúng như bảng API trong `srs.md` (chưa có SRS thì vẽ sau, ghi vào "Không vẽ: chờ SRS"), kèm mã lỗi của nhánh chính.
4. **Bảng chú giải** cho D1: `Bước | Actor | Mô tả | Nguồn (US/FR) | Trạng thái sau bước`.
5. **Không vẽ**: danh sách loại bỏ qua kèm lý do, và scenario/FR không có trong sơ đồ nào kèm lý do (vd "FR thuần dữ liệu").

## Ràng buộc
- Không thêm bước, vai trò, trạng thái hay quy tắc mà story/FRD/glossary không có. Chỗ thiếu thông tin (vd hủy đơn đã duyệt) thì vẽ nút `? Q-xxx` và ghi Q.
- Tên trạng thái khớp glossary/FRD; lệch thì ghi vào `consistency-report.md` hoặc open-questions, không tự sửa FRD.
- Một sơ đồ ≤ 15 nút, một câu hỏi; quá lớn thì tách theo quy trình con. Không vẽ lại cùng thông tin ở hai loại.
- Mermaid hợp lệ cú pháp: có `mmdc` thì render thử để bắt lỗi; không có thì rà bằng mắt và nói rõ chưa render.

## Độ phủ K1 (đo bằng lệnh; mọi scenario và FR phải xuất hiện trong ít nhất một sơ đồ)
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

Thiếu thì vẽ bổ sung hoặc giải thích ở "Không vẽ". Các kiểm khớp K2-K4, K6 giữa sơ đồ, SRS và test chạy ở `/ba-start check` (`ba-consistency`). Ghi `events.csv`: `flow` (`phủ%;số sơ đồ`).

## Kiểm tra trước khi báo xong
K1 = 100% hoặc mọi mục thiếu đã giải thích; mọi nhánh lỗi có scenario ID; mọi nút `?` có Q-ID; số sơ đồ báo kèm lý do không vẽ. Gợi ý `/ba-start tests --module <slug>` (TC `ST` lấy từ mũi tên D2) rồi `check`/`gate`.
