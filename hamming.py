def splitData(data, length):
    arr = []

    for i in range(0, len(data), length):
        arr.append(data[i:i+length])

    return arr


def encode(data, controlBitsNumber):
    s = insertZeroControlBits(data, controlBitsNumber)
    s = calculateControlBits(s, controlBitsNumber)
    return s


def decode(data, r):
    res = data[:-1]

    for i in range(r):
        pos = 2 ** i - 1
        res = changeChar(res, pos, '*')

    res = res.replace('*', '')

    return res


def controlBitsNumber(word):
    for i in range(word):
        if 2 ** i >= word + i + 1:
            return i

def insertZeroControlBits(data, controlBitsNumber):
    res = data

    for i in range(controlBitsNumber):
        pos = 2 ** i - 1
        res = res[:pos] + '0' + res[pos:]

    return res


def changeChar(string, position, value):
    s = list(string)
    s[position] = value
    s = ''.join(s)

    return s


def correctError(data, position):

    if isinstance(position, str):
        return position

    if data[position - 1] == '1':
        fix = '0'
    else:
        fix = '1'
    data = changeChar(data, position - 1, fix)

    return data


def detectErrors(data, controlBitsNumber):
    temp = data[:-1]
    sum = 0

    for i in range(controlBitsNumber):
        position = 2 ** i - 1
        t = ''

        for j in range(position, len(temp), (position + 1) * 2):
            t = t + temp[j:j + position + 1]

        t = t[1:]
        t = t.replace('0', '')

        if temp[position] != str(len(t) % 2):
            sum += position + 1

    if sum == 0:
        return None
    elif len(data.replace('0', '')) % 2 == 0:
        return -1

    return sum


def calculateControlBits(data, controlBitsNumber):

    for i in range(controlBitsNumber):
        position = 2 ** i - 1
        t = ''

        for j in range(position, len(data), (position + 1) * 2):
            t = t + data[j:j + position + 1]
        t = t.replace('0', '')
        if len(t) % 2 == 1:
            data = changeChar(data, position, '1')

    data += str(len(data.replace('0', '')) % 2)

    return data
