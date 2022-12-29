# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from os import stat
from Pyro4 import expose
from array import *


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        number = self.read_input()[0]
        step = int(number) / len(self.workers)
        mapped = []

        for i in range(0, len(self.workers) - 1):
            mapped.append(self.workers[i].mymap(i * step, (i + 1) * step, int(number)))
        mapped.append(self.workers[len(self.workers) - 1].mymap((len(self.workers) - 1) * step, int(number) + 1, int(number)))

        reduced = self.myreduce(mapped)
        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(a, b, number):
        res = []
        for k in range(a, b):
            if k != 0:
                if number % k == 0:
                    isPrime = True
                    for i in range(2, (k // 2) + 1):
                        if k % i == 0:
                            isPrime = False
                            break
                    if isPrime:
                        res.append(k)
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        res = []
        for part in mapped:
            for s in part.value:
                res.append(s)
        return res

    def read_input(self):
        f = open(self.input_file_name, 'r')
        return [line.strip() for line in f.readlines()]

    def write_output(self, output):
        f = open(self.output_file_name, 'w')

        for s in output:
            f.write(str(s) + '\n')

        f.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
