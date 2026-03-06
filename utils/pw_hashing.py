import bcrypt

def hash_password(password:str):

    # Creating utf8 encoding, salt and then hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(entered_password:str , hashed_password:str):

    entered_password_bytes = entered_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    result = bcrypt.checkpw(entered_password_bytes, hashed_password_bytes)
    return result



# if __name__ == "__main__":
    password = "testpass123"
    hashed = hash_password(password)
    print(f"Plain: {password}")
    print(f"Hashed: {hashed}")
    
    verify_password(password, hashed)
    print("Password verification successful!")
