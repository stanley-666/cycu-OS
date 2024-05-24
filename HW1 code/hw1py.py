import multiprocessing
from multiprocessing import Pool
import threading
import os
import time
import datetime
import pytz
from tqdm import tqdm

tz = pytz.timezone('Asia/Taipei')

class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None,args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        # threadLock1 = threading.Lock()
        if self._target is not None:
            # threadLock1.acquire()
            #print(threading.current_thread())
            self._return = self._target(*self._args,**self._kwargs)
            time.sleep(0.1)
            # threadLock1.release()
        else :
            print('None')


    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return
    def _return(self):
        return self._return

class Sorting :
    def __init__(self):
        self.K = -1
        self.mergebuffer = []

    def bubbleSort(self,arr) :
        #print('-----------------------------'+__name__+'------------------------------')
        #print( 'bubble sort current process pid : ' + str(os.getpid()))
        n = len(arr)
        # Traverse through all array elements
        for i in range(n - 1):
            # range(n) also work but outer loop will
            # repeat one time more than needed.
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

        return arr

    def Merge(self,arr1, arr2) :
        # using naive method
        # to combine two sorted lists
        #print( 'Merge current process pid : ' + str(os.getpid()))
        size_1 = len(arr1)
        size_2 = len(arr2)
        res = []
        i, j = 0, 0
        while i < size_1 and j < size_2:
            if arr1[i] < arr2[j]:
                res.append(arr1[i])
                i += 1

            else:
                res.append(arr2[j])
                j += 1
        res = res + arr1[i:] + arr2[j:]

        return res

    def MergeSort(self,arr):
        print('MergeSort current process pid : ' + str(os.getpid()))
        array_length = len(arr)
        if array_length <= 1:
            return arr

        middle_index = array_length // 2
        left = arr[0:middle_index]
        right = arr[middle_index:]
        left = self.MergeSort(left)
        right = self.MergeSort(right)
        return self.Merge(left, right)

    def problem1(self,arr) :
        print('Calculating using cpu resources')
        start = time.time()
        n = len(arr)
        progress = tqdm(total=n)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
            progress.update(1)
        progress.update(1)
        end = time.time()
        execution_time = end-start
        print('execution_time : '+str(execution_time)+'(s)')
        ############## output file ################
        buffer = arr
        return buffer, execution_time
        # size = len(buffer)
        # if size > 10000 :
        #     name = str(size // 10000) + 'w_output1.txt'
        # else:
        #     name = str(size) + '_output1.txt'
        # with open('output/' + name, 'w') as f:
        #     f.write('total sorting val : ' + str(size) + '\n')
        #     f.write('execution_time : '+str(execution_time)+'(s)\n')
        #     f.write('datetime : ' + str(datetime.datetime.now(tz)) +'\n')
        #     for num in buffer:
        #         f.write(str(num) + '\n')
        #
        #     f.close()

    def problem2(self,arr) :
        k = int(input("請輸入要切成幾份:\n"))
        divided_arr = [] # 切成幾份
        length = len(arr)
        size = length // k # 每份幾個
        remain = length % k # 多出來的

        for i in range (k) : # 新增資料
            divided_arr.append(arr[size*i:size*i+size])

        for i in range(length-remain,length) : #把剩餘的資料均分
            divided_arr[i%k].append(arr[i])

        print('Calculating using cpu resources')
        start = time.time()
        progress = tqdm(total=2*k-1)
        for i in range(0, k):
            divided_arr[i] = self.bubbleSort(divided_arr[i])
            progress.update(1)

        self.mergebuffer = divided_arr[0]
        for i in range(1,k) :
            self.mergebuffer = self.Merge( self.mergebuffer, divided_arr[i] )
            progress.update(1)
        end = time.time()
        execution_time = end - start
        print('execution_time : '+str(execution_time)+'(s)')

        ############## output file ################
        buffer = self.mergebuffer
        return buffer,execution_time
        # size = len(buffer)
        # if size > 10000 :
        #     name = str(size // 10000) + 'w_output2.txt'
        # else:
        #     name = str(size) + '_output2.txt'
        # with open('output/' + name, 'w') as f:
        #     f.write('total sorting val : ' + str(size) + '\n')
        #     f.write('execution_time : ' + str(execution_time) + '(s)\n')
        #     f.write('datetime : ' + str(datetime.datetime.now(tz)) + '\n')
        #     for num in buffer:
        #         f.write(str(num) + '\n')
        #
        #     f.close()

    def problem3(self,arr) :
        k = int(input("請輸入要切成幾份:\n"))
        divided_arr = []  # 切成幾份
        length = len(arr)
        size = length // k  # 每份幾個
        remain = length % k  # 多出來的
        for i in range(k):  # 新增資料
            divided_arr.append(arr[size * i:size * i + size])
            # print( '第i份 : '+ str(i+1))
            # print(size * i,size * i + size)

        for i in range(length - remain, length):  # 把剩餘的資料均分
            divided_arr[i % k].append(arr[i])

        success = False
        if __name__ == '__main__':
            print('Calculating using cpu resources')

            start = time.time()
            cpus = multiprocessing.cpu_count()
            pool = Pool(16)
            bubbleresults = pool.map_async(self.bubbleSort, divided_arr) #map 一次能多個iterable
            print('將不會阻塞並和 pool.map_async 並行觸發')
            # close 和 join 是確保主程序結束後，子程序仍然繼續進行
            pool.close()
            pool.join()
            sortedarr = bubbleresults.get()
            buffer = []
            if k >= 1 :
                pool = Pool(16)
                buffer = sortedarr[0]
                for i in range(1, k):
                    buffer = pool.starmap_async(self.Merge, zip([buffer], [sortedarr[i]])) # starmap 一次只能一個iterable
                    buffer = buffer.get()[0]
                pool.close()
                pool.join()
                end = time.time()
                execution_time = end - start
                print('execution_time : '+str(execution_time)+'(s)')
                success = True
        if success == True :
            return buffer,execution_time
            # size = len(buffer)
            # if size > 10000:
            #     name = str(size//10000) + 'w_output3.txt'
            # else :
            #     name = str(size) + '_output3.txt'
            #
            # # with open('output/' + name,'w') as f :
            # #     f.write( 'total sorting val : ' + str(size)+'\n')
            # #     f.write('CPU Time : ' + str(execution_time) + '(s)\n')
            # #     f.write('datetime : ' + str(datetime.datetime.now(tz)) + '\n')
            # #     for num in buffer :
            # #         f.write(str(num)+'\n')
            # #
            # #     f.close()
        else :
            return None

    def problem4(self,arr) :
        k = int(input("請輸入要切成幾份:\n"))
        divided_arr = []  # 切成幾份
        length = len(arr)
        size = length // k  # 每份幾個
        remain = length % k  # 多出來的
        for i in range(k):  # 新增資料
            divided_arr.append(arr[size * i:size * i + size])

        for i in range(length - remain, length):  # 把剩餘的資料均分
            divided_arr[i % k].append(arr[i])
        if __name__ == "__main__":
            # 建立 k 個子執行緒
            print('Calculating using cpu resources')
            algorithm = Sorting()
            threads = []
            start = time.time()
            for i in range(k):
                t = ThreadWithReturnValue(target=algorithm.bubbleSort, args=[divided_arr[i]])
                threads.append(t)
                threads[i].start()
            # 主執行緒繼續執行自己的工作
            # 等待所有子執行緒結束

            ret = [] # store sorted array
            for i in range(k):
                ret.append(threads[i].join())

            threads = []
            if k > 1 :
                sortedarr = []
                for i in range(k):
                    t = ThreadWithReturnValue(target=algorithm.Merge, args=(sortedarr,ret[i]),)
                    threads.append(t)
                    threads[i].start()
                    sortedarr = threads[i].join()

                # 主執行緒繼續執行自己的工作
                # 等待所有子執行緒結束

            elif k == 1 :
                sortedarr = ret[0]

            end = time.time()
            execution_time = end - start
            buffer = sortedarr
            print('execution_time : '+str(execution_time)+'(s)')
            return buffer,execution_time
            # size = len(buffer)
            # if size > 10000:
            #     name = str(size // 10000) + 'w_output4.txt'
            # else :
            #     name = str(size) + '_output4.txt'
            # with open('output/' + name, 'w') as f:
            #     f.write('total sorting val : ' + str(size) + '\n')
            #     f.write('execution_time : ' + str(execution_time) + '(s)\n')
            #     f.write('datetime : ' + str(datetime.datetime.now(tz)) + '\n')
            #     for num in buffer:
            #         f.write(str(num) + '\n')

