---
description: BA teamwork - nhận module (tách Git branch), gửi module review, Lead BA duyệt module, lưu/nối checkpoint
argument-hint: <"Tôi nhận module [slug]" | "Gửi module review [slug]" | "Duyệt module [slug]" | "Lưu checkpoint [nhãn]" | "Tiếp tục [slug]">
---

Tham số: `$ARGUMENTS`

Nạp skill `ba-collab` bằng Skill tool và làm theo.

- Có cụm "nhận module" -> chế độ **claim**.
- Có cụm "review" -> chế độ **review packet**.
- Có cụm "duyệt" -> chế độ **duyệt** (Lead BA).
- Có cụm "checkpoint" hoặc "tiếp tục" -> chế độ **checkpoint** (skill `ba-checkpoint`).
- Không khớp: hỏi lại đúng 1 câu, dừng.

Không tự `git push`, không tự merge. Chỉ tạo branch/commit cục bộ khi người dùng đã nêu rõ; mọi thao tác ghi ra remote phải xin xác nhận trước.
