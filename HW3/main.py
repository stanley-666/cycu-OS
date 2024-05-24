import os
import copy

def swap( num1, num2 ) :
   return num2,num1

class IO :
    def __init__(self):
        self.vec_nums = []
        self.fileName = str()
        self.command = -1
        self.num = 0

        while self.readfile() == False:
            print("[WARNING] : Failed to load the file (CHECK THE PATH (input/... .txt) FILE EXISTENCE)")
        print("Read File Successfully")

    def insertion(self,format1):
        self.vec_nums.append(format1)

    def readfile(self) :
        # try :
            fileName = input("請輸入檔案名稱:\n")
            if fileName == '0' :
                return False
            if os.path.exists('input/' + fileName) == False :
                print(fileName +" does not exist! \n")
                return False
            else :
                with open('input/' + fileName,'r') as file :

                    data = []
                    for line in file : # append every line to data list
                        if line != '\n' :
                            data.append(line)

                    size = len(data)
                    cin = [] # store command and timeslice
                    if size > 0 :
                        for val in data[0].split() :
                            cin.append(val)

                        self.command = int(cin[0])
                        self.num = int(cin[1])
                        #print(self.command,self.num)
                        for i in range(1,size) :
                            buffer = data[i]
                            for j in buffer :
                                if j.isspace() == False and j.isdigit() == True: # NOT SPACE AND IS DIGIT
                                    #print(j)
                                    self.vec_nums.append(int(j))

                    file.close()
                    self.fileName = fileName
                    return True
        # except :
        #     print('exception')
        #     return False

    def outputfile(self,outputstr):
        outputfilename = 'out_' + self.fileName[:-4] + '.txt'
        with open('output/'+outputfilename, 'w') as f:
            f.write(outputstr)
            f.close()

    def clear(self) :
        self.vec_nums = []

    def size(self) :
        return len(self.vec_nums)

    def getlist(self) :
        return self.vec_nums

    def get(self):
        return self.num

    def GETCOMMAND(self):
        return self.command

    def printarr(self,arr) :
        size = len(arr)
        print(size)
        for i in range(size) :
            print( "[" + str(i+1) + "] " + str(arr[i]))

