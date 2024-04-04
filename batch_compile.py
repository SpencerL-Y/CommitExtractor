import sys
import os


def refine_and_compile_c_code():
    csrcs = os.listdir("./test_files")    
    for cf in csrcs:
        os.system("cd ./test_files && gcc " + cf + " -o ../test_bins/" + cf.split(".")[0])

if __name__ == "__main__":
    refine_and_compile_c_code()