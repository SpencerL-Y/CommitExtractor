from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree
import os, sys
import requests

bro = webdriver.Chrome()
initial_url = "https://github.com/torvalds/linux/commits/master/?author=torvalds"
brief_xpath = "//div[@data-testid=\"listview-item-title-container\"]//h4//span//a"
nxt_button_xpath = "//a[@data-testid=\"pagination-next-button\"]"
changed_file_name_xpath = "//copilot-diff-entry"
commit_id = 0

commit_records = []
diff_file_list = []
def bro_get_page(curr_depth, url=initial_url):
    global commit_id
    global diff_file_list
    if curr_depth > 0:
        return
    print("########## PAGE " + str(curr_depth) + " CONTENT ############")
    bro.get(url)
    brief_list = bro.find_elements(By.XPATH, brief_xpath)
    for item in brief_list:
        commit_id = commit_id + 1
        temp_str = ""
        print("------------------- commit id " + str(commit_id))
        print(item.get_attribute("title"))
        temp_str += "------------------- commit id " + str(commit_id) + "\n"
        temp_str += item.get_attribute("title") + "\n"
        content_bro = webdriver.Chrome()
        content_href = item.get_attribute("href")
        content_bro.get(content_href)
        changed_files_blocks = content_bro.find_elements(By.XPATH, changed_file_name_xpath)
        print("------------------- changed files:")
        temp_str += "------------------- changed files:\n"
        for changed_title in changed_files_blocks:
            data_file_path = changed_title.get_attribute("data-file-path")
            print(data_file_path)
            temp_str += data_file_path + "\n"
            diff_file_list.append(temp_str)
        commit_records.append(temp_str)
    nxt_btn = bro.find_element(By.XPATH, nxt_button_xpath)
    nxt_btn_href = nxt_btn.get_attribute("href")
    bro_get_page(curr_depth + 1, nxt_btn_href)
    
def extract_commit_info_from_local_git():
    os.system("cd ./commit_files && rm commit_*")
    os.system("cd linux && git log -n 10 > ../gitlogs.txt")
    gitlogs_f = open("./gitlogs.txt", "r+")
    curr_commit_info = ""
    commit_num = ""
    for line in gitlogs_f.readlines():
        if line.startswith("commit"):
            if curr_commit_info == "" or commit_num == "":
                pass
            else:
                os.mknod("./commit_files/commit_" + commit_num + ".txt")
                write_f = open("./commit_files/" + "commit_" + commit_num + ".txt", "w+")
                write_f.write(curr_commit_info)
                write_f.write("diff files:\n")
                os.system("cd linux && git log -p -1 " + commit_num + " >> " + "../commit_files/commit_" + commit_num + ".txt")
                write_f.close()
            curr_commit_info = ""
            commit_num = line.split("commit")[1].strip()
        curr_commit_info += line
    gitlogs_f.close()
if __name__ == "__main__":
    init_depth = 0
    # bro_get_page(init_depth)
    # print(diff_file_list)
    extract_commit_info_from_local_git()
    