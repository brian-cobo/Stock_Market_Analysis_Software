# File Imports
from Main_Program.Web_Scraper import Find_Articles
from Main_Program.Stock_Visualizations_Menu import Gather_Stock_Info_Menu as Stock


def navigate_through_article_scraper():
    choice = 0
    print('Article Scraper and Analysis')
    scraper = Find_Articles()
    while choice != -1:
        choice = int(input('\nChoose Option:\n'
                           '1: Retrieve Articles About Specific Company\n'
                           '2: Retrieve Articles From Front Page\n'
                           '-1: Quit\n'))
        if choice == -1:
            print('\nExiting Article Scraper\n')

        elif choice == 1:
            company = input("\nWhat company would you like to search articles for?\n")
            num_of_pages_to_search = int(input("\nHow many pages would you like to go through?\n"))
            scraper.find_article_from_search_URL(scraper.find_search_URL(company), num_of_pages_to_search)

        elif choice == 2:
            home_page_URL = f'https://www.ibtimes.com/business'
            num_of_pages_to_search = int(input("\nHow many pages would you like to go through?\n"))
            scraper.find_articles_from_main_business_page(home_page_URL,
                                                          num_of_pages_to_search)
        else:
            print('Choice not recognized')

def navigate_through_stock_data():
    stock = Stock()
    choice = 0
    print('Welcome')
    while choice != -1:
        choice = int(input('\nChoose Option:\n'
                           '1: Get Historical Data\n'
                           '2: Get Current Data\n'
                           '3: Create Market Report\n'
                           '4: Get Sector Data\n'
                           '5: Search for Company Symbol\n'
                           '-1: Quit\n'))
        if choice == -1:
            print("\nStock Data")

        elif choice == 1:
            stockSymbol = stock.ask_for_stock_symbol()
            stock.get_historical_data(stockSymbol)

        elif choice == 2:
            stockSymbol = stock.ask_for_stock_symbol()
            stock.get_current_data(stockSymbol, print_results=True)

        elif choice == 3:
            stock.create_market_report()

        elif choice == 4:
            stock.get_sector_data()

        elif choice == 5:
            keyword_to_search_for = input('\nWhat keyword would you like to search for? ')
            stock.search_for_company_symbol(keyword_to_search_for)

        else:
            print('Choice not recognized')


if __name__ == "__main__":
    main_choice = 0
    print('Stock Market Analysis Software')

    while main_choice != -1:
        choice = int(input('\nDo you want to retrieve stock data of article data?\n'
                           ' 1: Retrieve Stock Data\n'
                           ' 2: Retrieve Article Data\n'
                           '-1: Quit\n'))
        if choice == 1:
            navigate_through_stock_data()
        if choice == 2:
            navigate_through_article_scraper()
        if choice == -1:
            print('Goodbye')
            exit(0)
        else:
            print('Choice not Recognized')