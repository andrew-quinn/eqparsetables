def humanize(s):
    suffix = ['', 'k', 'm', 'bn', 'tn']

    try:
        n = float(s)
    except ValueError:
        return s

    if n < 1000:
        return str(s)

    mag = 0
    while n > 1000:
        n /= 1000.0
        mag += 1

    return f'{n:.1f}{suffix[mag]}'
