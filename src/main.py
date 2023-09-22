# the goal of this script is to scrape the data from the website and store it in a file

import requests
from bs4 import BeautifulSoup
import os

if __name__ == "__main__":
    base_url = "https://www.merriam-webster.com/browse/dictionary/"
    letters = "abcdefghijklmnopqrstuvwxyz"
    page_urls = [base_url + letter for letter in letters]
    # page_urls.append(base_url + "0")
    page_urls.append(base_url + "bio")
    page_urls.append(base_url + "geo")

    word_list = []
    for page_url in page_urls:
        first_page_url = page_url + "/1"
        first_page = requests.get(first_page_url)
        first_page_soup = BeautifulSoup(first_page.content, "html.parser")
        
        # find the span tag with class "counters" and get its contents
        first_page_soup_counters = first_page_soup.find("span", class_="counters")
        first_page_soup_counters_contents = first_page_soup_counters.contents

        # the contents of the span tag is of the form "page 1 of 4". We need to get the 4
        num_pages = int(first_page_soup_counters_contents[0].split()[-1])
        
        for page_num in range(1, num_pages + 1):
            url = page_url + "/" + str(page_num)
            print(url
                  )
            page = requests.get(url)
            
            # create the "output" folder if it doesn't exist
            if not os.path.exists("output"):
                os.makedirs("output")

            # write the html to a file for debugging purposes
            # with open("output/" + page_url.split("/")[-1] + "_" + str(page_num) + ".html", "w") as f:
            #     f.write(page.text)
            soup = BeautifulSoup(page.content, "html.parser")
            
            # find the div tag with class "mw-grid-table-list"
            div_tag = soup.find("div", class_="mw-grid-table-list")

            # find all the span tags within the div tag
            span_tags = div_tag.find_all("span")

            # get the text from each span tag and append it to the word_list
            for span_tag in span_tags:
                word_list.append(span_tag.text)

    # write the word_list to "output/word_list.txt". Create the file and folder if it doesn't exist
    with open("output/word_list.txt", "w") as f:
        for word in word_list:
            f.write(word + "\n")
