import openai
import os, re
import sys

global_model = "gpt-4-0125-preview"
# chat interface 
class chat_interface:
    def __init__(self) -> None:
        self.msg_list = []

    def show_conversations(self):
        print("------------------------------------- conversations")
        for msg in self.msg_list:
            if msg['role'] == 'user':
                print("USER ================== BEGIN")
                print(msg['content'])
                print("USER ================== END")
            else:
                print("CHATGPT ================== BEGIN")
                print(msg['content'])
                print("CHATGPT ================== END")
        print("------------------------------------- conversations end")
    

    def set_up_aiproxy_configs(self):
        openai.api_key = "sk-5nga6ZRm5D87QSytGYlw9jIhItjhnPqxeUoUfRuAJAam87zt"
        openai.api_base = "https://api.aiproxy.io/v1"

    # reserved for latter if key for openai can be obtained, currently we are using the aiproxy
    # aiproxy is not free
    def set_up_default_configs(self):
        openai.api_key = "sk-5nga6ZRm5D87QSytGYlw9jIhItjhnPqxeUoUfRuAJAam87zt"
        openai.api_base = "https://api.aiproxy.io/v1"


    def ask_question_and_record(self, content):
        self.msg_list.append({"role": "user", "content": content})
        res = openai.ChatCompletion.create(
            model=global_model,
            messages=[{"role": "user", "content": content}]
        )
        answer = res.choices[0].message
        self.msg_list.append(answer)
        return answer
    
    def set_role_and_ask(self, content):
        role_message = "You will help me with the commit change of Linux kernel analyzing. \n"
        role_message += "Each time you will first be given a text containing the commit change description in Github, then the file changed will also be deliverred to you.\n"
        role_message += "You should first analyze the possible functions that have been changed by the commit, then analyze the syscalls that have been changed by these functions\n"
        role_message += "If the commit is not about core functionality or the commit cannot influence basic behavior of kernel syscalls, the field IS_CORE_FUNC will be NO\n"
        role_message += "The final outcome of your answer should follow the format below:\n"
        role_message += "CHATBEGIN\n"
        role_message += "IS_CORE_FUNC: YES/NO\n (\"YES\" when the commit is about core functionality that can be tested through syscalls)"
        role_message += "ANALYSIS: [a sentence of analysis description here]"
        role_message += "SYSCALL PROGRAM IN C:\n"
        role_message += "[C Program]\n"
        role_message += "CHATEND\n"
        role_message += "In the above format, [C Program] should be in the following format:\n"
        role_message += "INCLUDES: \n#include <xxx.h>\n #include <xxx.h>"
        role_message += "PROGRAM: \n[program segment in main without main declaration and without other function declaration]\n"
        role_message += '\n'
        role_message += "Do not use ``` to surround the code, the above code should be generated completely with you only modify the program by\
                         inserting the include files and syscall programs at CHATGPT INSERT ...\n"
        message_list = []
        message_list.append({"role": "user", "content": role_message})
        message_list.append({"role": "user", "content": content})
        res = openai.ChatCompletion.create(
            model=global_model,
            messages=message_list
        )
        answer = res.choices[0].message
        # print(answer)
        return answer
    
def obtain_llm_info(commit_change):
    interface = chat_interface()
    interface.set_up_aiproxy_configs()
    answer = interface.set_role_and_ask(commit_change)
    return answer.content
  
if __name__ == '__main__':
    commit_info = ""
    commit_file = open("./commit_files/commit_18685451fc4e546fc0e718580d32df3c0e5c8272.txt", "r+")
    for line in commit_file.readlines():
        commit_info += line
    interface = chat_interface()
    interface.set_up_aiproxy_configs()
    answer = interface.set_role_and_ask(commit_info)
    print(answer.content)