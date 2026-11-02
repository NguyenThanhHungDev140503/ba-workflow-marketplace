# Thiết kế: bộ diagram cho team code (chi tiết đủ dùng, không thừa)

Trạng thái: **đã cài đặt trong 0.5.0** (khác thiết kế: K3 dùng quy ước `ST:A>B` ở cột Ghi chú của TC; K2 so với dòng `enum status:` dưới sơ đồ ER; `ba-export`/`ba-package` không đổi). Đã thử K2/K3/K4/K6 trên module mẫu có lỗi cố ý; chưa thử trên module thật. Căn cứ: phản hồi sau khi dùng thử ("diagram đơn giản, tính năng nhiều"), và hiện trạng plugin 0.4.0.

## 1. Hiện trạng
| Nơi | Diagram | Vấn đề |
|---|---|---|
| `backbone` → `process-flows.md` | 1 flowchart/quy trình lớn, mức dự án | không có vai trò, không có ngoại lệ, không có sơ đồ module/phụ thuộc |
| `ba-flow` → `spec/flows.md` | swimlane + nhánh lỗi + điểm tích hợp (0.4.0) | một loại duy nhất; `sequenceDiagram` chỉ nhắc "khi cần"; không có mẫu |
| `ba-spec` → `frd.md`/`srs.md` | state diagram "nếu có", ER | không bắt buộc, không kiểm khớp với flow/API/test |
| mọi nơi | — | không ai quyết định *nên vẽ gì, bao nhiêu* |

Hệ quả: dev không có sơ đồ tương tác (ai gọi API nào, thứ tự, lỗi), không có máy trạng thái bắt buộc, ER không đối chiếu với API. Vừa thiếu chỗ cần, vừa dễ vẽ tràn lan chỗ không cần.

## 2. Dev cần gì từ BA
| Câu hỏi của dev | Diagram trả lời | Có sẵn? |
|---|---|---|
| Hệ thống gồm những khối nào, phụ thuộc nhau ra sao? | **D0 Bản đồ module** | không |
| Nghiệp vụ đi qua những bước, ai làm, rẽ nhánh nào? | **D1 Luồng (swimlane)** | có (`ba-flow`) |
| Thực thể X có những trạng thái nào, chuyển khi nào, ai được chuyển? | **D2 Máy trạng thái** | tùy chọn |
| Các bên gọi nhau theo thứ tự nào, lỗi thì sao? | **D3 Trình tự** | không có mẫu |
| Dữ liệu lưu thế nào, khóa, quan hệ, enum? | **D4 ER** | có, chưa kiểm |
| Quyền ai làm gì | bảng (không vẽ) | có trong FRD |

Quy tắc loại: **không** vẽ sơ đồ lớp, deployment, activity trùng với flow, hay sơ đồ riêng cho từng story. Bảng làm tốt hơn thì dùng bảng.

## 3. Nguyên tắc chống thừa
1. **Chỉ vẽ khi có thông tin mà bảng/văn bản không nói rõ bằng**; mỗi loại có điều kiện kích hoạt (mục 4).
2. **Ngân sách**: tối đa 5 loại (D0-D4); mỗi sơ đồ ≤ 15 nút, quá thì tách theo quy trình con; mỗi sơ đồ trả lời đúng một câu hỏi.
3. **Mọi phần tử có ID nguồn** (`US-001/S1`, `FR-005`, `POST /leave-requests`, tên trạng thái); phần tử không có nguồn là bịa.
4. **Một nguồn sự thật**: tên trạng thái/thực thể lấy từ `glossary.md` và FRD; mọi sơ đồ dùng đúng tên đó.
5. **Phủ được đo bằng lệnh**, không phủ thì phải giải thích (mục "Không vẽ").
6. Chỉ Mermaid; không ảnh chụp, không công cụ vẽ ngoài.

## 4. Bộ diagram đề xuất
| # | Diagram | Mức | Kích hoạt | Chứa | Neo vào | Giới hạn |
|---|---|---|---|---|---|---|
| D0 | Bản đồ module (`flowchart`) | dự án, ở `backbone` | luôn | module, phụ thuộc có chiều, hệ thống ngoài | `modules.md` | 1 sơ đồ, ≤ 15 nút |
| D1 | Luồng swimlane | module, `spec/flows.md` | luôn, mỗi quy trình nghiệp vụ | actor, quyết định, nhánh lỗi, điểm gọi module khác | US/Sn, FR | mỗi quy trình ≤ 15 nút |
| D2 | Máy trạng thái (`stateDiagram-v2`) | module, `spec/flows.md` | thực thể có trường trạng thái với ≥ 3 giá trị | trạng thái, sự kiện, điều kiện (guard), actor được phép | glossary, FRD, enum trong ER, TC `ST` | 1 sơ đồ/thực thể |
| D3 | Trình tự (`sequenceDiagram`) | module, `spec/flows.md` | bước vượt ranh giới: gọi module khác, hệ thống ngoài, hoặc bất đồng bộ | thứ tự gọi, endpoint, mã lỗi, nhánh lỗi chính | endpoint/mã lỗi trong SRS, FR | 1 sơ đồ/điểm tích hợp, ≤ 8 thông điệp |
| D4 | ER (`erDiagram`) | module, `srs.md` | module sở hữu dữ liệu | thực thể, khóa, quan hệ + bội số, enum, thực thể module khác dạng stub | trường API, glossary | chỉ thực thể module sở hữu |

