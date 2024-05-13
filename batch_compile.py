import sys
import os


def refine_and_compile_c_code():
    os.system("cd ./test_bins && rm commt_*")
    csrcs = os.listdir("./test_files")    
    for cf in csrcs:
        if cf.find("_no") == -1:
            os.system("cd ./test_files && gcc " + cf + " -o ../test_bins/" + cf.split(".")[0])

if __name__ == "__main__":
    refine_and_compile_c_code()