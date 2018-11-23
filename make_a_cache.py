# Homework for SDE study club: write a get_value() method that takes advantage of the pre-build caches
# to get the lowest possible score.

import numpy as np

score = 0
small_hits = 0
big_hits = 0
small_writes = 0
big_writes = 0
disk_reads = 0

SMALL_CACHE_MEM_SIZE = 500
SMALL_CACHE_WRITE_COST = 1
SMALL_CACHE_READ_COST = 1

LARGE_CACHE_MEM_SIZE = 5000
LARGE_CACHE_WRITE_COST = 10
LARGE_CACHE_READ_COST = 10

DISK_MEM_SIZE = 1000000
DISK_MEM_WRITE_COST = 1000
DISK_MEM_READ_COST = 1000

TEST_SIZE = 1000000
standard_dev = 100
NUMBER_TIMES_TO_SHIFT_INPUT = 3


class SmallCache:
    def __init__(self):
        self.memory = np.zeros(SMALL_CACHE_MEM_SIZE)

    def read(self, index):
        global score
        global small_hits

        small_hits += 1
        score += SMALL_CACHE_READ_COST
        return self.memory[index]

    def write(self, index, value):
        global score
        global small_writes
        small_writes += 1

        score += SMALL_CACHE_WRITE_COST
        self.memory[index] = value


class LargeCache:
    def __init__(self):
        self.memory = np.zeros(LARGE_CACHE_MEM_SIZE)

    def read(self, index):
        global score
        global big_hits
        big_hits += 1
        score += LARGE_CACHE_READ_COST

        return self.memory[index]

    def write(self, index, value):
        global score
        global big_writes
        big_writes += 1
        score += LARGE_CACHE_WRITE_COST
        self.memory[index] = value


class DiskMemory:
    def __init__(self):
        self.memory = np.random.rand(DISK_MEM_SIZE)

    def read(self, index):
        global score
        global disk_reads
        disk_reads += 1
        score += DISK_MEM_READ_COST
        return self.memory[index]

    def write(self, index, value):
        global score
        score += DISK_MEM_WRITE_COST
        self.memory[index] = value

    def check(self, index):
        # THIS METHOD IS FOR CHECKING ONLY - YOU CANNOT USE IT FOR YOUR READS
        return self.memory[index]


disk = DiskMemory()
small_cache = SmallCache()
large_cache = LargeCache()


def generate_normal_dist_random_number(centerpoint):
    # Generates a pseudo-random number according to a normal distribution centered around centerpoint
    return int(np.random.normal(centerpoint, standard_dev))

