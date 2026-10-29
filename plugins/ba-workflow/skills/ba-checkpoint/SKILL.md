---
name: ba-checkpoint
description: Lưu và nối lại trạng thái làm việc của một module (đang làm gì, quyết định, bước tiếp, file đã đổi), để đổi phiên hoặc bàn giao cho BA khác. Dùng khi chạy /ba-collab Lưu checkpoint hoặc Tiếp tục.
---

# Checkpoint

Nạp skill `ba-conventions` trước. Checkpoint nằm trong workspace nên đi theo Git cùng branch module, BA khác nhận bàn giao đọc được. Chỉ ghi file; không tự commit, không push.

## Lưu ("Lưu checkpoint [nhãn]")
1. Xác định module: branch hiện tại dạng `ba/<slug>/<module>` thì lấy từ đó, không thì hỏi.
2. Tạo `ba-workspace/<slug>/checkpoints/<yyyymmdd-hhmm>-<module>.md`:

```
---
ts: <ISO 8601 kèm múi giờ>
branch: <branch hoặc "không có git">
module: <module>
step: <bước hiện tại: stories | spec | tests | check | gate | review>
active_artifact: <file đang sửa>
label: <nhãn>
---
## Đang làm
## Quyết định
- LOCKED: <đã chốt, kèm ai/khi nào>
- OPEN: <chưa chốt, kèm Q-ID nếu có>
## 3 bước tiếp theo
(đủ cụ thể để làm ngay mà không đọc lại ghi chú; mỗi bước nêu file hoặc lệnh)
## Lưu ý
## Trạng thái tại thời điểm lưu
(trạng thái module, verdict gate gần nhất, Q chặn còn mở: tính bằng lệnh, không nhớ)
## Hash
<sha256sum> <path>   (status.md, mọi file trong stories/, spec/, tests/ của module)
```

3. Ghi `events.csv` dòng `checkpoint`. Nói rõ file vừa tạo.

## Tiếp tục ("Tiếp tục [slug]")
1. Chọn checkpoint mới nhất của module (theo branch hiện tại, hoặc hỏi nếu có nhiều module). Không có thì báo "chưa có checkpoint" và dừng.
2. Chạy lại `sha256sum` cho các file trong mục Hash. Liệt kê **file đã đổi, mới thêm, đã xóa kể từ checkpoint** trước mọi việc khác; ai đổi thì lấy từ `git log` nếu có.
3. Trạng thái module khác lúc lưu (vd đã `Chờ review` hoặc `Đã duyệt`) thì cảnh báo; module `Đã duyệt` thì không tiếp tục sửa mà gợi ý `/ba-start impact`.
4. In lại Đang làm, Quyết định, 3 bước tiếp theo; hỏi người dùng có đúng bước 1 không rồi mới làm.

## Quy tắc
- Quyết định `LOCKED` không bị đảo ngược khi tiếp tục trừ khi người dùng nói.
- Bước tiếp theo mơ hồ ("làm tiếp story") thì viết lại cho cụ thể trước khi lưu.
- Checkpoint là trạng thái phiên, không phải lịch sử artifact; lịch sử nằm ở Git và `baselines.csv`.
