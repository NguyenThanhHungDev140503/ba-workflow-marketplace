---
name: ba-gate
description: Bước 6 của workflow BA - chấm điểm chất lượng một module (truy vết, độ sâu AC, từ mơ hồ, câu hỏi chặn, thuật ngữ, đủ spec) và ra verdict PASS / CONDITIONAL / REJECT. Dùng khi chạy /ba-start gate --module.
---

# Gate

Nạp skill `ba-conventions` trước. Tham số: `--module <slug>` (bắt buộc, hỏi nếu thiếu). Chỉ đọc, chỉ ghi `gate-report.md` và dòng verdict trong `status.md`. Không tự sửa artifact để "cho qua".

Đầu vào: `modules/<module>/stories/`, `spec/` (có thể chưa có spec: khi đó chiều 6 tính theo story), `traceability.csv`, `glossary.md`, `open-questions.md`. Tùy chọn: `tests/` (độ phủ test), `consistency-report.md` (lỗi nhất quán). Thiếu stories thì dừng, gợi ý `/ba-start stories`.

## 6 chiều (đo bằng lệnh, ghi con số thô cạnh điểm)
| # | Chiều | Trọng số | Điểm 0-100 |
|---|---|---|---|
| 1 | Truy vết | 25 | % US/FR có đủ chuỗi US→BR→RAW trong `traceability.csv` |
| 2 | Độ sâu AC | 20 | % story có >= 3 scenario gồm happy, edge, error |
| 3 | Từ mơ hồ | 20 | 100 − 10 × số lần dùng từ mơ hồ không kèm số đo (tối thiểu 0). Dòng ghi rõ `chờ Q-xxx` (đang chờ số) không tính ở đây; thiếu số đã bị phạt ở chiều 6 |
| 4 | Câu hỏi chặn | 15 | 100 nếu không còn Q `Mở, chặn` của module; 0 nếu còn |
| 5 | Thuật ngữ | 10 | % thuật ngữ nghiệp vụ trong story/spec có trong `glossary.md` |
| 6 | Đủ spec | 10 | % FR có US nguồn và kiểm chứng được; NFR có số đo |

Điểm tổng = tổng(điểm × trọng số) / 100, tính bằng `python3`.

## Verdict
- **REJECT**: tổng < 65, hoặc có lỗi cứng: story không có AC, ID mồ côi (không truy ngược được), số nghiệp vụ tự đặt không có nguồn.
- **CONDITIONAL**: 65 ≤ tổng < 85, hoặc còn Q `Mở, chặn` của module.
- **PASS**: tổng ≥ 85 và không có lỗi cứng, không còn Q chặn.

Hạ bậc (không đổi điểm, không đổi trọng số): PASS hạ thành CONDITIONAL khi
- có `tests/` và độ phủ scenario < 90% (tính theo `ba-testgen`), hoặc
- `consistency-report.md` còn lỗi **H** chưa sửa.
Chưa có `tests/` hoặc báo cáo consistency thì ghi "chưa chạy" trong gate-report, không hạ bậc. Báo cáo consistency/test cũ hơn stories/spec (so thời gian sửa file) thì ghi "đã cũ", không tính.

## Tạo `modules/<module>/gate-report.md`
Verdict + điểm tổng, bảng 6 chiều (số thô, điểm, ghi chú), bảng lỗi `Mức | File:dòng | Lỗi | Cách sửa`, việc cần làm trước khi gửi review. Thêm mục "Test và nhất quán" (độ phủ, số lỗi H/M/L, hoặc "chưa chạy"). Cập nhật cột `verdict gần nhất` trong `status.md` và ghi `events.csv` dòng `gate` (`VERDICT;điểm;số lỗi cứng`).

## Ràng buộc
- Mỗi lỗi chỉ ra file và dòng cụ thể; không nhận xét chung chung.
- Không dùng cùng một phiên để vừa soạn vừa chấm nếu có thể tách: nói rõ nếu người chấm chính là người soạn, vì kết quả dễ thiên vị.
- Dấu hiệu tự lừa: "story nhỏ nên khỏi cần edge case", "một vai trò nên khỏi cần phân quyền", "sẽ làm rõ sau". Gặp thì tính là lỗi.
- Scenario thiếu ID `US-nnn/Sn` tính là lỗi cứng khi module đã có `tests/`.
- Gợi ý bước kế: PASS/CONDITIONAL -> `/ba-collab Gửi module review <slug>`; REJECT -> sửa theo bảng lỗi rồi chạy lại gate.
