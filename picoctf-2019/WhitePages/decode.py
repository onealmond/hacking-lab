from chepy import Chepy

def decode():
    
    ch = Chepy('WhitePages/whitepages.txt')\
            .load_file()\
            .find_replace('\u2003','0')\
            .find_replace(' ','1')\
            .from_binary()
    return str(ch)


if __name__ == '__main__':
    print(decode())

