# -*- coding: utf-8 -*-
import Threader as THd
import Clicker

def main():
    if __name__ == "__main__":
        with THd.Threader() as thd:
            Process = Clicker.ClickerProcess()
            thd.Trigger(Process)



main()