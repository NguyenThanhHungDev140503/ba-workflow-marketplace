---
name: ba-guide
description: Hướng dẫn và điều hướng workflow BA. Dùng khi người dùng hỏi về plugin/workflow BA, "dùng plugin BA", "bắt đầu dự án BA", "làm gì tiếp theo", "đang ở bước nào" - đọc trạng thái ba-workspace rồi chỉ ra bước kế tiếp.
---

# Hướng dẫn workflow BA

Nạp skill `ba-conventions` trước. Mục tiêu: xác định đang ở đâu trong workflow rồi chỉ **đúng một bước kế tiếp**, không giảng cả quy trình trừ khi người dùng hỏi tổng quan. Hỏi xác nhận trước khi chạy bước; không tự chạy bước ghi ra ngoài (push, Confluence).

## 1. Đọc trạng thái (chỉ đọc, bằng lệnh)
- `ls ba-workspace/`; có nhiều dự án thì hỏi, một dự án thì dùng nó.
- `01-backbone/status.md`, `open-questions.md` (đếm Q `Mở, chặn`), `baselines.csv`, `events.csv` (dòng cuối), `git branch --show-current` (dạng `ba/<slug>/<module>` cho biết module đang làm), `git config user.name`.
- Chưa rõ vai trò (BA hay Lead BA) thì hỏi một câu.

## 2. Chọn bước kế tiếp (lấy điều kiện đầu tiên đúng)
| Trạng thái | Việc kế tiếp |
|---|---|
| Không có `ba-workspace/` | Hỏi đường dẫn tài liệu thô -> `/ba-start intake <path>` |
| Có `00-intake`, chưa có `01-backbone` | Nhắc số Q chặn; `/ba-start backbone --slug <slug>` |
| Vừa xong backbone, chưa chọn `flow` cho module | Chạy mục 3 "Cấu hình" trước khi BA vào `flow` (có thể làm sau khi có stories để có số liệu) |
| Có backbone, workspace chưa commit | Lead BA commit workspace trước khi BA nhận module |
| BA chưa có branch module | Liệt kê module `Chưa nhận` -> `/ba-collab Tôi nhận module <slug>` |
| Module `Đang soạn` hoặc `Cần sửa`, thiếu stories | `/ba-start stories --module <m>` |
| ... có stories, thiếu `spec/` | `/ba-start frd --module <m>` rồi `srs` |
| ... có FRD, thiếu `spec/flows.md` (hoặc thiếu D2/D3 khi thực thể có trạng thái ≥ 3 giá trị / có bước vượt ranh giới mà chưa ghi "Không vẽ") | `/ba-start flow --module <m>` (độ chi tiết theo cột `flow` của module trong `modules.md`, rồi `flow-granularity` trong `vision-scope.md`, mặc định `use-case`; chưa đặt thì chạy mục 3 "Cấu hình" trước) |
| ... có spec, thiếu `tests/` | `/ba-start tests --module <m>` |
| ... có tests, chưa có hoặc cũ `consistency-report.md` | `/ba-start check --module <m>` |
| ... chưa có hoặc cũ `gate-report.md` | `/ba-start gate --module <m>` |
| Gate `REJECT` | Sửa theo bảng lỗi trong gate-report rồi chạy lại gate |
| Gate `PASS`/`CONDITIONAL`, module chưa `Chờ review` | `/ba-collab Gửi module review <m>` |
| Module `Chờ review` (Lead BA) | `/ba-collab Duyệt module <m>` |
| Mọi module `Đã duyệt` | `/ba-start package --slug <slug>`, `export docx`, `export confluence` |
| Khách đổi yêu cầu | `/ba-start impact --slug <slug> "<CR>"` |
| Dừng giữa chừng / đổi người | `/ba-collab Lưu checkpoint` / `Tiếp tục` |
| Cuối kỳ | `/ba-start retro --slug <slug>` |

"Cũ" nghĩa là có file nguồn (stories/spec) sửa sau báo cáo; so thời gian sửa file.

