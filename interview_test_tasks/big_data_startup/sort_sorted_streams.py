#! /usr/bin/python


########################\  (Check out my heavy ASCII art skills! *ROLF*)
### K sorted streams ####\_____________________________________________
#######################################################################|
#                                                                     #|
#     Given a list of k sorted streams of integers, combine them      #|
#     into a single sorted stream.                                    #|
#                                                                     #|
#     MyStream objects represent sorted arrays of integers of         #|
#     arbitrary length and implement only a pop() method that         #|
#     either removes the first element of the stream and returns      #|
#     it, or returns None if the stream is empty.                     #|
#                                                                     #|
#######################################################################|


from priority_queue import PriorityQueue

class MyStream(object):
    def __init__(self, filename):
        self.in_file = open(filename)
        self.iterator = self.__iter__()
        self.empty = False

    def __iter__(self):
        line = ' '
        while line:
            line = self.in_file.readline()
            if line:
                yield int(line)

    def __del__(self):
        self.in_file.close()
        
    def pop(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.empty = True
            return None
                    
def merge_streams(streams):
    """Merges sorted streams into one sorted list.
    :param streams: list of MyStream objects.
    :return: sorted list of integers.
    """

    min_buffer = PriorityQueue()
    all_streams_are_empty = False
    iterations = 0
    next_i = None
    while not all_streams_are_empty:
        all_streams_are_empty = True
        for i, stream in enumerate(streams):
            while not stream.empty:
                if (next_i is not None) and i != next_i:
                    break

                new_int = stream.pop()

                if new_int is not None:
                    min_buffer.insert((i, new_int))
                if iterations < 1: # first step is to get the top
                                   # "layer" of all streams
                    break
                else: # if we already have our top "layer" 
                      # we will run the main sorting algorithm
                    next_i, min_int = min_buffer.pop_min()
                    yield min_int # return minimums one by one
                    next_i = None if streams[next_i].empty else next_i

            all_streams_are_empty = all_streams_are_empty and stream.empty
        iterations += 1

    while len(min_buffer): # when all streams became empty
                                # we just ineratively pop all heap content
        yield min_buffer.pop_min()

    print ('DEBUG: heap (list) of real size == %s were allocated '
           'during sorting.' % len(min_buffer.heap))

