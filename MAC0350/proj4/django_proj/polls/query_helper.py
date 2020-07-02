def build_insert_query (table_name, fields, values):
    f_str = ""
    v_str = "".join(str(values)[1:-1])
    if fields is not None:
        f_str = "".join(str(fields)[1:-1]).replace("'", "")
    return ("INSERT INTO %s (%s)\n"
            "VALUES (%s)"
            % (table_name, f_str, v_str))