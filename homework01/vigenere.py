def encrypt_vigenere(plaintext, keyword):
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    keyword = keyword.lower()
    index = 0
    for char in plaintext:
        if (ord(char) in range(65,91)) or (ord(char) in range(97,123)):
            res_sign = ord(char)+ord(keyword[index])-97
            if (ord(char) in range(65,91)):
                if (res_sign in range(65,91)):
                    ciphertext += chr(res_sign)
                else:
                    ciphertext += chr(res_sign-26)
            elif (ord(char) in range(97,123)):
                if (res_sign in range(97,123)):
                    ciphertext += chr(res_sign)
                else:
                    ciphertext += chr(res_sign-26)
            index += 1
            if index >= len(keyword):
                index = 0
        else:
            ciphertext += char
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    keyword = keyword.lower()
    index = 0
    for char in ciphertext:
        if (ord(char) in range(65,91)) or (ord(char) in range(97,123)):
            res_sign = ord(char)-(ord(keyword[index])-97)
            if (ord(char) in range(65,91)):
                if (res_sign in range(65,91)):
                    plaintext += chr(res_sign)
                else:
                    plaintext += chr(res_sign + 26)
            elif (ord(char) in range(97,123)):
                if (res_sign in range(97,123)):
                    plaintext += chr(res_sign)
                else:
                    plaintext += chr(res_sign + 26)
            index += 1
            if index >= len(keyword):
                index = 0
        else:
            plaintext += char
    return plaintext