## 3. Cấu hình (khi người dùng hỏi "cấu hình", "nên vẽ diagram mức nào", hoặc trước khi chạy `/ba-start flow`)
Mục tiêu: chọn `flow` (độ chi tiết diagram) cho **từng module** cho hợp với team. Hai giá trị: `use-case` (mỗi story một sơ đồ, trừ story đơn giản) và `quy-trình` (gộp theo quy trình nghiệp vụ). Ưu tiên: tham số lệnh > cột `flow` trong `modules.md` > `flow-granularity` trong `vision-scope.md` > `use-case`.

1. **Đo** (chỉ đọc), chạy từ gốc workspace; mỗi dòng ra số liệu và một gợi ý:

```
python3 - <<'EOF'
import glob, os, re
rd = lambda f: open(f, encoding="utf-8").read() if os.path.isfile(f) else ""
flow = {}
rows = [l.strip("| \n").split("|") for l in rd("01-backbone/modules.md").splitlines() if l.startswith("|")]
if rows:
    head = [c.strip() for c in rows[0]]
    for r in rows[2:]:
        d = dict(zip(head, [c.strip() for c in r]))
        flow[d.get("slug", "")] = (d.get("flow", ""), d.get("Phụ thuộc", ""))
for m in sorted(glob.glob("modules/*/")):
    slug = os.path.basename(m.rstrip("/"))
    sc = [len(re.findall(r"\[US-\d+/S\d+\]", rd(f))) for f in glob.glob(m + "stories/US-*.md")]
    cx = sum(1 for n in sc if n >= 4)
    stateful = bool(re.search(r"stateDiagram|trạng thái|status", rd(m + "spec/frd.md"), re.I))
    ratio = cx / len(sc) if sc else 0
    rec = "use-case" if ratio >= 0.3 or stateful else "quy-trình"
    cur, dep = flow.get(slug, ("", ""))
    print(f"{slug}: {len(sc)} story, {sum(sc)} scenario, {cx} story >=4 scenario ({round(100*ratio)}%), có trạng thái: {'có' if stateful else 'không'}, phụ thuộc: {dep or '-'}, flow hiện tại: {cur or '(chưa đặt)'} -> gợi ý {rec}")
EOF
```

Quy tắc gợi ý: `use-case` nếu từ 30% story có ≥ 4 scenario hoặc module có trạng thái; còn lại `quy-trình`. Đây là gợi ý, không phải luật. Chưa có stories thì không có số liệu: giải thích hai mức và hỏi thay vì đoán.
2. **Hỏi tối đa 2 câu** để điều chỉnh gợi ý: team code nhận việc theo use case/ticket hay theo tính năng/quy trình? Có muốn ít tài liệu hơn là chi tiết từng bước không? Nhận việc theo use case hoặc cần chi tiết thì nghiêng `use-case`; muốn gọn thì nghiêng `quy-trình`.
3. **Trình bày** bảng `module | số liệu chính | gợi ý | lý do một dòng`, nêu rõ đánh đổi: `use-case` dễ review và truy vết hơn nhưng nhiều sơ đồ hơn; `quy-trình` gọn nhưng một sơ đồ lớn hơn, khó giao việc.
4. **Ghi khi người dùng đồng ý**: điền cột `flow` của từng module trong `01-backbone/modules.md` (thêm cột nếu thiếu); đặt mặc định dự án bằng dòng `flow-granularity:` trong `vision-scope.md` nếu nhiều module cùng mức. Module đã có `spec/flows.md` mà đổi mức thì nhắc chạy lại `/ba-start flow --module <m>`; không tự vẽ lại.

## 4. Trả lời
Ngắn: (1) đang ở bước nào (một dòng, kèm số liệu: module, trạng thái, Q chặn); (2) bước kế tiếp với lệnh chính xác; (3) hỏi có chạy luôn không. Người dùng hỏi tổng quan thì mới đưa bảng vòng đời: `Chưa nhận -> Đang soạn -> Chờ review -> Đã duyệt` (hoặc `Cần sửa`) và hai vai Lead BA / BA, trỏ tới README của plugin.
