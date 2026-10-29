---
name: ba-testgen
description: Bước 5b của workflow BA - sinh test case từ acceptance criteria của một module, đo độ phủ scenario. Dùng khi chạy /ba-start tests --module.
---

# Test cases

Nạp skill `ba-conventions` trước. Tham số: `--module <slug>` (bắt buộc, hỏi nếu thiếu). Đầu vào: `modules/<module>/stories/` (scenario phải có ID `US-nnn/Sn`), `spec/` nếu có (ma trận quyền, state diagram, NFR). Thiếu stories thì dừng; scenario thiếu ID thì dừng và gợi ý bổ sung ID ở `stories`. Module `Đã duyệt` thì dừng: sửa phải đi qua `/ba-start impact`.

## Quy tắc sinh (mỗi quy tắc trả lời bằng TC, không bằng lời)
1. Mỗi scenario có ít nhất 1 TC. Happy -> `HP`; edge -> `BV` hoặc `ST`; error -> `ER` hoặc `AZ`.
2. Mỗi trường có ngưỡng/độ dài/khoảng ngày trong story hoặc spec -> bộ biên `min-1, min, min+1, max-1, max, max+1` (loại giá trị không có nghĩa, vd độ dài âm). Chỉ dùng con số có trong nguồn.
3. Mỗi vai trò trong ma trận quyền -> ít nhất 1 TC `AZ` được phép và 1 TC bị từ chối.
4. Mỗi chuyển trạng thái trong state diagram, kể cả chuyển không hợp lệ (vd duyệt hai lần) -> `ST`.
5. Quy tắc dùng chung dữ liệu giữa module (spec có nêu) -> `DI`.
6. Mỗi NFR có số đo -> 1 TC `PF` nêu tiêu chí đo, không viết kịch bản tải.
7. Chỗ thiếu số hoặc thiếu kết quả mong đợi: không bịa. Ghi Q-ID vào `open-questions.md`, TC đánh dấu `[chờ Q-xxx]` trong cột Ghi chú.

## Ghi
- `modules/<module>/tests/test-cases.csv` theo cột trong `ba-conventions`, ghi bằng `python3` + `csv`. Dữ liệu mẫu thực tế (tên, số tiền, ngày hợp lý), không `test123`. Kết quả mong đợi cụ thể, không "hoạt động bình thường". Tiền điều kiện/bước đủ để người khác chạy mà không hỏi lại.
- `modules/<module>/tests/test-summary.md`: số TC theo loại, độ phủ, TC đang chờ Q.
- `traceability.csv`: điền `TC-ID` theo `US-ID`. `events.csv`: dòng `tests`.
- Chạy lại thì giữ `TC-ID` đã có, đánh tiếp số, scenario đã xóa thì đánh dấu TC `[bỏ]` thay vì xóa.

## Độ phủ (đo bằng lệnh, ngưỡng 90%)
Chạy từ thư mục gốc workspace, thay `M` bằng module:

```
python3 - <<'EOF'
import csv, glob, re
M = "modules/M"
sc = {m for f in glob.glob(f"{M}/stories/US-*.md") for m in re.findall(r"\[(US-\d+/S\d+)\]", open(f, encoding="utf-8").read())}
cov = {r["Scenario"] for r in csv.DictReader(open(f"{M}/tests/test-cases.csv", encoding="utf-8")) if "[bỏ]" not in r["Ghi chú"]}
print(len(sc & cov), "/", len(sc), "phủ%", round(100 * len(sc & cov) / len(sc)) if sc else 0, "thiếu:", sorted(sc - cov))
EOF
```

Phụ: số trường có bộ `BV`, số vai trò có `AZ` cả hai chiều.

## Kiểm tra trước khi báo xong
Phủ >= 90% hoặc nêu lý do; không TC nào thiếu kết quả mong đợi; mỗi TC `BV` có giá trị lấy từ nguồn. Gợi ý `/ba-start check --module <slug>` rồi `/ba-start gate --module <slug>`.
