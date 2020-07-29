_chars = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h',
          'i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
          'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',
          'S','T','U','V','W','X','Y','Z',' ',',','.','?','!']  # length = 67 (0-66)

_chunk_size = 4


def _find_index(char):
    for i in range(len(_chars)):
        if char == _chars[i]:
            return i


def _complete_block(block):
    while len(block) % _chunk_size != 0:
        block += ' '
    return block


def get_key():
    from random import randrange
    key = []
    for i in range(_chunk_size):
        key.append(randrange(len(_chars)))
    key.append(randrange(len(_chars) - 2))
    return key


def _plain_to_block(plain_txt):
    block_txt = []
    for i in range(len(plain_txt) // _chunk_size):
        temp_lst = []
        for j in range(i * _chunk_size, (i * _chunk_size) + _chunk_size):
            temp_lst.append(plain_txt[j + (i // _chunk_size)])
        block_txt.append(temp_lst)
    block_txt.append(0)    
    return block_txt


def encrypt_block(block_txt, private_key):
    for i in range(len(block_txt) - 1):
        if i == 0:
            shift = block_txt[i][0]
        else:
            shift = block_txt[i - 1][0]
        for j in range(_chunk_size):
            if block_txt[i][j] in _chars:
                index = (_find_index(block_txt[i][j]) + private_key[j] + _find_index(shift))
                block_txt[i][j] = _chars[index % len(_chars)]
                if j == 0 and i == 0:
                    temp = index // len(_chars)
                    block_txt[len(block_txt) - 1] = _chars[temp + private_key[len(private_key) - 1]]
    return block_txt


def decrypt_block(block_txt, private_key):
    decode_txt = []
    length = len(block_txt) - 1
    rounds = _find_index(block_txt[len(block_txt) - 1]) - private_key[len(private_key) - 1]
    for i in range(length): 
        for j in range(_chunk_size):
            if i == 0:                  
                temp_reverse = _find_index(block_txt[i][0]) + (len(_chars) * rounds) - private_key[0]
                temp_shift = (temp_reverse // 2 + (temp_reverse % 2)) % len(_chars)
                shift = temp_shift
            else:
                shift = _find_index(block_txt[i - 1][0])
            char_position = _find_index(block_txt[i][j]) - private_key[j] - shift
            if char_position < 0:
                char_position += len(_chars)
            decode_txt.append(_chars[char_position])
    return decode_txt


def main():
    plain_txt = _complete_block(input('Input Text For Encryption\n'))
    private_key = get_key()
    print('Before Encryption:', plain_txt)
    block_txt = _plain_to_block(plain_txt)
    encrypt_block(block_txt, private_key)
    print('After Encryption:', ''.join(char for sublist in block_txt for char in sublist))
    decrypted_txt = decrypt_block(block_txt, private_key)
    print('After Decryption:', ''.join(decrypted_txt))


if __name__ == '__main__':
    main()
