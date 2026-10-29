---
name: ba-conventions
description: Quy ước dùng chung của workflow BA (ID, trạng thái module, schema traceability, baseline, events.csv, severity, từ mơ hồ, cách tìm workspace). Các skill ba-* nạp skill này trước khi làm việc; không chạy độc lập.
---

# Quy ước chung

Mọi skill `ba-*` tuân theo file này. Mâu thuẫn giữa skill và file này thì theo file này.

## Workspace
- Gốc: `ba-workspace/<slug>/` tại thư mục làm việc hiện tại.
- Không có `<slug>`: nếu `ba-workspace/` có đúng một thư mục con thì dùng nó, nhiều hơn thì hỏi, không đoán.

## ID (ổn định, không đánh lại số, không tái sử dụng)
`RAW-nnn` yêu cầu thô · `BR-nnn` mục tiêu nghiệp vụ · `US-nnn` story · `FR-nnn` yêu cầu chức năng · `NFR-nnn` phi chức năng · `Q-nnn` câu hỏi mở · `CR-nnn` thay đổi · `TC-nnn-mm` test case (nnn = số US, mm = thứ tự).
**Scenario ID**: mỗi scenario trong story có ID `US-012/S1`, `S2`... viết ngay trong tên scenario: `Scenario: [US-012/S1] <tên>`. Test case và báo cáo dựa vào ID này. Story cũ chưa có thì bổ sung, không đổi nội dung scenario.

## Trạng thái module (`01-backbone/status.md`)
Cột: `module | owner | branch | trạng thái | cập nhật | verdict gần nhất`.
Giá trị trạng thái, chỉ dùng đúng các chữ này:
`Chưa nhận` → `Đang soạn` → `Chờ review` → `Đã duyệt`; từ `Chờ review`/`Đã duyệt` có thể về `Cần sửa` (review trượt hoặc có CR), rồi `Đang soạn` lại.

## traceability.csv
Một dòng cho mỗi liên kết, cột cố định, ô chưa có để trống:

`RAW-ID,BR-ID,module,US-ID,FR-ID,NFR-ID,TC-ID`

- backbone: tạo dòng `RAW,BR,module,,,,`.
- stories: mỗi US thêm dòng (sao chép RAW/BR/module nguồn) với `US-ID`.
- spec: điền `FR-ID`/`NFR-ID` vào dòng cùng `US-ID`; một US có nhiều FR thì thêm dòng.
- tests: điền `TC-ID` vào dòng cùng `US-ID`; một US có nhiều TC thì thêm dòng.
- File cũ thiếu cột `TC-ID` thì thêm cột (rỗng) khi ghi lần đầu. Không xóa dòng. RAW ngoài phạm vi để `module=OUT-OF-SCOPE`.
- Ghi CSV bằng `python3` (module `csv`) để ô có dấu phẩy được quote đúng, luôn `csv.writer(f, lineterminator="\n")` và `open(..., newline="", encoding="utf-8")` (mặc định của `csv` là CRLF, lẫn với dòng thêm bằng `echo` và làm Git báo đổi dòng).
- RAW/BR toàn hệ thống (phi chức năng, ràng buộc chung): để `module=ALL`. NFR của chúng nằm trong SRS của **module chủ NFR**, được `backbone` đánh dấu `(chủ NFR)` trong `modules.md`; chỉ có đúng một module như vậy.

## Test case (`modules/<module>/tests/test-cases.csv`)
Cột: `TC-ID,US-ID,Scenario,Loại,Ưu tiên,Tiền điều kiện,Bước,Dữ liệu,Kết quả mong đợi,Ghi chú`.
Mã loại (chỉ dùng bảng này): `HP` happy · `BV` biên · `ER` lỗi/không hợp lệ · `AZ` phân quyền · `ST` trạng thái · `DI` toàn vẹn dữ liệu · `PF` hiệu năng. Ưu tiên: `P1`, `P2`, `P3`.

## Severity (consistency, gate)
**H** mâu thuẫn số liệu/quy tắc hoặc đứt chuỗi truy vết · **M** thiếu đối ứng (US không có FR, FR không có endpoint, trường API không có thuộc tính) · **L** đặt tên/thuật ngữ.

## baselines.csv (`ba-workspace/<slug>/baselines.csv`)
`path,sha256,version,approved_by,date` — `path` tương đối so với `ba-workspace/<slug>/`. Chỉ thêm dòng, không sửa dòng cũ; bản mới của cùng `path` là dòng sau cùng (version tăng). Tạo bằng `sha256sum`, không tự bịa hash.
Hook `guard` của plugin hỏi xác nhận trước khi sửa file có trong danh sách này.

## events.csv (`ba-workspace/<slug>/events.csv`)
Nhật ký chỉ-thêm-dòng, nguồn dữ liệu cho retro. Cột `date,event,module,detail`; `detail` không chứa dấu phẩy. Ghi bằng lệnh sau (tạo header nếu chưa có):

```
[ -f ba-workspace/<slug>/events.csv ] || echo 'date,event,module,detail' > ba-workspace/<slug>/events.csv
echo "$(date +%F),<event>,<module>,<detail>" >> ba-workspace/<slug>/events.csv
```

| event | do skill nào ghi | detail |
|---|---|---|
| `claim` | collab | tên người nhận |
| `status` | collab, impact | `từ>đến` (vd `Đang soạn>Chờ review`) |
| `gate` | gate | `VERDICT;điểm;số lỗi cứng` |
| `tests` | testgen | `phủ%;số TC` |
| `check` | consistency | `H;M;L` (số lỗi còn lại) |
| `cr` | impact | `CR-nnn` |
| `q-open`, `q-close` | intake và bước đóng câu hỏi | `Q-nnn` |
| `export` | export, confluence | `đích;số mục` |
| `checkpoint` | checkpoint | nhãn |

Sự kiện không thuộc module nào (intake, package, export toàn dự án) để cột `module` là `-`. Thiếu sự kiện thì ghi thiếu, không suy đoán thay.

## Từ mơ hồ (không có số đo thì không được vào story/spec)
nhanh, chậm, dễ dùng, thân thiện, linh hoạt, vài, nhiều, ít, sớm, kịp thời, an toàn, ổn định, hiệu quả, dễ mở rộng, phù hợp, tương tự, v.v., nếu cần, các loại, "và các..." .

## Nguyên tắc làm việc
- Không bịa. Nguồn không nói thì ghi `open-questions.md` với Q-ID; suy luận của bạn đánh dấu `[suy luận]`, giả định `[giả định: Q-xxx]`, chưa kiểm chứng `[chưa xác minh]`.
- Con số, đếm, phần trăm: tính bằng lệnh (`grep -c`, `awk`, `python3`), không tính nhẩm.
- Ghi remote (push, gửi tin, đăng Confluence) luôn cần người dùng xác nhận từng lần. Không nhập, hiển thị hay lưu token/mật khẩu; xác thực dịch vụ ngoài qua MCP (`/mcp`).
- Cổng bàn giao: mọi lệnh `export` áp dụng đúng phần "Trước khi đóng gói" của `ba-package` (module chưa `Đã duyệt` hoặc file lệch baseline chỉ xuất khi người dùng xác nhận, và đánh dấu `NHÁP`).
- Kết thúc mỗi bước: liệt kê file đã tạo/sửa, số liệu chính, và lệnh gợi ý cho bước kế.
