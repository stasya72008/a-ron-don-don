def number_format(num):
    num = num.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
    if num.startswith('0'):
        num = '38' + num
    return num
