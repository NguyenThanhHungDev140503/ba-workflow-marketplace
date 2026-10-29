---
name: ba-retro
description: Hồi cứu theo kỳ (mặc định 7 ngày) từ events.csv - module đã duyệt, tỷ lệ PASS, cycle time, churn, câu hỏi chặn tồn - kèm tối đa 3 việc tiếp theo. Dùng khi chạy /ba-start retro.
---

# Retro

Nạp skill `ba-conventions` trước. Tham số: `--slug <slug>` (bắt buộc), `--since 24h|7d|14d|30d|YYYY-MM-DD` (mặc định `7d`), `--by-owner` (bật số liệu theo người), `--git` (thêm `git log` khi có `.git/`). Chỉ đọc; ghi vào `retro/`.

## Dữ liệu
`events.csv` (chính), `changes/CR-*.md`, `00-intake/open-questions.md` (có ngày mở/đóng), `status.md`. Thiếu `events.csv` hoặc kỳ không có sự kiện nào thì nói "không có hoạt động trong kỳ" và dừng. Sự kiện thiếu (vd không có `q-open`) thì ghi rõ chỉ số nào không tính được, không suy đoán.

## Tính số liệu (chạy lệnh, không tính nhẩm)
Thay `WS` và `SINCE` (`YYYY-MM-DD`):

```
python3 - <<'EOF'
import csv, collections, datetime as dt, json, statistics as st
WS, SINCE = "ba-workspace/SLUG", dt.date.fromisoformat("YYYY-MM-DD")
d = lambda r: dt.date.fromisoformat(r["date"])
rows = list(csv.DictReader(open(f"{WS}/events.csv", encoding="utf-8")))
win = [r for r in rows if d(r) >= SINCE]
gates = [r for r in win if r["event"] == "gate"]
verd = collections.Counter(r["detail"].split(";")[0] for r in gates)
st_to = lambda r, s: r["event"] == "status" and r["detail"].endswith(">" + s)
approved = [r for r in win if st_to(r, "Đã duyệt")]
cycle = []
for a in approved:
    s = [d(r) for r in rows if r["module"] == a["module"] and st_to(r, "Đang soạn") and d(r) <= d(a)]
    if s:
        cycle.append((d(a) - max(s)).days)
churn = collections.Counter(r["module"] for r in win if st_to(r, "Cần sửa") or r["event"] == "cr")
out = {
    "approved": len(approved),
    "gate_runs": len(gates), "verdicts": dict(verd),
    "pass_rate": round(100 * verd["PASS"] / len(gates)) if gates else None,
    "cycle_days_median": st.median(cycle) if cycle else None,
    "churn_top5": churn.most_common(5),
}
print(json.dumps(out, ensure_ascii=False))
EOF
```

Định nghĩa: `pass_rate` = PASS / mọi lần gate trong kỳ; `cycle` = ngày từ lần `Đang soạn` gần nhất đến `Đã duyệt`; `churn` = số lần về `Cần sửa` + số CR theo module. Thêm bằng lệnh: tuổi trung vị câu hỏi mở (hôm nay − `Ngày mở`), số Q `chặn` mở > 5 ngày, chiều gate trượt nhiều nhất (đọc các `gate-report.md`, ghi nếu đủ dữ liệu).

## Báo cáo `retro/retro-<yyyymmdd>.md`
1. Một dòng tóm tắt.
2. Đã bàn giao (module `Đã duyệt` trong kỳ).
3. Churn (module, nguyên nhân: CR hay review trượt, trích CR-ID hoặc gate-report).
4. Chất lượng gate: kỳ này vs kỳ trước (đọc `retro/snapshot-*.json` gần nhất; chưa có thì ghi "retro đầu tiên", bỏ phần so sánh).
5. Hotspot: top 5 module theo churn.
6. **Tối đa 3 việc tiếp theo**, mỗi việc kèm một lệnh cụ thể (vd lỗi từ mơ hồ lặp lại -> `/ba-start stories --module X` và đóng Q-xxx).

Ghi `retro/snapshot-<yyyymmdd>.json` (kết quả JSON trên + cửa sổ) để lần sau tính chênh lệch.

## Quy tắc
- Mọi nhận xét trích một sự kiện, CR hoặc file; nhận xét không dẫn được thì bỏ.
- Báo cáo theo module và quy trình, không đổ lỗi cá nhân. Chỉ nêu theo người khi có `--by-owner`.
- Không tính cập nhật nhỏ làm churn; churn chỉ là `Cần sửa` và CR.
- Không đủ dữ liệu cho một chỉ số thì ghi "không đủ dữ liệu: thiếu sự kiện X".
