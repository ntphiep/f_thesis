# Mô tả về Implementation của Text Style Paraphraser

## Problem Definition (Định nghĩa Bài toán)

Bài toán là chuyển đổi *style* của văn bản trong khi vẫn giữ nguyên *meaning* của nó. Các mô hình hiện tại thường làm thay đổi *meaning* của câu gốc.

## Proposed Solution (Giải pháp Đề xuất)

Chuyển bài toán thành bài toán sinh văn bản *paraphrase generation*.

## Method (Phương pháp): STRAP (Style Transfer via Paraphrasing)

STRAP là một phương pháp *unsupervised style transfer* mô hình hóa bài toán như một bài toán *controlled paraphrase generation*. Nó không yêu cầu dữ liệu song song giữa các *style* khác nhau và tiến hành theo ba giai đoạn đơn giản:

1.  Tạo dữ liệu giả song song bằng cách đưa các câu từ các *style* khác nhau qua một mô hình *diverse paraphrase*.
2.  Huấn luyện các mô hình "*inverse paraphrase*" riêng cho từng *style* để chuyển đổi các câu đã *paraphrase* trở lại *style* gốc.
3.  Sử dụng mô hình "*inverse paraphrase*" cho *style* mong muốn để thực hiện chuyển đổi *style*.

## Step-by-Step Details (Chi tiết từng bước)

1.  **Creating Pseudo-Parallel Data (Tạo Dữ liệu Giả Song song):**
    *   Mục tiêu là chuẩn hóa các câu đầu vào bằng cách loại bỏ thông tin dự đoán *style* gốc của nó.
    *   Cho mỗi câu x từ *style* i (x ∈ X_i), tạo ra một *paraphrase* z bằng cách sử dụng mô hình *pre-trained paraphrase* f_para:
        *   `z = f_para(x)` where `x ∈ X_i`
    *   Điều này tạo ra một tập dữ liệu Z_i gồm các câu đã chuẩn hóa và cho phép chúng ta tạo một *corpus* giả song song (X_i, Z_i) giữa mỗi câu gốc và phiên bản *paraphrase* của nó.
    *   **Implementation:**
        *   Mô hình *diverse paraphraser* `f_para` được hiện thực hóa bằng cách sử dụng mô hình GPT-2 đã được *fine-tune*. Xem `style_paraphrase/inference_utils.py` (GPT2Generator class).
        *   Quá trình lọc dữ liệu để tăng tính đa dạng được hiện thực hóa trong `datasets/prepare_paraphrase_data.py`.
    *   **Data Source:** *Filtered* ParaNMT-50M *corpus*.

2.  **Training the "Inverse Paraphrase" Model (Huấn luyện Mô hình "Inverse Paraphrase"):**
    *   Mục tiêu là huấn luyện một mô hình riêng cho từng *style* để cố gắng tái tạo lại câu gốc x từ *paraphrase* z của nó.
    *   Mô hình *inverse paraphrase* f_inv_i cho *style* i học cách tái tạo lại *corpus* gốc X_i bằng cách sử dụng mục tiêu *language modeling* tiêu chuẩn với *cross-entropy loss* L_CE:
        *   `x_hat = f_inv_i(z)` where `z ∈ Z_i`
        *   `loss = Σ x∈X_i L_CE(x, x_hat)`
    *   **Implementation:**
        *   Các mô hình *inverse paraphrase* được hiện thực hóa bằng cách sử dụng các mô hình GPT-2 đã được *fine-tune*. Xem `style_paraphrase/run_lm_finetuning.py`.
        *   `GPT2ParentModule` class trong `style_paraphrase/utils.py` định nghĩa *forward pass* và tính toán *loss*.
    *   **Fine-tuning:**
        *   Các mô hình GPT-2 được *fine-tune* bằng cách sử dụng *learning rate* nhỏ (ví dụ: 5e-5) và *Adam optimizer*.
        *   *Early stopping* được sử dụng dựa trên *perplexity* của tập *validation*.
        *   Quá trình huấn luyện được định nghĩa trong hàm `train` trong `style_paraphrase/run_lm_finetuning.py`.

