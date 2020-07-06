def make_table(title, headers, rows):
    """
    Convert a data frame into Enjin table format.

    :param title:
    :param headers:
    :param rows:
    :return: a string containing parse data in Enjin table format
    """
    str_list = []
    str_list.append(f'[size=5][b]{title}[/b][/size]')
    str_list.append('[table]')
    str_list += [format_header(header) for header in headers]
    str_list += [format_row(row) for row in rows]
    str_list.append('[/table]')

    return '\n'.join(str_list)


def format_header(header_values):
    """
    Formats a row of data with bolded values.

    :param header_values: a list of values to be used as headers
    :return: a string corresponding to a row in enjin table format
    """
    header = '[tr][td][b]{0}[/b][/td][/tr]'
    header_sep = '[/b][/td][td][b]'
    return header.format(header_sep.join(header_values))


def format_row(row_values):
    """
    Formats a row of data into enjin table format.

    :param row_values: a list of lists of values to be used as rows
    :return: a string corresponding to a row in enjin table format
    """
    gutter = row_values[0]
    if isinstance(row_values[0], int):
        gutter = str(row_values[0] + 1)

    row = '[tr][td]{0}[/td][/tr]'
    row_sep = '[/td][td]'

    return row.format(row_sep.join([gutter] + row_values[1:]))
