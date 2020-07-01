def make_table(title, headers, rows):
    """
    Convert a data frame into Enjin table format.

    :param title:
    :param headers:
    :param rows:
    :return: a string containing parse data in Enjin table format
    """
    str_list = []
    str_list.append('[size=5][b]{0}[/b][/size]'.format(title))
    str_list.append('[table]')
    for header in headers:
        str_list.append(format_header(header))

    for row in rows:
        gutter = row[0]
        if isinstance(row[0], int):
            gutter = str(row[0] + 1)
        str_list.append(format_enjin_row([gutter] + row[1:]))

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


def format_enjin_row(row_values):
    """
    Formats a row of data into enjin table format.

    :param row_values: a list of lists of values to be used as rows
    :return: a string corresponding to a row in enjin table format
    """
    row = '[tr][td]{0}[/td][/tr]'
    row_sep = '[/td][td]'
    return row.format(row_sep.join(row_values))


