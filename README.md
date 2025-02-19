# ChatPot RAG

**Nhóm tác giả**
- Vũ Văn Thanh
- Nguyễn Quốc Khánh
- Nguyễn Viết Doanh

## Mục lục

* [Giới thiệu về ChatPot](#Giới-thiệu-về-ChatPot)
* [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
* [Thiết lập môi trường](#thiết-lập-môi-trường)
* [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)

## Giới thiệu về ChatPot 

ChatPot là một sản phẩm tìm kiếm thông tin, có khả năng xử lý tài liệu được cung cấp để trích xuất câu trả lời. Khi bạn nhập tài liệu vào, hệ thống sẽ đọc và phân loại nội dung để đưa ra câu trả lời phù hợp. Sản phẩm này giúp cải thiện hiệu quả tìm kiếm và hỗ trợ quá trình tra cứu thông tin một cách trực tiếp.

## Yêu cầu hệ thống

* `Operating Systems: Windows`
* `Python 3.6+`

## Thiết lập môi trường

Tải project bằng cách sử dụng lệnh `git clone`

```

```

Tạo môi trường mới và cài đặt các gói liên quan

```
```

## Hướng dẫn sử dụng

Chạy chương trình chatbot trên VScode

`**Bước 1: Khởi động backend**`

Vào file crs\main.py

```
uvicorn src.main:app --reload --port 8001
```

`**Bước 2: Khởi động frontend**`

Thực thi file templates\index.html bằng cách khởi chạy live server

**Hoàn thành!!!**

Sau đó, mở trình duyệt, vào đường dẫn [http://127.0.0.1:8001] để bắt đầu đặt câu hỏi với bot.
