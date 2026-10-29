# Checklist chạy thử ba-workflow

Chạy trong một thư mục trống mới (`git init` trước để thử claim/branch), phiên Claude Code mới. Sao chép `yeu-cau-mau.md` vào đó. Đánh dấu mỗi dòng đạt/không đạt; dòng không đạt ghi lại nguyên văn điều Claude làm sai.

## 1. `/ba-start intake yeu-cau-mau.md`
- [ ] Hỏi/đề xuất slug (vd `nghi-phep`), tạo `ba-workspace/nghi-phep/00-intake/` đủ 4 file.
- [ ] 11 ý -> ít nhất 11 dòng RAW (`RAW-001...`), mỗi dòng có nguồn.
- [ ] Mâu thuẫn mục 2 (12 vs 14 ngày): một Q ghi cả hai vế kèm tên Lan, Minh; không chọn bên nào.
- [ ] Mơ hồ không bị tự đặt số: mục 3 "nhanh/lâu", mục 8 "dễ dùng/ổn định/nhiều", mục 9 "không nhiều" -> mỗi cái trỏ một Q đòi số.
- [ ] Mục 6 (hủy đơn đã duyệt), mục 10 (TP.HCM) thành Q; Q đổi quy tắc/ngưỡng có nhãn `Mở, chặn bước stories`.
- [ ] Bảng Q có cột `Ngày mở`, `Ngày đóng`; `events.csv` có dòng `q-open`.
- [ ] Cuối báo số RAW / Q mở / Q chặn và gợi ý bước backbone.
- [ ] Chạy lại intake cùng slug: hỏi bổ sung hay dừng, **không ghi đè**.

## 2. `/ba-start backbone --slug nghi-phep`
- [ ] Có 6 file; module tách theo nghiệp vụ (vd gửi/duyệt đơn, số dư phép, báo cáo-lịch), không tách theo màn hình.
- [ ] `traceability.csv` có 7 cột; số RAW duy nhất = số RAW trong intake; RAW mục 10 xử lý (phạm vi/out-of-scope).
- [ ] `status.md`: mọi module `Chưa nhận`.

## 3. `/ba-collab Tôi nhận module <slug>`
- [ ] Tạo branch `ba/nghi-phep/<module>`, `status.md` -> `Đang soạn`, có owner, thư mục `modules/<module>/{stories,spec}` + `notes.md`.
- [ ] `events.csv` có `claim` và `status`; 1 commit cục bộ; **không push**.
- [ ] Nhận lại module đó lần hai: dừng và báo đã có owner.

## 4. `/ba-start stories --module <slug>`
- [ ] Nhắc các Q chặn trước khi viết, hỏi chờ hay viết nháp.
- [ ] Nếu nháp: scenario liên quan có `[giả định: Q-xxx]`.
- [ ] Mỗi story >= 3 scenario có ID `[US-nnn/Sn]`; có scenario "không đủ quyền" cho hành động phân quyền.
- [ ] Không tự đặt số cho 12/14 ngày hay "nhanh".
- [ ] `traceability.csv` có dòng `US-ID`.

## 5. `/ba-start frd`, `srs`, `tests`, `check` (cùng `--module`)
- [ ] SRS chưa có FRD -> tạo FRD trước và nói rõ.
- [ ] NFR cho "ổn định/nhiều người dùng" có Q đòi số, không tự đặt.
- [ ] `tests`: mỗi scenario >= 1 TC; có bộ biên cho ngưỡng 3 ngày nghỉ ốm; TC phụ thuộc Q ghi `[chờ Q-xxx]`; in ra `phủ% >= 90` hoặc nêu lý do; không dữ liệu `test123`.
- [ ] `check`: bảng tóm tắt + bảng lỗi có file:dòng; có mục "Đã loại (false positive)".

## 6. `/ba-start gate --module <slug>`
- [ ] Còn Q chặn mở -> verdict không thể là PASS.
- [ ] Bảng 6 chiều có số thô; điểm tổng tính bằng lệnh.
- [ ] Cố tình xóa một scenario khỏi 1 story rồi chạy lại: REJECT hoặc lỗi cứng nêu đúng file.
- [ ] `status.md` có verdict; `events.csv` có `gate`.

## 7. Review và duyệt
- [ ] `/ba-collab Gửi module review <slug>` khi gate REJECT: từ chối. Khi hợp lệ: tạo `review-packet.md`, trạng thái `Chờ review`, **không gửi đi đâu**.
- [ ] `/ba-collab Duyệt module <slug>`: hỏi tên người duyệt, xác nhận; `baselines.csv` có hash cho stories, spec, tests; trạng thái `Đã duyệt`.
- [ ] **Hook**: nhờ Claude sửa một file đã baseline -> hiện hộp hỏi xác nhận với lý do "đã duyệt (v1, ...)".
- [ ] `/ba-start stories --module <slug>` trên module đã duyệt: dừng, trỏ sang `impact`.

## 8. `/ba-start impact --slug nghi-phep "Khách muốn thêm loại phép thai sản 6 tháng"`
- [ ] Tạo `changes/CR-001.md` có bảng ảnh hưởng, cột "Đã duyệt?", TC bị ảnh hưởng; ảnh hưởng suy đoán ghi `[chưa xác minh]`.
- [ ] **Không tự sửa** spec trước khi bạn chọn phương án.

## 9. `/ba-start package`, `export docx`, `retro`
- [ ] `package`: liệt kê module chưa duyệt/lệch baseline và hỏi bản NHÁP; tạo `dist/*.html`; số mục đối chiếu nguồn.
- [ ] Sửa tay một file đã duyệt rồi `package`: báo lệch hash.
- [ ] `export docx`: không có `mmdc` thì dừng và hỏi (nếu tài liệu có Mermaid); lint placeholder; file `.docx` > 10 KB.
- [ ] `retro --slug nghi-phep --since 14d`: số liệu khớp `events.csv` (đếm tay một chỉ số); "retro đầu tiên", không so sánh kỳ trước; <= 3 việc, mỗi việc kèm lệnh.

## 10. Checkpoint
- [ ] `/ba-collab Lưu checkpoint thu-nghiem` tạo file trong `checkpoints/` có hash.
- [ ] Sửa một story rồi `/ba-collab Tiếp tục nghi-phep`: liệt kê đúng file đã đổi **trước** khi đề xuất bước tiếp.

## Ghi kết quả
Gửi lại danh sách dòng không đạt (kèm trích đoạn). Chỗ nào skill diễn đạt mơ hồ thì tôi sửa skill rồi bạn `/reload-plugins` chạy lại đúng bước đó.