class IO :
    def __init__(self):
        self.vec_nums = []
        self.fileName = str()
    def readfile(self) :
        try :
            fileName = input("請輸入檔案名稱:\n")
            if fileName == '0' :
                return False
            if os.path.exists('input/' + fileName) == False :
                print(fileName +" does not exist! \n")
                return False
            else :
                with open('input/' + fileName,'r') as file :
                    for line in file :
                        for x in line.split() :
                            if x != '\n' :
                                self.vec_nums.append(int(x))
                    # for val in self.vec_nums :
                    #     print(val)
                    file.close()
                    self.fileName = fileName
                    return True
        except :
            return False

    def outputfile(self,sortedArray,execution_time,methodid):
        outputfilename = self.fileName[:-4] + '_output' + methodid + '.txt'
        with open('output/'+outputfilename, 'w') as f:
            f.write('Sort : \n')
            for num in sortedArray:
                f.write(str(num) + '\n')
            f.write('CPU Time : ' + str(execution_time) + '(s)\n')
            f.write('Output Time : ' + str(datetime.datetime.now(tz)) + '\n')

    def clear(self) :
        self.vec_nums = []

    def size(self) :
        return len(self.vec_nums)

    def getarr(self) :
        return self.vec_nums

    def printarr(self,arr) :
        for i in range(len(arr)) :
            print( "[" + str(i+1) + "] " + str(arr[i]))

def main() :
    io = IO()
    cases = Sorting()
    command = -1
    while command != 0 :
        io.__init__()
        cases.__init__()
        while io.readfile() == False:
            print("[WARNING] : Failed to load the file (CHECK THE PATH (input/... .txt) FILE EXISTENCE)" )

        arr = io.getarr()
        try :
            command = int(input("請輸入方法編號:(方法1, 方法2, 方法3, 方法4)(0代表結束)\n"))
            if command == 1:
                sortedArray,execution_time = cases.problem1(arr)
                io.outputfile(sortedArray,execution_time,'1')

            elif command == 2:
                sortedArray,execution_time = cases.problem2(arr)
                io.outputfile(sortedArray, execution_time, '2')
            elif command == 3:
                sortedArray,execution_time = cases.problem3(arr)
                io.outputfile(sortedArray, execution_time, '3')
            elif command == 4:
                sortedArray,execution_time = cases.problem4(arr)
                io.outputfile(sortedArray, execution_time, '4')

            elif command == 0 :
                print('Program finished')
            else :
                print('輸入方法編號 1,2,3,4 (0代表結束)')
        except :
            print('方法輸入錯誤')

if __name__ == '__main__':
    main()







