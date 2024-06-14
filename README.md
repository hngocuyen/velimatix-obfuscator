# #Velimatix Obfuscation 
A best AST outsource obfuscation by ngocuyencoder and minhnguyen2412


<p align="center">
<img src="https://github.com/hngocuyen/velimatix-obfuscator/blob/main/img.png", width="5000", height="5000">
</p>



## Language Selection / Chọn Ngôn Ngữ

- [English](#english)
- [Tiếng Việt](#ti%E1%BA%BFng-vi%E1%BB%87t)

---

## English

### Introduction

Hello everyone, I am Ngocuyencoder. Today, I am excited to introduce you to the outsourcing obfuscation project we have been working on for the past few months, called **Velimatix**. We have referred to and modified code from various obfuscation sources on GitHub, including **Dauricum**, **Hyperion**, and **Pycloak**, to create a solution tailored to our needs.

### Features

#### Anti-Hooking
This feature ensures that our code is protected from hooking attempts. It is very robust, and its effectiveness is maximized by not publicly releasing the source code.

#### Anti-Pycdc
Our obfuscation effectively counters Pycdc (Python Decompiler). Although some have attempted to customize Pycdc to bypass our anti-measures, they have been unsuccessful. Here’s an example of typical bypass code:
```python
try:
    pass
except:
    pass
finally:
    pass
```
Even though such methods can bypass other protections, they do not succeed against our anti-measures.

#### Anti-HTTPTookit and Proxy Systems
We have modified the source to include protections against HTTPToolkit and proxy systems. By applying our knowledge of hooking, we have developed an effective anti-system for these tools.

#### AST (Abstract Syntax Tree) Modifications
We have incorporated various methods to protect and obfuscate the AST:

- **EXCEPTJ Method**: Based on the Dauricum method
- **BINASCII Method**: Inspired by the Hyperion method
- **BUILTINS.DICT Method**: Using the Pycloak method
- **STRING Method**: Custom-written by MinhNguyen, utilizing `eval(lambda ...)`

### Sources and Acknowledgments

We have drawn inspiration and code from the following GitHub repositories:
- **Dauricum**: For their methods in AST manipulation
- **Hyperion**: For their unique approaches to binary and ASCII protection
- **Pycloak**: For their innovative techniques in dictionary obfuscation

### Conclusion

For any questions or further information, please feel free to contact us.

Ngocuyencoder and Nguyenminh2412

---

## Tiếng Việt

### Giới thiệu

Xin chào tất cả mọi người, tôi là Ngocuyencoder. Hôm nay tôi sẽ giới thiệu cho mọi người về dự án outsource obfuscation mà bọn tôi đã thực hiện trong vài tháng qua, gọi là **Velimatix**. bọn tôi đã tham khảo và sửa đổi mã từ các nguồn obfuscation trên GitHub, bao gồm **Dauricum**, **Hyperion**, và **Pycloak**, để tạo ra một giải pháp phù hợp với nhu cầu của bọn tôi.

### Các tính năng

#### Anti-Hooking
Tính năng này đảm bảo mã của bọn tôi được bảo vệ khỏi hooking (có lẽ sau khi public source này thì hết bảo đảm rồi)

#### Anti-Pycdc
Obfuscation của bọn tôi chống lại Pycdc (PYC Decompiler) rất hiệu quả. Mặc dù có người đã cố gắng tùy chỉnh Pycdc để vượt qua anti của bọn tôi, nhưng không thành công. Dưới đây là một ví dụ về mã bypass thông thường:
```python
try:
    pass
except:
    pass
finally:
    pass
```
Mặc dù các method như vậy có thể bypass được các bảo vệ khác, nhưng không thể vượt qua được anti của bọn tôi.

#### Anti-HTTPTookit và Hệ thống Proxy
Hãy sửa đổi mã nguồn của Velimatix để thêm tính năng này vào

#### Sửa đổi AST (Abstract Syntax Tree)
bọn tôi đã kết hợp nhiều method để bảo vệ và obfuscate AST:

- **method EXCEPTJ**: Dựa trên method Dauricum
- **method BINASCII**: Lấy cảm hứng từ method Hyperion
- **method BUILTINS.DICT**: Sử dụng method Pycloak
- **method STRING**: Viết bởi MinhNguyen, sử dụng `eval(lambda ...)`

### Nguồn và Lời cảm ơn
bọn tôi đã lấy cảm hứng và mã từ các kho GitHub sau:
- **Dauricum**: method thao tác AST 
- **Hyperion**: method binascii và vars
- **Pycloak**: method `__builtins__.__dict__`

### Kết luận

For any questions or further information, please feel free to contact us.

ngocuyencoder and Nguyenminh2412
