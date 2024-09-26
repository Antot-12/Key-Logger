from cryptography.fernet import Fernet

# Генерація ключа
key = Fernet.generate_key()
print(f"Ваш новий шифрувальний ключ: {key.decode()}")

