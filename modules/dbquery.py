import modules.dbconnection as run_query

class dbQuery:

    def __init__(self):
        db_file = None

    def write_to_sql(self, data):
        """ Write to sqlite db """
        hidnames = [data[0], data[1]] # To prepare data (fix if data contains ' or " that breaks)
        query = run_query.execute_query(f"SELECT COUNT(*) FROM bets WHERE hid=? AND name=?", hidnames)
        exists = query[0][0]
        if not exists:
            print(f"   [INSERT] Bonushunt #{data[0]}   {data[1]}")
            run_query.execute_query('INSERT INTO bets (hid, name, provider, bet, win, currency, mp, casino_name) VALUES (?,?,?,?,?,?,?,?)', data)

    def print_db(self):
        """ returns all data in list format """
        df = run_query.execute_query("SELECT * FROM bets")
        return df
