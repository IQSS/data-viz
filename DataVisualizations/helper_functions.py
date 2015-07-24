import pandas

def duplicates(all_var):
	seen = set()
	for i in all_var:
		seen.add(i)
		if i in seen:
			return True
	return False


def vars_valid(all_var, df_columns):

	for i in all_var:
		if i not in df_columns:
			return True
	return False

def all_var_numeric(var_list, data_frame):

	for i in var_list:
		if pandas.Series(data_frame[i]).dtype != 'float64' and pandas.Series(data_frame[i]).dtype != 'int64':
			return False
	return True