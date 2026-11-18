# Judge audit

Chạy từ `src/` với nhãn `human` và `judge` đã lưu trong CSV.

```sh
python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 10
python -m lab9.judge --csv data/eval/judge_helpful_public.csv --audit 8
```

`FAIL` là lớp dương vì mục tiêu là phát hiện câu trả lời có lỗi. Ngưỡng đạt là κ ≥ 0,60, precision ≥ 0,80 và recall ≥ 0,70. Ma trận dùng nhãn người hiện có trong CSV.

| Tiêu chí | n | κ | Precision | Recall | TP / FP / FN / TN | Tỷ lệ lỗi theo judge → hiệu chỉnh Rogan–Gladen | Quyết định |
|---|---:|---:|---:|---:|---|---|---|
| `tone_ok` | 100 | 0,757 | 0,857 | 0,800 | 24 / 4 / 6 / 66 | 28% → 30% | Đạt cả ba ngưỡng, dùng cho giọng điệu |
| `helpful` | 100 | 0,375 | 1,000 | 0,300 | 9 / 0 / 21 / 70 | 9% → 30% | κ và recall dưới ngưỡng, loại khỏi gate |

## Audit thủ công

| Case | Judge | Người | Ai đúng? | Bằng chứng và thay đổi rubric đề xuất |
|---|---|---|---|---|
| `tone_ok` · `H-008` | PASS | FAIL | Người | Cách xưng «em … nha» quá suồng sã trong thông báo hoàn tiền. Thêm ví dụ đối chiếu cách xưng hô thân mật và cách xưng hô trung tính dùng trong CS. |
| `tone_ok` · `H-029` | PASS | FAIL | Người | «Không cần nhắn thêm» có giọng ra lệnh. Yêu cầu judge xét toàn câu, kể cả mệnh lệnh sau lời mở đầu lịch sự. |
| `tone_ok` · `H-042` | FAIL | PASS | Người | Câu ngắn vẫn lịch sự và nêu rõ khoản hoàn cùng thời gian dự kiến. Cho ví dụ đạt với phản hồi trung tính, ngắn gọn và không có lời xin lỗi. |
| `tone_ok` · `H-051` | FAIL | PASS | Người | Ghi chú cho biết CS LogiX chấp nhận từ «refund». Thêm ví dụ dùng thuật ngữ được phép trong câu tiếng Việt lịch sự. |
| `tone_ok` · `H-070` | PASS | FAIL | Người | Emoji cười trong phản hồi khiếu nại dễ bị hiểu là cợt nhả. Thêm tiêu chí về emoji theo ngữ cảnh khiếu nại. |
| `tone_ok` · `H-081` | FAIL | PASS | Judge theo ghi chú của CSV | Ghi chú nói người chấm đọc nhầm ticket. Chuyển ca này sang lượt gán nhãn thứ hai có kèm ticket trước khi sửa nhãn. Tách tiêu chí giọng điệu khỏi tiêu chí quyết định hoàn tiền. |
| `helpful` · `HL-015` | PASS | FAIL | Người | Reply báo 55.000đ, ledger ghi 40.000đ theo CSV. Đưa đối chiếu số tiền vào grader bằng code và ưu tiên kết quả đó khi tính hữu ích. |
| `helpful` · `HL-016` | PASS | FAIL | Người | Lời xin lỗi dài đi cùng số tiền sai, 55.000đ trong reply và 35.000đ trong ledger. Quy định lệch ledger là lỗi bắt buộc trượt ở tiêu chí chính xác. |
| `helpful` · `HL-047` | PASS | FAIL | Người | «Xử lý rồi» thiếu kết quả cụ thể và cách xưng hô lệch chuẩn trong nhãn. Yêu cầu rubric hữu ích nêu rõ kết quả hoặc bước tiếp theo, còn cách xưng hô chấm ở `tone_ok`. |

## Kết luận
- Judge `helpful` phát hiện 9 trong 30 lỗi theo nhãn người và bỏ sót 21 lỗi. Precision 1,000 nghĩa là cả 9 cảnh báo đều đúng trên bộ này. Recall 0,300 khiến judge bỏ lọt quá nhiều lỗi để dùng làm gate. Các kiểm tra số tiền và phê duyệt dùng grader bằng code.
- Rogan–Gladen ước lượng lại tỷ lệ lỗi chung dựa trên độ nhạy và độ đặc hiệu của judge. Các verdict từng ca và quyết định đạt ngưỡng giữ nguyên sau hiệu chỉnh.
- Kết quả đo trên CSV replay đã công khai. Sau khi sửa rubric, cần đo lại trên tập câu trả lời mới được người chấm gán nhãn.
