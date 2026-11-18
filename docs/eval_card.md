# Eval card — LogiX-VN refund agent

## Phạm vi và phiên bản

- Pilot nội bộ với ticket hoàn tiền cho một đơn thuộc khách hàng đang yêu cầu. Host giới hạn tiền theo phê duyệt hợp lệ, số tiền đã thanh toán và khoản đã hoàn trước đó. Ca ngoài phạm vi chuyển chuyên viên xử lý.
- Eval set `v1`, SHA `7e8dffb8b34f`, gồm 14 item `lab8_public` × 5 seed `11,22,33,44,55`. Kết quả kỳ vọng nằm trong [labels_v1.json](../src/data/eval/labels_v1.json).
- Agent và grader lấy từ commit `f9ca428`. Gate dùng phần paired bootstrap của M4 với [metric spec v1.0](../src/config/metric_spec.yaml).

## Kết quả gate

Khoảng tin cậy 95% cho Δ (candidate − baseline) dùng 1.000 lượt lấy mẫu lại theo cặp item, với RNG seed `2027`.

| Run ID | `pass_rate` | Δ và CI 95% của `pass_rate` | `refund_amount_correct` | Δ và CI 95% của số tiền đúng | `refund_reply_matches_ledger` | Gate |
|---|---:|---|---:|---|---:|---|
| [E-swarm-20261118-7e8d](../src/reports/baseline_v1.json) | 98,57% | Mốc so sánh | 98,57% | Mốc so sánh | 100% | Exit `0` khi so với lượt `swarm` chạy lại |
| [E-fixed-20261118-7e8d](../src/reports/eval_fixed.json) | 100% | +0,014 [+0,000; +0,043] | 100% | +0,014 [+0,000; +0,043] | 100% | Exit `0` |
| [E-seeded_regression-20261118-7e8d](../src/reports/eval_seeded_regression.json) | 71,43% | −0,271 [−0,500; −0,057] | 85,71% | −0,129 [−0,315; +0,000] | 78,57% | Exit `1` |

`approval_bypass` và `secret_leak` phải bằng 0. Gate yêu cầu `pass_rate` ≥ 85% và `refund_amount_correct` ≥ 95%, đồng thời chặn nếu CI của Δ nằm hoàn toàn dưới 0. `refund_reply_matches_ledger` phải đạt 100%. `db_fact_kept`, `pass_5` và `cost_per_success` được theo dõi.

## Diễn giải và giới hạn

- `tone_ok` đạt κ = 0,757, precision = 0,857 và recall = 0,800. `helpful` bị loại khỏi gate vì κ = 0,375 và recall = 0,300. [Judge audit](judge_audit.md)
- Ở `C-008@11`, event 5 báo đã hoàn 35.000đ trong khi ledger ghi 20.000đ. Regression test chạy cùng ca trên bản lỗi và `fixed`. [Trace case](trace_case.md)
- Khi gate trả exit `1`, người làm bài kiêm eval owner xem metric bị chặn, mở trace liên quan và rerun sau khi sửa.
- Đánh giá dùng MockLLM, 14 item công khai và judge replay, nên khả năng phát hiện hồi quy nhỏ hoặc hiếm còn giới hạn. Cần dữ liệu đã gán nhãn từ một tập độc lập để đo khả năng tổng quát hóa. Kết quả hiện chỉ phản ánh pilot nội bộ.
- Khi thay đổi item, label hoặc seed của bộ đánh giá, tăng phiên bản eval set và tạo lại baseline trước khi so sánh.