Không có điều kiện kích hoạt thì ghi vào mục "Không vẽ" của `flows.md` kèm lý do (vd "module chỉ báo cáo, không có trạng thái"). Màn hình/UI flow **không** nằm trong bộ này; chỉ bật khi có `--ui` (để sau, nếu team cần).

## 5. Kiểm khớp giữa các sơ đồ (chỗ team code hay vấp)
Đoạn lệnh `python3` nhúng sẵn (như `ba-flow` hiện có), mỗi kiểm in `khớp/tổng` và danh sách thiếu:
| Kiểm | So sánh |
|---|---|
| K1 phủ luồng | mọi scenario + FR xuất hiện trong ≥ 1 D1/D2/D3 (đã có) |
| K2 trạng thái | tập trạng thái D2 = enum `status` trong D4/SRS = trạng thái trong FRD |
| K3 chuyển trạng thái | mỗi mũi tên D2 có ≥ 1 TC `ST`; mỗi TC `ST` ứng một mũi tên (kể cả chuyển không hợp lệ bị từ chối) |
| K4 trình tự | mọi endpoint ở D3 có trong bảng API của SRS và ngược lại (endpoint nào chưa có trong D3 phải thuộc luồng 1 module, không vượt ranh giới) |
| K5 dữ liệu | mọi trường request/response của SRS có thuộc tính trong D4 (đã có ở `ba-consistency` (c)) |
| K6 module | mọi mũi tên "→ module khác" ở D1/D3 có cạnh tương ứng trong D0 (`modules.md`) |

K1-K6 báo vào `consistency-report.md` (đã có cơ chế severity H/M/L): K2/K4 lệch = **H**, K3/K6 lệch = **M**.

## 6. Thay đổi cần làm (gọn, không thêm skill mới)
| File | Việc |
|---|---|
| `ba-conventions` | thêm mục "Bộ diagram": bảng mục 4, nguyên tắc mục 3, mẫu tối thiểu của mỗi loại |
| `ba-backbone` | `process-flows.md` thêm D0 bản đồ module; luồng mức dự án giữ ≤ 1 sơ đồ/quy trình lớn |
| `ba-flow` | sinh D1 + D2 + D3 theo điều kiện kích hoạt; mục "Không vẽ"; K1; mẫu cho từng loại |
| `ba-spec` | SRS: D4 bắt buộc nếu module sở hữu dữ liệu; enum trạng thái lấy đúng từ D2 |
| `ba-consistency` | thêm K2-K4, K6 (đã có K5) |
| `ba-gate` | giữ nguyên chiều/trọng số; hạ bậc nếu K2 hoặc K4 còn lệch (H) |
| `ba-testgen` | TC `ST` sinh trực tiếp từ mũi tên D2 (thay cho "chuyển trạng thái trong state diagram" chung chung) |
| `ba-export`, `ba-package` | giữ; sơ đồ đã là Mermaid, vẫn cần `mmdc` để render |
| `ba-guide` | bảng quyết định: chưa có D2/D3 khi điều kiện kích hoạt đúng thì gợi ý `flow` |

Không thêm lệnh mới: `/ba-start flow --module` vẫn là điểm vào.

## 7. Đánh đổi và rủi ro
- 5 loại là mức tối đa chấp nhận; thêm loại nữa (UI, deployment) sẽ lặp lại vấn đề "nhiều mà thừa".
- Mermaid không biểu diễn tốt swimlane lớn; ngưỡng 15 nút và tách quy trình con là cách giảm, không phải loại bỏ.
- K1-K6 dựa vào nhãn ID trong sơ đồ; BA/Claude quên gắn nhãn sẽ báo thiếu giả. Mẫu và kiểm phải đi cùng nhau.
- Chưa thử trên module thật; cần chạy lại ca mẫu `nghi-phep` (có state đơn nghỉ, điểm tích hợp `so-du-phep`) để xem số sơ đồ thực tế (kỳ vọng: 1 D0, 1-2 D1, 1 D2, 1 D3, 1 D4 cho module `don-nghi-phep`).

## 8. Thứ tự cài đặt đề xuất
1. `ba-conventions` (bảng, nguyên tắc, mẫu) 2. `ba-flow` (D1-D3 + K1) 3. `ba-spec` (D4, enum) 4. `ba-consistency` (K2-K4, K6) 5. `ba-backbone` (D0) 6. `ba-testgen`, `ba-gate`, `ba-guide` 7. chạy lại ca mẫu, đếm số sơ đồ và lỗi khớp.
