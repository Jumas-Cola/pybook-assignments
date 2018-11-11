def encrypt_caesar(plaintext):
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for char in plaintext:
        if (ord(char) in range(65,91)) or (ord(char) in range(97,123)):
            if (ord(char)+3 in range(65,91)) or (ord(char)+3 in range(97,123)):
                ciphertext += chr(ord(char)+3)
            else:
                ciphertext += chr(ord(char)-26+3)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ''
    for char in ciphertext:
        if (ord(char) in range(65,91)) or (ord(char) in range(97,123)):
            if (ord(char)-3 in range(65,91)) or (ord(char)-3 in range(97,123)):
                plaintext += chr(ord(char)-3)
            else:
                plaintext += chr(ord(char)+26-3)
        else:
            plaintext += char
    return plaintext
