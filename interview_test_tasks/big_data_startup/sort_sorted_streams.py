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
            return None
                    
def merge_streams(streams):
    """Merges sorted streams into one sorted list.
    :param streams: list of MyStream objects.
    :return: sorted list of integers.
    """

    priority_buffer = PriorityQueue()
    all_streams_are_empty = False
    empty_stream = False
    iterations = 0
    while not all_streams_are_empty:
         all_streams_are_empty = True
         for stream in streams:
            new_int = stream.pop()
            empty_stream = new_int is None
            while not empty_stream:
                priority_buffer.insert(new_int)
                if iterations < 1: # first step is to get the top
                                   # "layer" of all streams
                    break
                else: # if we already have our top "layer" 
                      # we will run the main sorting algorithm
                    min_int = priority_buffer.pop_min()
                    yield min_int # return minimums one by one
                    iterations += 1
                    if new_int == min_int:
                        new_int = stream.pop()
                    else:
                        break # go to the next stream
            all_streams_are_empty = all_streams_are_empty and empty_stream

    if iterations:
        print ('DEBUG: heap (list) of real size == %s were allocated '
               'during sorting.' % len(priority_buffer.heap))

    while len(priority_buffer): # when all streams became empty
                                # we just ineratively pop all heap content
        yield priority_buffer.pop_min()

