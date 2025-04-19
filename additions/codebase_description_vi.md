# Mô tả Codebase

Tài liệu này cung cấp mô tả chi tiết về từng file và folder trong codebase, có tham chiếu đến các bước liên quan trong bài báo "Reformulating Unsupervised Style Transfer as Paraphrase Generation".

## Top-Level Files and Folders

*   `.gitignore`: Chỉ định các file không được Git theo dõi.
*   `demo_paraphraser.py`: Hiện thực hóa bản demo dòng lệnh để paraphrase các câu đơn bằng mô hình GPT-2 đã được huấn luyện trước (Section 3 trong bài báo).
*   `description_en.md`: File này (mô tả codebase bằng tiếng Anh).
*   `description_vi.md`: Mô tả codebase bằng tiếng Việt.
*   `LICENSE`: Chứa thông tin về giấy phép cho codebase.
*   `paraphrase_many.py`: Hiện thực hóa một script để paraphrase nhiều câu từ một file đầu vào và ghi kết quả vào một file khác (Section 3 trong bài báo).
*   `README_terminal_demo.md`: Cung cấp hướng dẫn về cách chạy bản demo dòng lệnh.
*   `README-multilingual.md`: Cung cấp chi tiết về các bộ phân loại đa ngôn ngữ để đánh giá hình thức.
*   `README.md`: Cung cấp tổng quan chung về dự án, bao gồm hướng dẫn thiết lập, thông tin về dataset và quy trình huấn luyện/đánh giá.
*   `requirements.txt`: Liệt kê các gói Python cần thiết để chạy codebase.
*   `setup.py`: Xác định metadata của gói và các tùy chọn cài đặt.
*   `data_samples/`: Chứa các file dữ liệu mẫu cho các style khác nhau (ví dụ: Shakespeare, Tweets, Bible).
*   `datasets/`: Chứa các script để chuẩn bị dataset cho quá trình huấn luyện và đánh giá (Section 4 trong bài báo).
*   `mturk_evals/`: Chứa dữ liệu và script cho các đánh giá Mechanical Turk (Section 3 trong bài báo).
*   `outputs/`: Chứa các output được tạo bởi mô hình và baseline.
*   `papers/`: Chứa bài báo nghiên cứu và slide.
*   `style_paraphrase/`: Chứa code cốt lõi cho mô hình chuyển đổi style, bao gồm diverse paraphraser, các mô hình inverse paraphrase và các script huấn luyện/đánh giá.
*   `web-demo/`: Chứa code cho bản demo web.

## Detailed Description of Key Folders and Files

### `data_samples/`

*   `aae.txt`: Dữ liệu mẫu theo style tiếng Anh-Mỹ gốc Phi.
*   `bible.txt`: Dữ liệu mẫu theo style Kinh thánh.
*   `coha_1810-1830.txt`: Dữ liệu mẫu từ Corpus of Historical American English (1810-1830).
*   `coha_1890-1910.txt`: Dữ liệu mẫu từ Corpus of Historical American English (1890-1910).
*   `coha_1990-2000.txt`: Dữ liệu mẫu từ Corpus of Historical American English (1990-2000).
*   `english_tweets.txt`: Dữ liệu mẫu theo style Tweet tiếng Anh.
*   `joyce.txt`: Dữ liệu mẫu từ các tác phẩm của James Joyce.
*   `lyrics.txt`: Dữ liệu mẫu theo style Lyrics.
*   `README.md`: Mô tả nội dung của thư mục `data_samples`.
*   `romantic_poetry.txt`: Dữ liệu mẫu theo style Romantic Poetry.
*   `shakespeare.txt`: Dữ liệu mẫu theo style Shakespeare.
*   `switchboard.txt`: Dữ liệu mẫu từ Switchboard corpus (hội thoại).

### `datasets/`

*   `bpe2text.py`: Chuyển đổi một file BPE trở lại dạng text thô ban đầu (được sử dụng trong quá trình tiền xử lý dữ liệu).
*   `dataset_config.py`: Chứa các cài đặt cấu hình cho các dataset khác nhau.
*   `prepare_paraphrase_data.py`: Tiền xử lý dữ liệu TSV gồm các cặp câu để có định dạng tương thích cho việc huấn luyện paraphrase (Section 2.1 trong bài báo).
*   `style_dataset.py`: Định nghĩa các class `ParaphraseDatasetText` và `InverseParaphraseDatasetText`, được sử dụng để tải và xử lý dữ liệu cho việc huấn luyện mô hình paraphrase và các mô hình inverse paraphrase.

### `mturk_evals/`

Thư mục này chứa dữ liệu và kết quả từ các đánh giá Mechanical Turk được sử dụng để đánh giá chất lượng của các mô hình chuyển đổi style (Section 3 trong bài báo).

### `outputs/`

Thư mục này chứa các output được tạo bởi mô hình và baseline.

### `papers/`

