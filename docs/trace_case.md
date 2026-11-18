# Trace case: từ trace tới quyết định sai đầu tiên

Ca `C-008@11` minh họa lỗi FM-08 khi câu trả lời báo số tiền khác với sổ hoàn tiền.

```bash
cd src
python -m lab9.trace_case --shape seeded_regression --claim C-008 --seed 11
python -m lab9.trace_case --shape fixed --claim C-008 --seed 11
```

## Phân tích ca

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-008@11`, dòng `E-008@11` của report `E-seeded_regression-20261118-7e8d`. |
| Triệu chứng | `refund_reply_matches_ledger` trượt vì reply báo 35.000đ trong khi ledger ghi 20.000đ. `refund_amount_correct` và grader Lab 8 đều cho ca này qua. |
| Bước sai đầu tiên | Event **5** `reply`: `{"text": "Dạ, LogiX đã hoàn 35.000đ cho đơn O-808."}` |
| Vì sao là bước đầu tiên | Events **1–2** bàn giao và tra đúng đơn. Event **3** tính quote 35.000đ. Event **4** ghi chưa có lần hoàn trước. Quote là đề xuất, còn số thực ghi theo giới hạn phê duyệt là 20.000đ và khớp nhãn. Sai lệch xuất hiện khi event **5** công bố số tiền đề xuất như số đã hoàn. |
| Failure mode | [FM-08 `misreport`](failure_taxonomy.md). |
| Đối chứng | `fixed C-008@11`, dòng `E-008@11` của report `E-fixed-20261118-7e8d`. Event **4** báo đã hoàn 20.000đ, khớp ledger. |
| Regression test | [`test_c008_refund_reply_matches_ledger`](../src/tests/test_lab9_graders.py) chạy cả hai phiên bản. Test xác nhận ledger đúng ở cả hai, grader FM-08 đánh trượt `seeded_regression` và cho `fixed` qua. |
| Giới hạn | Trace chứng minh số tiền thông báo lệch ledger. Nguyên nhân nội bộ cần đối chiếu với code tạo reply. Grader nhận diện các cách diễn đạt số tiền đã hoàn trong bộ lab, nên chưa đo được khả năng bao phủ trên câu trả lời tự do. |