3.  **Style Transfer (Chuyển đổi Phong cách):**
    *   Cho một câu s bất kỳ (trong bất kỳ *style* nào), chuyển đổi nó thành một câu s_j trong *style* mục tiêu j bằng cách sử dụng quy trình hai bước: chuẩn hóa *style* với f_para, sau đó là tạo *style* với *inverse paraphraser* f_inv_j:
        *   `s_j = f_inv_j(f_para(s))`
    *   **Implementation:**
        *   `GPT2Generator` class trong `style_paraphrase/inference_utils.py` hiện thực hóa quy trình chuyển đổi *style*.
        *   Hàm `generate` gọi *diverse paraphraser* và mô hình *inverse paraphrase* thích hợp.

## Evaluation (Đánh giá)

*   Sử dụng các *metrics* để đánh giá chất lượng của việc chuyển đổi *style*, bao gồm:
    *   *Accuracy* (Độ chính xác): Đo lường mức độ thành công trong việc chuyển đổi *style*.
    *   *Similarity* (Độ tương đồng): Đo lường mức độ tương đồng về *meaning* giữa câu gốc và câu đã chuyển đổi.
    *   *Fluency* (Độ trôi chảy): Đo lường mức độ trôi chảy và tự nhiên của câu đã chuyển đổi.
*   Đề xuất một phương pháp đánh giá mới, kết hợp các *metrics* trên ở cấp độ câu (*sentence-level aggregation*) để đánh giá toàn diện hơn.
*   Sử dụng một tập dữ liệu mới (CDS) với 15 triệu câu và 11 *style* khác nhau để đánh giá mô hình.

## Code Implementation Details (Chi tiết về Implementation Code)

Dưới đây là cách các công thức chính được hiện thực hóa trong code:

*   **Top-k và Top-p filtering:** Được hiện thực hóa trong hàm `top_k_top_p_filtering` tại `style_paraphrase/utils.py`.
    *   Đầu vào: `logits` (*logits* distribution), `top_k`, `top_p`.
    *   Nếu `top_p > 0`:
        *   Sắp xếp `logits` và tính *cumulative probability*:
            ```python
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probs = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)
            ```
        *   Xác định các token cần loại bỏ:
            ```python
            sorted_indices_to_remove = cumulative_probs > top_p
            ```
        *   Loại bỏ các token:
            ```python
            indices_to_remove = sorted_indices_to_remove.scatter(dim=1, index=sorted_indices, src=sorted_indices_to_remove)
            logits[indices_to_remove] = filter_value
            ```
    *   Nếu `top_k > 0`:
        *   Xác định các token cần loại bỏ:
            ```python
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            ```
        *   Loại bỏ các token:
            ```python
            logits[indices_to_remove] = filter_value
            ```
*   **Sampling sequence:** Được hiện thực hóa trong hàm `sample_sequence` tại `style_paraphrase/utils.py`.
    *   Sử dụng hàm `get_logits` để lấy *logits* cho *token* tiếp theo.
    *   Áp dụng `top_k_top_p_filtering` lên *logits*.
    *   Lấy mẫu *token* tiếp theo bằng `torch.multinomial`.
*   **Beam search:** Được hiện thực hóa trong hàm `beam_search` tại `style_paraphrase/utils.py`.
    *   Sử dụng hàm `get_logits` để lấy *logits* cho *token* tiếp theo.
    *   Chọn `beam_size` *token* tốt nhất.
    *   Tiếp tục mở rộng *beam* cho đến khi đạt độ dài tối đa hoặc gặp *token* kết thúc câu.

## Summary (Tóm tắt)

Phương pháp này giúp cải thiện khả năng bảo toàn *meaning* trong quá trình chuyển đổi *style* văn bản, đồng thời đạt được kết quả tốt trên các tập dữ liệu khác nhau.