*   `EMNLP 2020 Slides.pdf`: Chứa các slide được trình bày tại EMNLP 2020.
*   `Reformulating Unsupervised Style Transfer as Paraphase Generation.pdf`: Chứa bài báo nghiên cứu.

### `style_paraphrase/`

*   `__init__.py`: Một file trống cho biết thư mục `style_paraphrase` là một gói Python.
*   `args.py`: Xác định các đối số dòng lệnh cho các script huấn luyện và đánh giá.
*   `data_utils.py`: Chứa các hàm tiện ích để tải, tiền xử lý và tạo batch dữ liệu (Section 2.1 và 2.2 trong bài báo).
*   `dataset_config.py`: Chứa các cài đặt cấu hình cho các dataset khác nhau.
*   `hyperparameters_config.py`: Xác định các siêu tham số cho quá trình huấn luyện.
*   `inference_utils.py`: Chứa class `GPT2Generator`, được sử dụng để tạo paraphrase và thực hiện chuyển đổi style (Section 2.3 trong bài báo).
*   `run_evaluate_gpt2_template.sh`: Một script template để đánh giá mô hình GPT-2.
*   `run_finetune_gpt2_template.sh`: Một script template để fine-tune mô hình GPT-2.
*   `run_lm_finetuning.py`: Hiện thực hóa quá trình fine-tuning language model (Section 2.3 trong bài báo).
*   `schedule.py`: Chứa code để lên lịch và chạy các thí nghiệm trên một cluster SLURM.
*   `style_dataset.py`: Định nghĩa các class `ParaphraseDatasetText` và `InverseParaphraseDatasetText`, được sử dụng để tải và xử lý dữ liệu cho việc huấn luyện mô hình paraphrase và các mô hình inverse paraphrase (Section 2.1 và 2.2 trong bài báo).
*   `utils.py`: Chứa các hàm tiện ích để khởi tạo mô hình GPT-2, lấy mẫu sequence và thực hiện beam search (Section 2.3 trong bài báo).
*   `style_classify/`: Chứa code để huấn luyện và đánh giá các bộ phân loại style (Section 3 trong bài báo).
*   `evaluation/`: Chứa code để đánh giá các mô hình chuyển đổi style (Section 3 trong bài báo).
*   `examples/`: Chứa các script ví dụ để chạy các quy trình huấn luyện và đánh giá.

### `web-demo/`

*   `clean_queue.py`: Một script có thể được sử dụng để xóa hàng đợi xử lý cho bản demo web.
*   `config.json`: Chứa các cài đặt cấu hình cho bản demo web, chẳng hạn như đường dẫn mô hình và các API endpoint.
*   `demo_service.py`: Hiện thực hóa logic backend cho bản demo web, xử lý các request và tạo paraphrase.
*   `LICENSE`: Chứa thông tin về giấy phép cho bản demo web.
*   `README.md`: Cung cấp hướng dẫn về cách thiết lập và chạy bản demo web.
*   `setup.sh`: Một shell script có thể cài đặt các dependency cần thiết và thiết lập môi trường cho bản demo web.
*   `strap-backend/`: Chứa code backend cho bản demo web.
    *   `app.py`: Hiện thực hóa ứng dụng Flask phục vụ bản demo web.
    *   `waitress_server.py`: Có thể được sử dụng để chạy ứng dụng Flask bằng máy chủ Waitress WSGI.
*   `strap-frontend/`: Chứa code frontend cho bản demo web.
    *   `.gitignore`: Chỉ định các file không được Git theo dõi.
    *   `package-lock.json`: Ghi lại các phiên bản chính xác của các dependency được sử dụng trong dự án frontend.
    *   `package.json`: Xác định các dependency và script cho dự án frontend.
    *   `README.md`: Cung cấp hướng dẫn về cách thiết lập và chạy frontend.
    *   `public/`: Chứa các tài sản tĩnh cho frontend, chẳng hạn như các file HTML, CSS và JavaScript.
*   `strap-landing/`: Có thể chứa code cho một trang đích cho bản demo web.

## Key Files and Their Relation to the STRAP Method

*   `style_paraphrase/inference_utils.py`: File này chứa class `GPT2Generator`, là thành phần cốt lõi của phương pháp STRAP. Nó hiện thực hóa các quy trình diverse paraphrasing và chuyển đổi style (Section 2.3 trong bài báo).
*   `style_paraphrase/run_lm_finetuning.py`: File này hiện thực hóa quy trình fine-tuning cho các mô hình inverse paraphrase (Section 2.3 trong bài báo).
*   `style_paraphrase/utils.py`: File này chứa các hàm tiện ích để khởi tạo mô hình GPT-2, lấy mẫu sequence và thực hiện beam search (Section 2.3 trong bài báo).
*   `datasets/prepare_paraphrase_data.py`: File này hiện thực hóa quy trình lọc dữ liệu để tăng tính đa dạng trong mô hình paraphrase (Section 2.1 trong bài báo).
