import modules

""" Examples """

def main() -> None:

    """
    dbquery = modules.dbQuery()
    print([row[3] for row in dbquery.print_db()])

    print()

    filehandler = modules.Filehandler()
    filehandler.run()
    """

    crawler = modules.Crawler()
    crawler.getToken() # First get a valid bearer token
    crawler.getLatestHunt() # Get latest hunt
    crawler.download()

main()