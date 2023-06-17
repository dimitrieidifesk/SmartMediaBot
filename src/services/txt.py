import pyAesCrypt
from pathlib import Path

async def encrypt_txt(filename = 'some.txt', password = '1'):
    """Шифрование txt файла с заданным паролем"""
    txt_file = Path('./input/' + filename)
    new_file = f'./output/{txt_file.stem}.aes'
    pyAesCrypt.encryptFile(txt_file, new_file, password)
    return new_file

async def decrypt_txt(filename = 'some.aes', password = '1'):
    """Дешифрование aes файла с заданным паролем"""
    aes_file = Path('./input/' + filename)
    new_file = f'./output/{aes_file.stem}.txt'
    pyAesCrypt.decryptFile(aes_file, new_file, password)
    return new_file