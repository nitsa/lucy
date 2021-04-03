import sys

if __name__ == "__main__":

    file = open(sys.argv[1], 'r')
    lines = file.readlines()
    file.close()

    for line  in lines:
        file2 = open(sys.argv[2], 'r')
        lines2 = file2.readlines()
        file2.close()

        for line2 in lines2:
            print(line.strip('\n').strip('\r').strip() + line2.strip('\n').strip('\r').strip())
