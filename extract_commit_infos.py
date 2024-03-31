from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import requests

bro = webdriver.Chrome()
initial_url = "https://github.com/torvalds/linux/commits/master/?author=torvalds"
brief_xpath = "//div[@data-testid=\"listview-item-title-container\"]//h4//span//a"
nxt_button_xpath = "//a[@data-testid=\"pagination-next-button\"]"
changed_file_name_xpath = "//*[@class=\"Link--primary Truncate-text\"]"
commit_id = 0
def bro_get_page(curr_depth, url=initial_url):
    if curr_depth > 10:
        return
    print("########## PAGE " + str(curr_depth) + " CONTENT ############")
    bro.get(url)
    brief_list = bro.find_elements(By.XPATH, brief_xpath)
    for item in brief_list:
        print("------------------- commit id " + str(commit_id))
        print(item.get_attribute("title"))
        content_bro = webdriver.Chrome()
        content_href = item.get_attribute("href")
        content_bro.get(content_href)
        changed_files_titles = content_bro.find_elements(By.XPATH, changed_file_name_xpath)
        print("------------------- changed files:")
        for changed_title in changed_files_titles:
            print(changed_title.text)
    nxt_btn = bro.find_element(By.XPATH, nxt_button_xpath)
    nxt_btn_href = nxt_btn.get_attribute("href")
    bro_get_page(curr_depth + 1, nxt_btn_href)



if __name__ == "__main__":
    init_depth = 0
    bro_get_page(init_depth)
    