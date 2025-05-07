class Color():
    def __init__(self)->None:
        self.list=[
            self.white,
            self.red,
            self.green,
            self.yellow,
            self.blue,
            self.purple,
            self.libiue,
            self.gray,
            self.reset
        ]
    def show_list(self):
        return self.show_list
    white = '\033[0;37;40m'
    red   = '\033[1;31;40m'
    green = '\033[1;32;40m'
    yellow= '\033[1;33;40m'
    blue  = '\033[1;34;40m'
    purple= '\033[1;35;40m'
    libiue= '\033[1;36;40m'
    gray  = '\033[1;31;90m'
    reset = '\033[0m'
    clear = '\033[2J'

if __name__ == '__main__':
    show = Color()
    for i in show.list:
        print(i+"|||||||||||||||||")