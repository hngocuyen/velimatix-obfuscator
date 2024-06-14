# velimatix-obfuscator
A best AST outsource obfuscation by ngocuyencoder and minhnguyen2412


<p align="center">
<img src="https://github.com/hngocuyen/velimatix-obfuscator/blob/main/img.png", width="5000", height="5000">
</p>

## Introduction

Hello everyone, I am Ngocuyencoder. Today, I am excited to introduce you to the outsourcing obfuscation project we have been working on for the past few months, called **Velimatix**. We have referred to and modified code from various obfuscation sources on GitHub, including **Dauricum**, **Hyperion**, and **Pycloak**, to create a solution tailored to our needs.

## Features

### Anti-Hooking
This feature ensures that our code is protected from hooking attempts. It is very robust, and its effectiveness is maximized by not publicly releasing the source code.

### Anti-Pycdc
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

### Anti-HTTPTookit and Proxy Systems
We have modified the source to include protections against HTTPToolkit and proxy systems. By applying our knowledge of hooking, we have developed an effective anti-system for these tools.

### AST (Abstract Syntax Tree) Modifications
We have incorporated various methods to protect and obfuscate the AST:

- **EXCEPTJ Method**: Based on the Dauricum method
- **BINASCII Method**: Inspired by the Hyperion method
- **BUILTINS.DICT Method**: Using the Pycloak method
- **STRING Method**: Custom-written by MinhNguyen, utilizing `eval(lambda ...)`

## Sources and Acknowledgments

We have drawn inspiration and code from the following GitHub repositories:
- **Dauricum**: For their methods in AST manipulation
- **Hyperion**: For their unique approaches to binary and ASCII protection
- **Pycloak**: For their innovative techniques in dictionary obfuscation

## Conclusion

Velimatix represents a culmination of the best practices and innovative techniques in code obfuscation. We believe it offers robust protection against various reverse-engineering and decompilation attempts. We hope you find it as powerful and useful as we have in our projects.

Thank you for your interest in Velimatix!

---

For any questions or further information, please feel free to contact us.

Ngocuyencoder and the Velimatix Team