class PR : # Page Replacement
    def __init__(self):
        self.io = IO()
        self.pageframesize = copy.deepcopy( self.io.get() )
        self.page = copy.deepcopy( self.io.getlist() )

    def FIFO(self):
        MAX_SIZE = copy.deepcopy(self.pageframesize)
        pagelist = copy.deepcopy(self.page)
        pageframe = list()
        pr = 0
        pf = 0

        PAGE_SIZE = len(self.page)
        outputstr = '--------------FIFO-----------------------\n'

        for i in range(PAGE_SIZE):
            CUR_SIZE = len(pageframe)
            PAGE_FAULT = False
            for page in pageframe:
                if page == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                    PAGE_FAULT = True
                    break

            if PAGE_FAULT == False :
                pf = pf + 1
                if (CUR_SIZE == MAX_SIZE):
                    pr = pr + 1
                    pageframe.pop(MAX_SIZE - 1)
                pageframe.insert(0, pagelist[i])
            # output string
            outputstr = outputstr + str(pagelist[i]) + '\t'
            for page in pageframe :
                outputstr = outputstr + str(page)

            if PAGE_FAULT == False :
                outputstr = outputstr + '\tF'
            outputstr = outputstr + '\n'
            #print(pagelist[i],pageframe,PAGE_FAULT)
        #print('Page Fault =', pf, 'Page Replaces =', pr, 'Page Frames =', MAX_SIZE)
        outputstr = outputstr + 'Page Fault = ' + str(pf) + '  Page Replaces = '+ str(pr) + '  Page Frames = ' + str(MAX_SIZE) + '\n\n'
        return outputstr

    def LRU(self):
        MAX_SIZE = copy.deepcopy(self.pageframesize)
        pagelist = copy.deepcopy(self.page)
        pageframe = list()
        pr = 0
        pf = 0
        PAGE_SIZE = len(self.page)
        #print('--------------LRU-----------------------')
        outputstr = '--------------LRU-----------------------\n'
        # 每個counter一開始都為0 被加入就重新計時
        for i in range(PAGE_SIZE):
            CUR_SIZE = len(pageframe)
            PAGE_FAULT = False
            #找最久的frame
            for j in range( len(pageframe)):
                if pageframe[j] == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                    pageframe.pop(j)
                    PAGE_FAULT = True
                    break

            if PAGE_FAULT == False :
                pf = pf + 1
                if CUR_SIZE == MAX_SIZE : #滿了
                    pr = pr + 1
                    pageframe.pop(MAX_SIZE-1)

            pageframe.insert(0, pagelist[i])

            outputstr = outputstr + str(pagelist[i]) + '\t'
            for page in pageframe:
                outputstr = outputstr + str(page)

            if PAGE_FAULT == False:
                outputstr = outputstr + '\tF'
            outputstr = outputstr + '\n'
            #print(pagelist[i],pageframe,PAGE_FAULT)
            #output

        #print('Page Fault =', pf, 'Page Replaces =', pr, 'Page Frames =', MAX_SIZE)
        outputstr = outputstr + 'Page Fault = ' + str(pf) + '  Page Replaces = ' + str(pr) + '  Page Frames = ' + str(MAX_SIZE) + '\n\n'
        return outputstr

    def LFU(self):
        MAX_SIZE = copy.deepcopy(self.pageframesize)
        pagelist = copy.deepcopy(self.page)
        pageframe = list()
        Counter = dict()
        pr = 0
        pf = 0
        PAGE_SIZE = len(self.page)
        #print('--------------Least Frequently Used LRU Page Replacement-----------------------')
        outputstr = '--------------Least Frequently Used LRU Page Replacement-----------------------\n'
        # 每個counter一開始都為0 被加入就重新計時
        for i in range(PAGE_SIZE):
            CUR_SIZE = len(pageframe)
            PAGE_FAULT = False
            #找最久的frame
            for j in range( len(pageframe)):
                if pageframe[j] == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                    PAGE_FAULT = True
                    break

            if PAGE_FAULT == False :
                pf = pf + 1
                if CUR_SIZE == MAX_SIZE : #滿了
                    pr = pr + 1
                    lessused = Counter[str(pageframe[MAX_SIZE-1])]
                    lessused_i = MAX_SIZE - 1
                    for j in range(MAX_SIZE-1,-1,-1) :
                        if lessused > Counter[str(pageframe[j])] :
                            lessused = Counter[str(pageframe[j])]
                            lessused_i = j
                    Counter[str(pageframe[lessused_i])] = 0
                    pageframe.pop(lessused_i)


            else :
                for j in range(len(pageframe)):
                    if pageframe[j] == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                        pageframe.pop(j)
                        break

            pageframe.insert(0, pagelist[i])

            # insert data
            if str(pagelist[i]) in Counter:
                Counter[str(pagelist[i])] = Counter[str(pagelist[i])] + 1
            else:
                Counter.update({str(pagelist[i]): 1})
            #print(pagelist[i],pageframe,PAGE_FAULT)
            outputstr = outputstr + str(pagelist[i]) + '\t'
            for page in pageframe:
                outputstr = outputstr + str(page)

            if PAGE_FAULT == False:
                outputstr = outputstr + '\tF'
            outputstr = outputstr + '\n'
            #output
        #print('Page Fault =', pf, 'Page Replaces =', pr, 'Page Frames =', MAX_SIZE)
        outputstr = outputstr + 'Page Fault = ' + str(pf) + '  Page Replaces = ' + str(pr) + '  Page Frames = ' + str(MAX_SIZE) + '\n\n'
        return outputstr

    def MFU_FIFO(self):
        #FIFO COUNTER要歸零
        MAX_SIZE = copy.deepcopy(self.pageframesize)
        pagelist = copy.deepcopy(self.page)
        pageframe = list()
        pr = 0
        pf = 0
        Counter = dict()
        PAGE_SIZE = len(self.page)
        outputstr = '--------------Most Frequently Used Page Replacement -----------------------\n'
        #print('--------------Most Frequently Used Page Replacement -----------------------')

        for i in range(PAGE_SIZE):
            CUR_SIZE = len(pageframe)
            PAGE_FAULT = False
            for page in pageframe:
                if page == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                    PAGE_FAULT = True
                    break

            if PAGE_FAULT == False :
                pf = pf + 1
                if CUR_SIZE == MAX_SIZE : #滿了
                    pr = pr + 1
                    mostused = Counter[str(pageframe[MAX_SIZE-1])]
                    mostused_i = MAX_SIZE - 1
                    for j in range(MAX_SIZE-1,-1,-1) :
                        if mostused < Counter[str(pageframe[j])] :
                            mostused = Counter[str(pageframe[j])]
                            mostused_i = j
                    Counter[str(pagelist[i])] = 0
                    pageframe.pop(mostused_i)
                    pageframe.insert(0, pagelist[i])

                elif CUR_SIZE < MAX_SIZE :
                    pageframe.insert(0, pagelist[i])

            # insert data
            if str(pagelist[i]) in Counter:
                Counter[str(pagelist[i])] = Counter[str(pagelist[i])] + 1
            else:
                Counter.update({str(pagelist[i]): 1})
            #output string
            outputstr = outputstr + str(pagelist[i]) + '\t'
            for page in pageframe:
                outputstr = outputstr + str(page)

            if PAGE_FAULT == False:
                outputstr = outputstr + '\tF'
            outputstr = outputstr + '\n'
            #print(pagelist[i],pageframe,PAGE_FAULT)
        #print('Page Fault =', pf, 'Page Replaces =', pr, 'Page Frames =', MAX_SIZE)
        outputstr = outputstr + 'Page Fault = ' + str(pf) + '  Page Replaces = ' + str(pr) + '  Page Frames = ' + str(MAX_SIZE) + '\n\n'
        return outputstr

    def MFU_LRU(self):
        # FIFO COUNTER不用歸零
        MAX_SIZE = copy.deepcopy(self.pageframesize)
        pagelist = copy.deepcopy(self.page)
        pageframe = list()
        Counter = dict()
        pr = 0
        pf = 0
        PAGE_SIZE = len(self.page)
        #print('--------------Least Frequently Used LRU Page Replacement-----------------------')
        outputstr = '--------------Most Frequently Used LRU Page Replacement-----------------------\n'
        # 每個counter一開始都為0 被加入就重新計時
        for i in range(PAGE_SIZE):
            CUR_SIZE = len(pageframe)
            PAGE_FAULT = False
            #找最久的frame
            for j in range( len(pageframe)):
                if pageframe[j] == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                    PAGE_FAULT = True
                    break

            if PAGE_FAULT == False :
                pf = pf + 1
                if CUR_SIZE == MAX_SIZE : #滿了
                    pr = pr + 1
                    mostused = Counter[str(pageframe[MAX_SIZE-1])]
                    mostused_i = MAX_SIZE - 1
                    for j in range(MAX_SIZE-1,-1,-1) :
                        if mostused < Counter[str(pageframe[j])] :
                            mostused = Counter[str(pageframe[j])]
                            mostused_i = j
                    #找最久然後pop
                    #下次重新載入 給予時間標記
                    Counter[str(pageframe[mostused_i])] = 0
                    pageframe.pop(mostused_i)
                    pageframe.insert(0, pagelist[i])

                elif CUR_SIZE < MAX_SIZE :
                    pageframe.insert(0, pagelist[i])
            else :
                for j in range(len(pageframe)):
                    if pageframe[j] == pagelist[i]:  # 如果現在的page在page frame裡 -> no page fault
                        pageframe.pop(j)
                        break
                pageframe.insert(0, pagelist[i])

            # insert data
            if str(pagelist[i]) in Counter:
                #被參考重新給予一個新的時間標記
                Counter[str(pagelist[i])] = Counter[str(pagelist[i])] + 1
            else:
                Counter.update({str(pagelist[i]): 1})
            #print(pagelist[i],pageframe,PAGE_FAULT,Counter)
            #output string
            outputstr = outputstr + str(pagelist[i]) + '\t'
            for page in pageframe:
                outputstr = outputstr + str(page)
            if PAGE_FAULT == False:
                outputstr = outputstr + '\tF'
            outputstr = outputstr + '\n'

        #print('Page Fault =', pf, 'Page Replaces =', pr, 'Page Frames =', MAX_SIZE)
        outputstr = outputstr + 'Page Fault = ' + str(pf) + '  Page Replaces = ' + str(pr) + '  Page Frames = ' + str(MAX_SIZE) + '\n'
        return outputstr

    def DO(self):
        command = self.io.GETCOMMAND()
        if command == 1 :
            outputstr = self.FIFO()
            self.io.outputfile(outputstr)
        elif command == 2:
            outputstr = self.LRU()
            self.io.outputfile(outputstr)
        elif command == 3:
            outputstr = self.LFU()
            self.io.outputfile(outputstr)
        elif command == 4:
            outputstr = self.MFU_FIFO()
            self.io.outputfile(outputstr)
        elif command == 5:
            outputstr = self.MFU_LRU()
            self.io.outputfile(outputstr)
        elif command == 6:
            outputstr = self.FIFO() + self.LRU() + self.LFU() + self.MFU_FIFO() + self.MFU_LRU()
            self.io.outputfile(outputstr)

class GUI :
    def display(self) :
        print('1.FIFO')
        print('2.LRU')
        print('3.LFU + LRU')
        print('4.MFU + FIFO')
        print('5.MFU + LRU')
        print('6.ALL')

def main() :
    # input1_method1.txt
    print('Program starts...')
    gui = GUI()
    try :
        start = input('Start?[y/n] : ')
        while start != 'y' and start != 'n' :
            print('Try again !!!')
            start = input('Start?[y/n] : ')
        while start == 'y' :
            gui.display()
            job = PR()
            job.DO()
            start = input('Continue?[y/n] : ')
            while start != 'y' and start != 'n':
                print('Try again !!!')
                start = input('Continue?[y/n] : ')
    except:
        pass
    finally:
        print('Program exits...')

if __name__ == '__main__':
    main()