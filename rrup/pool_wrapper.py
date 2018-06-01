
from multiprocessing import Pool


class PoolWrapper:
    def __init__(self, number_of_process=1, debug_mode=False):
        self.np = number_of_process
        self.debug_mode = debug_mode
        self.pool = Pool(self.np)

    def map(self, function, iterable_list):
        result = []
        if self.debug_mode:
            print "Ignoring number of processes here, executing for loop"
            for item in iterable_list:
                result.append(function(item))
        else:
            result = self.pool.map(function, iterable_list)

        return result






