""" a circular queue implementation for use in the clock algorithm
"""
import pageTable as pt

class CircularQueue():

    def __init__(self, queue_size):
        """
        Must be a Queue of Frames
        :param queue_size:
        :return:
        """
        self.qsize = queue_size
        self.pointer = 0
        self.list = []
        for i in range (0, queue_size):
            self.list.append(pt.Frame())
            self.list[i].PPN = i

    def update_successful(self, vpn, read_or_write):
        """
        :param frame: A frame to add to the Queue
        :return: False if a frame was NOT added, because the queue is full (will be page fault), True otherwise
        """
        # set sentinel value
        added = False

        # iterate through the list and try to add
        for elem in self.list:
            if elem.VPN == vpn:
                if read_or_write == 'W':
                    elem.dirty = True

                    # if we're not writing, then we're reading, and so we need to set the reference bit
                else:
                    elem.referencebit = True
                return True

        return False


    def add_successful(self, vpn, read_or_write):
        for elem in self.list:
            if elem.in_use == False:
                added = True
                elem.in_use = True
                elem.VPN = vpn
                elem.referencebit = True
                # if we're doing a write, need to set dirty bit
                if read_or_write == 'W':
                    elem.dirty = True

                return True
        return False


    def remove(self, ppn):
        removal_page = self.list[ppn]
        removal_page.in_use = False
        removal_page.referenced = False
        removal_page.dirty = False
        removal_page.vpn = None


    def find_victim(self):
        for index in range(0,self.qsize):
            elem = self.list[self.pointer]
            # if we find a page which is unreferenced (recently) and clean, that's our victim
            if elem.referencebit == False and elem.dirty == False:   # (0, 0)
                # return it's PPN, so we can index into it and remove it
                return elem.PPN
            elif elem.referencebit == False and elem.dirty == True:   # (0, 1)
                #skip, do nothing
                continue
            elif elem.referencebit == True and elem.dirty == False:    # (1, 0)
                elem.referencebit = False
                elem.dirty = False
            elif elem.referencebit == True and elem.dirty == True:     # (1, 1)
                elem.referencebit = False

            # use modulus of queue size to achieve a circular queue
            self.pointer = (self.pointer + 1) % self.qsize
            assert self.pointer <= self.qsize

        # if we get this far, no victim page was found,
        # need to flush __dirty unreferenced pages__ to disk
        # and then repeat

        return None

    def flush_dirty_and_unreferenced_pages(self):
        # NOTE: need to account for a DISK WRITE in clock algorithm

        # remove the dirty and unreferenced pages, count how many we removed
        number_of_disk_writes = 0
        for elem in self.list:
            if elem.dirty == True and elem.referencebit == False:
                elem.dirty = False
                number_of_disk_writes += 1

        return number_of_disk_writes