def get_value(to_read):
    # PUT YOUR CODE HERE
    # Right now this reads from disk each time, which is the most expensive read operation by a lot.
    # You should cache these disk reads in your large and small caches
    # print("Small = {}".format(small_cache.memory))

    # # --------------- SOLUTION NUMBER 1 --------------- #
    #
    # if to_read in small_cache.memory:
    #     # print("Small hit")
    #     return small_cache.read(np.argmax(small_cache.memory == to_read) + 1)
    #
    # elif 0 in small_cache.memory:
    #     disk_mem = disk.read(to_read)
    #     small_cache.write(np.argmax(small_cache.memory == 0), to_read)
    #     small_cache.write(np.argmax(small_cache.memory == 0), disk_mem)
    #     return disk_mem
    #
    # elif to_read in large_cache.memory:
    #     # print("Large hit")
    #     return large_cache.read(np.argmax(large_cache.memory == to_read) + 1)
    #
    # elif 0 in large_cache.memory:
    #
    #     disk_mem = disk.read(to_read)
    #     large_cache.write(np.argmax(large_cache.memory == 0), to_read)
    #     large_cache.write(np.argmax(large_cache.memory == 0), disk_mem)
    #     return disk_mem
    #
    # else:
    #     return disk.read(to_read)
    #
    # # ------------- END SOLUTION NUMBER 1 ------------- #

    # # --------------- SOLUTION NUMBER 2 --------------- #
    #
    # if to_read in large_cache.memory and np.argmax(large_cache.memory == to_read) < SMALL_CACHE_MEM_SIZE:
    #     # print("Small hit")
    #     return small_cache.read(np.argmax(large_cache.memory == to_read))
    #
    # elif 0 in small_cache.memory:
    #     disk_mem = disk.read(to_read)
    #     large_cache.write(np.argmax(large_cache.memory == 0), to_read)
    #     small_cache.write(np.argmax(small_cache.memory == 0), disk_mem)
    #     return disk_mem
    #
    # elif to_read in large_cache.memory and np.argmax(large_cache.memory == to_read) >= SMALL_CACHE_MEM_SIZE:
    #     # print("Large hit")
    #     return large_cache.read(np.argmax(large_cache.memory == to_read) + 1)
    #
    # elif 0 in large_cache.memory:
    #
    #     disk_mem = disk.read(to_read)
    #     large_cache.write(np.argmax(large_cache.memory == 0), to_read)
    #     large_cache.write(np.argmax(large_cache.memory == 0), disk_mem)
    #     return disk_mem
    #
    # else:
    #     return disk.read(to_read)
    #
    # # ------------- END SOLUTION NUMBER 2 ------------- #

    # --------------- SOLUTION NUMBER 3 --------------- #
    min_val = np.min(large_cache.memory[0:500])
    max_val = np.max(large_cache.memory[0:500])

    # print("Min:{}\tMax: {}\tTo Read: {}".format(min_val, max_val, to_read))

    if min_val != 0 and max_val != 0 and (to_read < (min_val - standard_dev * 5) or
                                          to_read > (max_val + standard_dev * 5)):

        small_cache.memory = np.zeros(SMALL_CACHE_MEM_SIZE)
        large_cache.memory = np.zeros(LARGE_CACHE_MEM_SIZE)

    if to_read in large_cache.memory and np.argmax(large_cache.memory == to_read) < SMALL_CACHE_MEM_SIZE:
        # print("Small hit")
        return small_cache.read(np.argmax(large_cache.memory == to_read))

    elif 0 in small_cache.memory:
        disk_mem = disk.read(to_read)
        large_cache.write(np.argmax(large_cache.memory == 0), to_read)
        small_cache.write(np.argmax(small_cache.memory == 0), disk_mem)
        return disk_mem

    elif to_read in large_cache.memory and np.argmax(large_cache.memory == to_read) >= SMALL_CACHE_MEM_SIZE:
        # print("Large hit")
        return large_cache.read(np.argmax(large_cache.memory == to_read) + 1)

    elif 0 in large_cache.memory:

        disk_mem = disk.read(to_read)
        large_cache.write(np.argmax(large_cache.memory == 0), to_read)
        large_cache.write(np.argmax(large_cache.memory == 0), disk_mem)
        return disk_mem

    else:
        return disk.read(to_read)

    # ------------- END SOLUTION NUMBER 3 ------------- #

def get_centerpoint():
    return np.random.randint(standard_dev, DISK_MEM_SIZE-standard_dev)


def run_test():
    global small_hits
    large_hits = 0
    for i in range(0, TEST_SIZE):

        if i % int(TEST_SIZE/NUMBER_TIMES_TO_SHIFT_INPUT) == 0:
            centerpoint = get_centerpoint()
            # reset the center of our normal distribution, so that the caches will need to adapt

        to_read = generate_normal_dist_random_number(centerpoint)
        candidate_value = get_value(to_read)
        # print("To Read = {} \nCandidate Value = {}".format(to_read, candidate_value))

        # print("Candidate = {}".format(candidate_value))
        # print("Disk Stuff = {}".format(DiskMemory.check(disk, to_read)))

        if candidate_value != DiskMemory.check(disk, to_read):
            raise ValueError('Error reading from disk')

    print("Score: {}".format(score))
    #print("Small Reads = {}\tBig Reads = {}\tDisk Reads = {}".format(small_hits, big_hits, disk_reads))
    #print("Small Writes = {}\tBig Writes = {}".format(small_writes, big_writes))


run_test()
