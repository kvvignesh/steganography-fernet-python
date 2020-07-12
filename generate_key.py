from cryptography.fernet import Fernet

key = Fernet.generate_key()

file = open('key.key', 'wb')
file.write(key) # The key is type bytes still
file.close()