# -*- coding: utf-8 -*-
import Threader as THd
import Clicker
from os import getcwd

def main():
    if __name__ == "__main__":
        print(getcwd())
        with THd.Threader() as thd:
            Process = Clicker.ClickerProcess()
            thd.Trigger(Process)



main()