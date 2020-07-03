from mac0350.models import *
def build_check_str (table_name, pkey_val):
    check_str = str(pkey_val).replace(':', '=')\
                    .replace(' ', '').strip("{}").replace("'","")
    val  = ("SELECT count(*)\n"
            "FROM %s\n"
            "WHERE %s"
            % (table_name, check_str))
    print(val)
    return val
# Returns the SQL that will insert the values in the table
def build_insert_query (table_name, fields, values):
    f_str = ""
    v_str = "".join(str(values)[1:-1])
    if fields is not None:
        f_str = "".join(str(fields)[1:-1]).replace("'", "")
    insert_str = ("INSERT INTO %s (%s)\n"
                  "VALUES (%s)"
                  % (table_name, f_str, v_str))

    return insert_str

# Returns the SQL that will remove the values corredpondant to pkey from the table
def build_delete_query (table_name, pkey_val):
    check_str = str(pkey_val).replace(':', '=')\
                    .replace(' ', '').strip("{}").replace("'","")
    verify_value_exists = ("SELECT count(*)\n"
                            "FROM %s\n"
                            "WHERE %s"
                            % (table_name, check_str))
    remove_str = ("DELETE FROM %s\n"
                  "WHERE %s"
                  % (table_name, check_str))
    return remove_str

def get_columns (cursor, table_name):
    cursor.execute(("SELECT column_name\n"
                    "FROM INFORMATION_SCHEMA.COLUMNS\n"
                    "WHERE TABLE_NAME=N'%s'"
                    % table_name.lower()))
    columns = [val[0] for val in cursor.fetchall()]
    return columns