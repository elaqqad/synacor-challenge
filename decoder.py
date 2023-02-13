from array import array

data = array('H')
with open("Program\challenge.bin", "rb") as f:
    data.frombytes(f.read())

decrypted = array('H')

def my_char(a):
    try:
        result = chr(a)
        if not result.isascii() or (28 <= a <= 31):
            return ''
        if is_special(result):
            return result
        if (result.isalpha() or result.isnumeric() or result.isspace()):
            return result
        return ''
    except:
        return ''


def is_special(result):
    return result in '+-?_!?=\/,;:*.@"&@()[]%<>\''


for address in range(6068, 30050):
    content = data[address]               # [1730 ] rmem ra   ,rb
    address = (address ** 2) % 32768      # [1735 ] mult rb   ,rb   ,rb
    aux = content & address               # [2129 ] and  rc   ,ra   ,rb
    aux = aux ^ 32767                     # [2133 ] not  rc   ,rc
    content = content | address           # [2136 ] or   ra   ,ra   ,rb
    content = content & aux               # [2140 ] and  ra   ,ra   ,rc
    rb = 16724                            # [1741 ] set  rb   ,16724
    aux = content & rb                    # 2129
    aux = aux ^ 32767                     # 2133
    content = content | rb                # 2136
    content = content & aux               # 2140
    decrypted.append(content)             # 2144

start = 0
phrases = ["[6068 ]"]
while start < 30049-6068:
    as_char = my_char(decrypted[start])
    if (as_char != ''):
        phrases[-1] = phrases[-1] + as_char
    else:
        address = start + 6068
        if (len(phrases) >= 1 and phrases[-1].endswith(' ]')):
            phrases[-1] = "[" + str(address) + " ]"
        else:
            phrases.append("[" + str(address) + " ]")
    start = start + 1

start = 26851 - 6068
number = 0
while start < 30049-6068:
    number = decrypted[start]
    chunk = decrypted[start+1: start+number+1]
    start = start + number + 1
    if (number > 10):
        significant = chunk[0] // 256
        min_value = 3.0
        min_result = ['']
        min_key = 0
        for a in range(0, 256):
            key = significant * 256 + a
            result = [my_char(key ^ x) for x in chunk]
            non_chars = [c for c in result if (c == '')]
            specials = [c for c in result if is_special(c)]
            upper = [c for c in result if c.isupper()]

            heuristic = len(non_chars)/len(result) + \
                len(specials)/len(result) + len(upper)/len(result)
            if heuristic < min_value:
                min_value = heuristic
                min_result = result
                min_key = key
        phrases.append("[" + str(start + 6068) + "/" + str(min_key) +
                       "/" + str(number) + " ]" + repr(''.join(min_result)))
    else:
        phrases.append("[" + str(start + 6068) + "/" + str(number) + " ]")


with open("Dumps\phrases.txt", "w") as f:
    f.write('\n'.join(phrases) + '\n')
