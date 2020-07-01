def make_table(title, headers, rows):
    gutter_width, cell_width = get_cell_widths(headers + rows)

    w = gutter_width + (len(rows[0]) - 1) * cell_width
    header_fmt = '{:_^' + str(w) + '}\n'
    str_list = [header_fmt.format(title)]

    gutter_fmt = '{:>' + str(gutter_width) + '} '
    cell_fmt = '{:' + str(cell_width) + '}'

    for r in headers + rows:
        gutter = r[0]
        if isinstance(r[0], int):
            gutter = str(r[0] + 1)
        str_list.append(gutter_fmt.format(gutter) + ''.join(cell_fmt.format(x) for x in r[1:]))

    return '\n'.join(str_list)


def get_cell_widths(rows):
    gutter = 0
    cell = 15
    for r in rows:
        gutter = max(gutter, len(str(r[0])))
        cell = max([cell] + [len(str(c)) for c in r[1:]])
    return gutter, cell

