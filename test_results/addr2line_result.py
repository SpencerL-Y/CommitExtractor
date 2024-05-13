import os
import sys


if __name__ == "__main__":
    for file in os.listdir("./"):
        os.system("cat " + file + " | addr2line -f -e ../../kcovtest_env/linux/vmlinux > " + file.split(".")[0] + "_coverage.txt")
