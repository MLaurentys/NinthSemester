def build_check_str (table_name, pkey_val):
	check_str = str(pkey_val).replace(':', '=')\
					.replace(' ', '').strip("{}").replace("'","")
	return ("SELECT count(*)\n"
			"FROM %s\n"
			"WHERE %s"
			% (table_name, check_str))

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

# Returns the SQL that will update the values corredpondant to pkey from the table
def build_update_query (table_name, fields, values, pkey_val):
	check_str = str(pkey_val).replace(':', '=')\
					.replace(' ', '').strip("{}").replace("'","")
	if values[0] == "NULL":
		fv_str = str(fields[0]).replace("'", "") + "=" + str(values[0])
	else:
		fv_str = str(fields[0]).replace("'", "") + "=" + "'" + str(values[0]) + "'"
	for i in range(1, len(fields)):
		if values[i] == "NULL":
			fv_str += ", " + str(fields[i]) + "=" + str(values[i])
		else:
			fv_str += ", " + str(fields[i]) + "=" + "'" + str(values[i]) + "'"
	update_str = ("UPDATE %s\n"
				  "SET %s\n"
				  "WHERE %s"
				  % (table_name, fv_str, check_str))
	return update_str
