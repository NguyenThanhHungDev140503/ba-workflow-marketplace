---
name: ba-consistency
description: Bước 5c của workflow BA - kiểm tra nhất quán chéo giữa story, FRD/SRS (endpoint, thực thể) và giữa các module, phân loại lỗi H/M/L. Dùng khi chạy /ba-start check.
---

# Consistency

Nạp skill `ba-conventions` trước. Tham số: `--module <slug>` (một module) hoặc không có (liên module). Chỉ đọc, chỉ ghi báo cáo; không tự sửa artifact. Thiếu stories thì dừng; thiếu SRS thì chỉ chạy phần (a), (d), (e) và nói rõ.

## Kiểm tra mỗi module
- (a) US ↔ FR hai chiều: US không có FR (M); FR không trỏ US nào (M).
- (b) FR ↔ endpoint trong SRS: FR cần API mà SRS không có (M); endpoint không FR nào dùng (M).
- (c) Trường request/response ↔ thuộc tính thực thể trong ER: trường không có thuộc tính (M); kiểu dữ liệu khác nhau (H).
- (d) Cùng một quy tắc/số liệu ở story, FR, NFR, TC: giá trị khác nhau (H).
- (e) Thuật ngữ so với `glossary.md`: một khái niệm hai tên gọi (L); thuật ngữ không có trong glossary (L).

## Kiểm tra liên module (`check` không `--module`)
- Thực thể xuất hiện ở nhiều module nhưng thuộc tính/kiểu khác nhau (H).
- Phụ thuộc khai trong `modules.md` mà spec không dùng, hoặc spec dùng module không khai (M).
- BR xung đột giữa hai module (H).
- Module có trạng thái khác nhau nhưng phụ thuộc lẫn nhau, vd module `Đã duyệt` phụ thuộc module `Đang soạn` (M).

## Kiểm khớp diagram (K2-K4, K6; chạy khi có `spec/flows.md`)
Chạy từ gốc workspace, thay `M` (đường dẫn `modules/M`) và `"M"` (slug) bằng module cần kiểm. Quy ước nhãn: xem "Bộ diagram" ở `ba-conventions`.

- **K2** tập trạng thái D2 = `enum status` trong SRS (lệch: **H**).
- **K3** mỗi mũi tên D2 có ít nhất một TC `ST:A>B` (thiếu: **M**).
- **K4** mọi endpoint ở D3 có trong bảng API của SRS (D3 có mà SRS không: **H**; SRS có mà chưa vẽ D3 chỉ là thông tin).
- **K6** mọi `→ <module>` ở D1/D3 nằm trong cột "Phụ thuộc" của `modules.md` (thiếu: **M**).
- K1 (phủ scenario/FR) chạy ở `ba-flow`; K5 là (c) ở trên.

```
python3 - <<'EOF'
import csv, re
M, SLUG = "modules/M", "M"
rd = lambda f: open(f, encoding="utf-8").read()
fl, srs = rd(f"{M}/spec/flows.md"), rd(f"{M}/spec/srs.md")
F = chr(96) * 3  # ba backtick, tránh đóng khối mã của tài liệu này
blocks = re.findall(F + r"mermaid\n(.*?)" + F, fl, re.S)
sd = "\n".join(b for b in blocks if "stateDiagram" in b)
seq = "\n".join(b for b in blocks if "sequenceDiagram" in b)
out = []
# K2 trạng thái D2 = enum status trong SRS
arrows = set(re.findall(r"^\s*(\w+)\s*-->\s*(\w+)", sd, re.M))
states = {s for a in arrows for s in a}
m = re.search(r"enum\s+status\s*:\s*(.+)", srs)
enum = {x.strip() for x in m.group(1).split("|")} if m else set()
if sd:
    out.append(("K2", len(states & enum), len(states | enum), "chỉ ở D2: %s; chỉ ở enum: %s" % (sorted(states - enum), sorted(enum - states))))
    # K3 mỗi mũi tên hợp lệ có TC ST
    tcs = {(a, b) for r in csv.DictReader(open(f"{M}/tests/test-cases.csv", encoding="utf-8")) for a, b, bad in re.findall(r"ST:(\w+)>(\w+)(!?)", r["Ghi chú"]) if not bad}
    out.append(("K3", len(arrows & tcs), len(arrows), "mũi tên thiếu TC: %s" % sorted(arrows - tcs)))
# K4 endpoint D3 phải có trong bảng API SRS
ep = lambda t: set(re.findall(r"\b(GET|POST|PUT|PATCH|DELETE) (/[\w/{}\-]+)", t))
d3, api = ep(seq), ep(srs)
if seq:
    out.append(("K4", len(d3 & api), len(d3), "D3 không có trong SRS: %s; SRS chưa vẽ D3 (info): %s" % (sorted(d3 - api), sorted(api - d3))))
# K6 mũi tên "→ module" phải nằm trong cột Phụ thuộc
row = next((l for l in rd("01-backbone/modules.md").splitlines() if l.startswith(f"| {SLUG} |")), "")
deps = {d.strip() for d in row.strip("| ").split("|")[-1].split(",")} if row else set()
refs = set(re.findall(r"→ ([a-z0-9-]+)", fl))
out.append(("K6", len(refs & deps), len(refs), "tham chiếu không có trong Phụ thuộc: %s" % sorted(refs - deps)))
for k, ok, tot, note in out:
    print(k, ok, "/", tot, note)
EOF
```

Thiếu `flows.md` hoặc `srs.md` thì bỏ qua kiểm tương ứng và ghi vào "Chưa kiểm được". Kết quả ghi vào bảng lỗi của báo cáo.

## Quy trình
1. Kiểm kê artifact từng module (đếm story, FR, endpoint, thực thể bằng lệnh); thiếu artifact nào ghi vào mục "Chưa kiểm được".
2. Đối chiếu từng cặp, mỗi phát hiện ghi file:dòng cả hai phía.
3. **Phản biện, loại false positive** trước khi báo: trường tính toán không cần cột; khác quy ước camelCase/snake_case đã ghi trong spec; phạm vi đã hoãn có Q-ID hoặc ghi "ngoài phạm vi". Mỗi cái loại bỏ ghi lại một dòng kèm lý do.
4. Phát hiện không dẫn được file:dòng thì không ghi.

## Báo cáo
`modules/<module>/consistency-report.md` (hoặc `consistency-report.md` ở gốc workspace cho liên module):
- Bảng tóm tắt: `Kiểm tra | Số mục | Khớp | Lệch | %`.
- Bảng lỗi: `# | Loại | Nguồn | Đích | Lỗi | Severity | Cách sửa`.
- Mục "Đã loại (false positive)" và "Chưa kiểm được".
Ghi `events.csv` dòng `check` với `H;M;L` còn lại. Gợi ý `/ba-start gate --module <slug>`; còn lỗi H thì gate sẽ hạ PASS xuống CONDITIONAL.
