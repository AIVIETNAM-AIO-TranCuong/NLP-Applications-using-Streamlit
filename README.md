# Project 1.1 - Streamlit NLP Application

Ứng dụng này là một demo dự án NLP bằng Streamlit

## Mô tả

Ứng dụng gồm hai chức năng chính:

- **Dịch văn bản**: nhận văn bản đầu vào và dịch sang ngôn ngữ đích được chọn.
- **Sửa lỗi chính tả**: kiểm tra và sửa lỗi chính tả cho văn bản trong các ngôn ngữ được pyspellchecker hỗ trợ.

## Nội dung dự án

- `app.py`: file ứng dụng Streamlit chính.
- `.venv/`: môi trường ảo Python nếu có.

## Yêu cầu cài đặt

Cài đặt Python 3.11 hoặc cao hơn.

Nếu chưa có thư viện, chạy:

```powershell
python -m pip install streamlit langdetect pyspellchecker nltk langcodes deep-translator
```

Ngoài ra, nếu dùng môi trường ảo, kích hoạt trước khi cài.

## Cách chạy

1. Cài các thư viện cần thiết (nếu chưa cài):

```powershell
python -m pip install streamlit langdetect pyspellchecker nltk langcodes deep-translator
```

2. Chạy ứng dụng Streamlit:

```powershell
streamlit run app.py
```

3. Mở trình duyệt theo đường dẫn được hiển thị trong terminal, thường là:

```text
http://localhost:8501
```

4. Nhập dữ liệu và nhấn nút `Dịch` hoặc `Kiểm tra` để xem kết quả.

## Chức năng ứng dụng

1. **Dịch văn bản**
   - Nhập câu hoặc đoạn văn vào ô text.
   - Chọn ngôn ngữ đích.
   - Nhấn nút `Dịch` để dịch.
   - Hiển thị ngôn ngữ nguồn, ngôn ngữ đích và kết quả dịch.

2. **Sửa lỗi chính tả**
   - Nhập câu hoặc đoạn văn vào ô text.
   - Nhấn nút `Kiểm tra` để chạy sửa lỗi.
   - Ứng dụng sẽ nhận diện ngôn ngữ và sửa lỗi với pyspellchecker.
   - Hiển thị ngôn ngữ phát hiện được và câu đã sửa.

## Lưu ý

- `deep-translator` cần kết nối internet để dịch.
- `pyspellchecker` không hỗ trợ tiếng Việt tốt, nên chỉ dùng chắc chắn với các ngôn ngữ trong `SPELL_LANGS`.
- Nếu cần bổ sung thêm tính năng, có thể mở rộng `app.py` và thêm các tab hoặc API xử lý khác.