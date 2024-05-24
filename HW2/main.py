import os
import copy

def SortWithIndexlist(list, indexstr1, indexstr2, indexstr3):
    sort = []
    if len(list) > 0:
        sort.append(list[0])
        size = len(list)
        added = False
        # sort with cpu burst
        for i in range(1, size):
            for j in range(0, len(sort)):
                if int(list[i][indexstr1]) < int(sort[j][indexstr1]):
                    sort.insert(j, list[i])
                    added = True
                    break

                elif int(list[i][indexstr1]) == int(sort[j][indexstr1]):
                    if int(list[i][indexstr2]) < int(sort[j][indexstr2]):
                        sort.insert(j, list[i])
                        added = True
                        break
                    elif int(list[i][indexstr2]) == int(sort[j][indexstr2]):
                        if int(list[i][indexstr3]) < int(sort[j][indexstr3]):
                            sort.insert(j, list[i])
                            added = True
                            break

            if added == False:
                sort.append(list[i])
            added = False

        return sort
    else:
        return list

def LISTinsertPPRR(list,p1,indexstr1) :
        # insert a process to the last of same priority
        added = False

        for i in range(0, len(list)):
            if int(p1[indexstr1]) < int(list[i][indexstr1]) :
                list.insert(i, p1)
                added = True
                break
        if added == False:
            list.append(p1)

        # print('ready to be process job')
        # for i in list:
        #     print(i)
        # print('-----------------------')
        return list

def LISTremovePPRR(list,currenttime):
        newlist = []
        for p in list :
            if int(p['Arrival Time']) > currenttime :
                newlist.append(p)
        return newlist

def Filter(list,indexstr1):
        # 符合在currenttime內的list
        smallest = list[0]
        for p in list :
            if int(p[indexstr1]) < int(smallest[indexstr1]) :
                smallest = p
        for p in list:
            if int(p[indexstr1]) == int(smallest[indexstr1]) and int(p['ID']) < int(smallest['ID']) :
                smallest = p

        return smallest

def CheckID(ID):
        IDnum = int(ID)
        if IDnum >= 0 and IDnum <= 9 :
            pass
        else :
            ID = chr(65+IDnum-10)
        return ID

def addwaitingtime(jobdone,ID) :
    #以保證<currenttime的process都在jobdone
    if len(jobdone) > 0:
        for j in jobdone :
            if j['ID'] == ID :
                pass
            else :
                if int(j['Turnaround Time']) == 0 :
                    j['Waiting Time'] = int(j['Waiting Time']) + 1

def addturnaroundtime(jobdone,ID,currenttime,arrival) :
    if len(jobdone) > 0:
        for j in jobdone :
            if j['ID'] == ID :
                j['Turnaround Time'] = currenttime - arrival

class IO :
    def __init__(self):
        self.vec_nums = []
        self.fileName = str()
        self.command = -1
        self.timeslice = 1

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
                        self.timeslice = int(cin[1])
                        format1 = {'ID' :int(), 'CPU Burst':int() , 'Arrival Time':int(), 'Priority':int()}
                        for i in range(2,size) :
                            buffer = data[i].split()
                            for j in range(len(buffer)) :
                                if j == 0 :
                                    format1['ID'] = buffer[j]
                                elif j == 1:
                                    format1['CPU Burst'] = buffer[j]
                                elif j == 2:
                                    format1['Arrival Time'] = buffer[j]
                                elif j == 3:
                                    format1['Priority'] = buffer[j]

                            v_size = len(self.vec_nums)
                            #print(v_size)
                            added = False
                            if v_size == 0 :
                                self.vec_nums.append(format1)
                                added = True
                            elif v_size > 0 :
                                for k in range (v_size) :
                                    if int(format1['Arrival Time']) < int(self.vec_nums[k]['Arrival Time']):
                                        self.vec_nums.insert(k,format1)
                                        #print(self.vec_nums)
                                        added = True
                                        break

                                    elif int(format1['Arrival Time']) == int(self.vec_nums[k]['Arrival Time']):
                                        if int(format1['ID']) < int(self.vec_nums[k]['ID']):
                                            self.vec_nums.insert(k,format1)
                                            #print(self.vec_nums)
                                            added = True
                                            break

                            if added == False :
                                self.vec_nums.append(format1)
                            added = False
                            format1 = {'ID': int(), 'CPU Burst': int(), 'Arrival Time': int(), 'Priority': int()}
                    file.close()
                    self.fileName = fileName
                    return True
        # except :
        #     print('exception')
        #     return False

    def outputfile(self,Gantt,waitinglist,turnaroundtimelist):
        outputfilename = 'out_' + self.fileName[:-4] + '.txt'
        with open('output/'+outputfilename, 'w') as f:
            if self.command == 1 :
                f.write('FCFS\n' + '==        FCFS==\n')
                f.write(Gantt)
                f.write('\n')
                f.write('===========================================================')
                f.write('\n')

                f.write('\nWaiting Time\n')
                f.write('ID\tFCFS\t\n')

                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist :
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['FCFS'])+'\t\n')
                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time\n')
                f.write('ID\tFCFS\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['FCFS'])+'\t\n')

                f.write('===========================================================')
                f.write('\n\n')
            elif self.command == 2 :
                f.write('RR\n' + '==          RR==\n')
                f.write(Gantt)
                f.write('\n')
                f.write('===========================================================')
                f.write('\n')

                f.write('\nWaiting Time\n')
                f.write('ID\tRR\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['RR'])+'\t\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time\n')
                f.write('ID\tRR\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['RR'])+'\t\n')

                f.write('===========================================================')
                f.write('\n\n')
            elif self.command == 3 :
                f.write('SRTF\n' + '==        SRTF==\n')
                f.write(Gantt)
                f.write('\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nWaiting Time\n')
                f.write('ID\tSRTF\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['SRTF'])+'\t\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time\n')
                f.write('ID\tSRTF\t\n')
                f.write('===========================================================')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['SRTF'])+'\t\n')

                f.write('===========================================================')
                f.write('\n\n')
            elif self.command == 4 :
                f.write('Priority RR\n' + '==        PPRR==\n')
                f.write(Gantt)
                f.write('\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nWaiting Time\n')
                f.write('ID\tPPRR\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['PPRR'])+'\t\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time\n')
                f.write('ID	PPRR	\n')
                f.write('===========================================================')
                f.write('\n')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['PPRR'])+'\t\n')

                f.write('===========================================================')
                f.write('\n\n')
            elif self.command == 5 :
                f.write('HRRN\n' + '==        HRRN==\n')
                f.write(Gantt)
                f.write('\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nWaiting Time\n')
                f.write('ID\tHRRN\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['HRRN'])+'\t\n')

                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time\n')
                f.write('ID\tHRRN\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t')
                    f.write(str(i['HRRN'])+'\t\n')
                f.write('===========================================================')
                f.write('\n\n')
            elif self.command == 6 :
                f.write('All\n')
                f.write(Gantt)
                f.write('===========================================================\n')
                f.write('\nWaiting Time')
                f.write('\nID\tFCFS\tRR\tSRTF\tPPRR\tHRRN\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in waitinglist:
                    f.write(str(i['ID'])+'\t'+str(i['FCFS'])+'\t'+str(i['RR'])+'\t'+str(i['SRTF'])+'\t'+str(i['PPRR'])+'\t'+str(i['HRRN'])+'\t\n')
                f.write('===========================================================')
                f.write('\n')

                f.write('\nTurnaround Time')
                f.write('\nID\tFCFS\tRR\tSRTF\tPPRR\tHRRN\t\n')
                f.write('===========================================================')
                f.write('\n')
                for i in turnaroundtimelist:
                    f.write(str(i['ID'])+'\t'+str(i['FCFS'])+'\t'+str(i['RR'])+'\t'+str(i['SRTF'])+'\t'+str(i['PPRR'])+'\t'+str(i['HRRN'])+'\t\n')
                f.write('===========================================================')
                f.write('\n\n')
            f.close()

    def clear(self) :
        self.vec_nums = []

    def size(self) :
        return len(self.vec_nums)

    def getarr(self) :
        return self.vec_nums
    def get(self):
        return self.timeslice

    def printarr(self,arr) :
        size = len(arr)
        print(size)
        for i in range(size) :
            print( "[" + str(i+1) + "] " + str(arr[i]))

class Scheduling :
    def __init__(self):
        self.timeslice = 1

    def settimeslice(self,timeslice):
        self.timeslice =  timeslice

    def FCFS(self,copylist):
        s = copy.deepcopy(copylist)
        size = len(s)
        currenttime = 0
        g = str()
        i = 0
        jobdone = []
        while i < size :
            if int(s[i]['Arrival Time']) <= currenttime : # when arrival time <= currenttime then do it
                burst = int(s[i]['CPU Burst'])
                w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                w['ID'] = s[i]['ID']
                w['Waiting Time'] = currenttime - int(s[i]['Arrival Time'])
                w['Turnaround Time'] = currenttime + burst - int(s[i]['Arrival Time'])
                jobdone.append(w)
                ID = CheckID(s[i]['ID'])
                for j in range(burst) :
                    g=g+ID
                currenttime = currenttime + burst
                i = i + 1
            else : # arrival time > currenttime
                idletime = int(s[i]['Arrival Time']) - currenttime
                # when there is no new coming job
                # idling
                for j in range(idletime) :
                    currenttime = currenttime + 1
                    g = g+'-'
        jobdone = SortWithIndexlist(jobdone,'ID','Waiting Time','Turnaround Time')
        # for i in jobdone :
        #     print(i)
        # print(g)
        return g, jobdone

    def RR(self,copylist):
        s = copy.deepcopy(copylist)
        currenttime = 0
        timeslice = self.timeslice
        q = []
        jobdone = []
        g = str()

        while len(q) > 0 or len(s) > 0:
            # s 有照arrival time來排
            if len(q) > 0 : # when have jobs to do then do the job
                job = q.pop(0)
                ID = CheckID(job['ID'])
                burst = int(job['CPU Burst'])
                timeleft = burst
                if timeleft > timeslice :
                    timeleft = timeleft - timeslice
                    for i in range(timeslice):
                        currenttime = currenttime + 1
                        g = g + ID
                        for j in jobdone:
                            if j['ID'] == job['ID']:
                                # 輪到你做一個timeslice
                                pass
                            else:
                                if int(j['Turnaround Time']) == 0:
                                    # 還沒輪到你做完，現在正在做別的process
                                    j['Waiting Time'] = int(j['Waiting Time']) + 1

                        while len(s) > 0 and int(s[0]['Arrival Time']) <= currenttime:
                            #讓時間到的工作去queue裡等
                            w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                            w['ID'] = s[0]['ID']
                            w['Waiting Time'] = 0
                            w['Turnaround Time'] = 0
                            jobdone.append(w)
                            q.append(s.pop(0))

                    job['CPU Burst'] = timeleft
                    q.append(job)

                else :
                    for i in range(timeleft):
                        currenttime = currenttime + 1
                        g = g + ID
                        for j in jobdone:
                            if j['ID'] == job['ID']:
                                if i+1 == timeleft :
                                    # 做完了
                                    j['Turnaround Time'] = currenttime - int(job['Arrival Time'])
                                pass
                            else:
                                if int(j['Turnaround Time']) == 0:
                                    # 還沒輪到你做完，現在正在做別的process
                                    j['Waiting Time'] = int(j['Waiting Time']) + 1

                        while len(s) > 0 and int(s[0]['Arrival Time']) <= currenttime:
                            w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                            w['ID'] = s[0]['ID']
                            w['Waiting Time'] = 0
                            w['Turnaround Time'] = 0
                            jobdone.append(w)
                            q.append(s.pop(0))

            else : # q is empty
                if int(s[0]['Arrival Time']) > currenttime :
                    idletime = int(s[0]['Arrival Time']) - currenttime
                    for i in range(idletime):
                        currenttime = currenttime + 1
                        g = g + '-'

                while int(s[0]['Arrival Time']) <= currenttime:
                    w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                    w['ID'] = s[0]['ID']
                    w['Waiting Time'] = 0
                    w['Turnaround Time'] = 0
                    jobdone.append(w)
                    q.append(s.pop(0))

        jobdone = SortWithIndexlist(jobdone, 'ID', 'Waiting Time', 'Turnaround Time')
        # for i in jobdone :
        #     print(i)
        # print(g)
        return g, jobdone

    def SRTF(self,copylist):
        # burst > arrival > id
        s = copy.deepcopy(copylist)
        g = str()
        currenttime = 0
        step = False
        jobdone = []
        sort = SortWithIndexlist(s, 'CPU Burst','Arrival Time','ID')

        while len(s) > 0 :
            sort = SortWithIndexlist(s, 'CPU Burst', 'Arrival Time','ID')
            for i in s:
                setw = False
                if int(i['Arrival Time']) <= currenttime:
                    for j in jobdone:
                        if j['ID'] == i['ID']:
                            setw = True
                    if setw == False :
                        w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                        w['ID'] = i['ID']
                        w['Waiting Time'] = 0
                        w['Turnaround Time'] = 0
                        jobdone.append(w)
            for p in sort :
                if int(p['Arrival Time']) <= currenttime :
                    ID = CheckID(p['ID'])
                    for p1 in s :
                        if p1['ID'] == p['ID'] :
                            currenttime = currenttime + 1
                            g = g + ID
                            addwaitingtime(jobdone, p1['ID'])
                            p1['CPU Burst'] = int(p1['CPU Burst']) -1
                            if int(p1['CPU Burst']) == 0 :
                                addturnaroundtime(jobdone, p1['ID'], currenttime, int(p1['Arrival Time']))
                                s.remove(p1)
                    # currenttime = currenttime + 1
                    # g = g + ID
                    step = True
                    break
            if step == False :
                currenttime = currenttime + 1
                g = g + '-'
            step = False
        jobdone = SortWithIndexlist(jobdone, 'ID', 'Waiting Time', 'Turnaround Time')
        # for i in jobdone :
        #     print(i)
        # print(g)
        return g, jobdone

    def PPRR(self,copylist):
        # burst > arrival > id
        s = copy.deepcopy(copylist)
        list = []
        jobdone = []
        processing = False
        g = str()
        timeslice = self.timeslice
        currenttime = 0
        highjob = {'ID' :int(), 'CPU Burst':int() , 'Arrival Time':int(), 'Priority':int()}
        setjob = False
        sort = SortWithIndexlist(s, 'Priority', 'Arrival Time', 'ID')
        while len(sort) > 0 or len(list) > 0 or int(highjob['CPU Burst']) > 0:
            for i in range(len(sort)) :
                if int(sort[i]['Arrival Time']) <= currenttime :
                    w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int()}
                    w['ID'] = sort[i]['ID']
                    w['Waiting Time'] = 0
                    w['Turnaround Time'] =0
                    jobdone.append(w)
                    list = LISTinsertPPRR(list,sort[i],'Priority')
                    processing = True

            if setjob == True and len(list) == 0 :
                if int(highjob['CPU Burst']) == 0:
                    processing = False

            sort = LISTremovePPRR(sort,currenttime)
            if processing == True:
                if timeslice == self.timeslice :
                    #print('time out job/ new job')
                    if len(list) > 0 :
                        highjob = list.pop(0)
                        setjob = True

                else :
                    if len(list) > 0 :
                        if int(highjob['CPU Burst']) == 0 :
                            timeslice = self.timeslice
                            highjob = list.pop(0)
                            setjob = True

                        elif int(highjob['Priority']) <= int(list[0]['Priority']) :
                            # not timeout and there is no higher Priority than this job
                            # print('same job')
                            pass
                        else :
                            # new high priority job , been preemptive
                            # print('preemptive job')
                            timeslice = self.timeslice
                            # put last job back
                            list = LISTinsertPPRR(list, highjob, 'Priority')
                            highjob = list.pop(0)
                            setjob = True

                if int(highjob['CPU Burst']) == 0:
                    # idle
                    timeslice == self.timeslice
                    currenttime = currenttime + 1
                    g = g + '-'
                else :
                    timeslice = timeslice -1
                    highjob['CPU Burst'] = int(highjob['CPU Burst']) -1
                    ID = CheckID(highjob['ID'])
                    currenttime = currenttime + 1
                    g = g + ID
                    addwaitingtime(jobdone,highjob['ID'])
                    if timeslice == 0 :
                        # timeout give new timeslice
                        timeslice = self.timeslice
                        if int(highjob['CPU Burst']) > 0 :
                            list = LISTinsertPPRR(list, highjob, 'Priority')


                    if int(highjob['CPU Burst']) == 0 :
                        addturnaroundtime(jobdone,highjob['ID'],currenttime,int(highjob['Arrival Time']))
                        timeslice == self.timeslice

            else :
                currenttime = currenttime + 1
                g = g + '-'

        jobdone = SortWithIndexlist(jobdone, 'ID', 'Waiting Time', 'Turnaround Time')
        # for i in jobdone :
        #     print(i)
        # print(g)
        return g, jobdone

    def HRRN(self,copylist):
        jobdone = []
        currenttime = 0
        g = str()
        s = copy.deepcopy(copylist)
        s = SortWithIndexlist(s,'Arrival Time' , 'ID','Priority')
        rr = float()
        setw = False

        while len(s) > 0 :
            for p in s:
                if int(p['Arrival Time']) <= currenttime:
                    waitingtime = currenttime - int(p['Arrival Time'])
                    newrr = (waitingtime + int(p['CPU Burst'])) / int(p['CPU Burst'])
                    if newrr > rr :
                        setw = True
                        w = {'ID': int(), 'Waiting Time': int(), 'Turnaround Time': int(), 'Response Ratio': float()}
                        w['ID'] = p['ID']
                        w['Waiting Time'] = currenttime - int(p['Arrival Time'])
                        w['Turnaround Time'] = currenttime + int(p['CPU Burst']) - int(p['Arrival Time'])
                        w['Response Ratio'] = (waitingtime + int(p['CPU Burst'])) / int(p['CPU Burst'])
                        rr = w['Response Ratio']
                        p_rev = copy.deepcopy(p)

            if setw == False :
                g = g + '-'
                currenttime = currenttime + 1

            else :
                #找到最大RR
                setw = False
                ID = CheckID(w['ID'])
                for i in range (int(p_rev['CPU Burst'])) :
                    g = g + ID
                    currenttime = currenttime + 1

                jobdone.append(w)
                if p_rev in s :
                    s.remove(p_rev)
                rr = 0

        jobdone = SortWithIndexlist(jobdone, 'ID', 'Waiting Time', 'Turnaround Time')
        # for i in jobdone :
        #     print(i)
        # print(g)
        return g,jobdone

    def ALL(self,copylist):
        out = str()
        processlist = copy.deepcopy(copylist)
        turnaround = []
        wait = []
        GanttFCFS,timelist = self.FCFS(processlist)
        out = out + '==        FCFS==\n'
        out = out + GanttFCFS + '\n'
        for p in timelist :
            wformat = {'ID': int(), 'FCFS': int(), 'RR': int(), 'SRTF': int(), 'PPRR': int(), 'HRRN': int()}
            tformat = {'ID': int(), 'FCFS': int(), 'RR': int(), 'SRTF': int(), 'PPRR': int(), 'HRRN': int()}
            wformat['ID'] = p['ID']
            wformat['FCFS'] = int(p['Waiting Time'])
            tformat['ID'] = p['ID']
            tformat['FCFS'] = int(p['Turnaround Time'])
            wait.append(wformat)
            turnaround.append(tformat)
        GanttRR,timelist = self.RR(processlist)
        out = out + '==          RR==\n'
        out = out + GanttRR + '\n'
        for p in timelist :
            for w in wait :
                if w['ID'] == p['ID'] :
                    w['RR'] = int(p['Waiting Time'])
                    break
            for t in turnaround :
                if t['ID'] == p['ID'] :
                    t['RR'] = int(p['Turnaround Time'])
                    break
        GanttSRTF,timelist = self.SRTF(processlist)
        out = out + '==        SRTF==\n'
        out = out + GanttSRTF + '\n'
        for p in timelist :
            for w in wait :
                if w['ID'] == p['ID'] :
                    w['SRTF'] = int(p['Waiting Time'])
                    break
            for t in turnaround :
                if t['ID'] == p['ID'] :
                    t['SRTF'] = int(p['Turnaround Time'])
                    break
        GanttPPRR,timelist = self.PPRR(processlist)
        out = out + '==        PPRR==\n'
        out = out + GanttPPRR + '\n'
        for p in timelist :
            for w in wait :
                if w['ID'] == p['ID'] :
                    w['PPRR'] = int(p['Waiting Time'])
                    break
            for t in turnaround :
                if t['ID'] == p['ID'] :
                    t['PPRR'] = int(p['Turnaround Time'])
                    break
        GanttHRRN,timelist = self.HRRN(processlist)
        out = out + '==        HRRN==\n'
        out = out + GanttHRRN + '\n'
        for p in timelist :
            for w in wait :
                if w['ID'] == p['ID'] :
                    w['HRRN'] = int(p['Waiting Time'])
                    break
            for t in turnaround :
                if t['ID'] == p['ID'] :
                    t['HRRN'] = int(p['Turnaround Time'])
                    break
        # print(out)
        # for i in wait :
        #      print(i)
        # for i in turnaround :
        #      print(i)
        return out,wait,turnaround

class GUI :
    def display(self) :
        print('1.FCFS')
        print('2.RR')
        print('3.SRTF')
        print('4.PPRR')
        print('5.HRRN')
        print('6.ALL')


# Press the green button in the gutter to run the script.
def main() :
    #input1.txt
    start = True
    ui = GUI()
    while start == True :
        ui.display()
        stop = input('Want to end(y/n) ? :')
        while stop != 'y' and stop != 'n' :
            if stop == 'y' :
                start = False
            elif stop == 'n':
                start = True
            else :
                stop = input('Try again !!! want to start(y/n) ? :')
        if stop == 'n' :
            io = IO()
            list = io.getarr()
            S = Scheduling()
            S.settimeslice(io.get())
            wait = []
            turnaround = []
            if io.command == 1 :
                Gantt,timelist = S.FCFS(list)

                for p in timelist:
                    wformat = {'ID': int(), 'FCFS': int()}
                    tformat = {'ID': int(), 'FCFS': int()}
                    wformat['ID'] = p['ID']
                    wformat['FCFS'] = int(p['Waiting Time'])
                    tformat['ID'] = p['ID']
                    tformat['FCFS'] = int(p['Turnaround Time'])
                    wait.append(wformat)
                    turnaround.append(tformat)
                io.outputfile(Gantt, wait, turnaround)
            elif io.command == 2 :
                Gantt,timelist = S.RR(list)
                for p in timelist:
                    wformat = {'ID': int(), 'RR': int()}
                    tformat = {'ID': int(), 'RR': int()}
                    wformat['ID'] = p['ID']
                    wformat['RR'] = int(p['Waiting Time'])
                    tformat['ID'] = p['ID']
                    tformat['RR'] = int(p['Turnaround Time'])
                    wait.append(wformat)
                    turnaround.append(tformat)
                io.outputfile(Gantt, wait, turnaround)
            elif io.command == 3 :
                Gantt,timelist = S.SRTF(list)
                for p in timelist:
                    wformat = {'ID': int(), 'SRTF': int()}
                    tformat = {'ID': int(), 'SRTF': int()}
                    wformat['ID'] = p['ID']
                    wformat['SRTF'] = int(p['Waiting Time'])
                    tformat['ID'] = p['ID']
                    tformat['SRTF'] = int(p['Turnaround Time'])
                    wait.append(wformat)
                    turnaround.append(tformat)
                io.outputfile(Gantt, wait, turnaround)
            elif io.command == 4:
                Gantt,timelist =S.PPRR(list)
                for p in timelist:
                    wformat = {'ID': int(), 'PPRR': int()}
                    tformat = {'ID': int(), 'PPRR': int()}
                    wformat['ID'] = p['ID']
                    wformat['PPRR'] = int(p['Waiting Time'])
                    tformat['ID'] = p['ID']
                    tformat['PPRR'] = int(p['Turnaround Time'])
                    wait.append(wformat)
                    turnaround.append(tformat)
                io.outputfile(Gantt, wait, turnaround)
            elif io.command == 5:
                Gantt,timelist = S.HRRN(list)
                for p in timelist:
                    wformat = {'ID': int(), 'HRRN': int()}
                    tformat = {'ID': int(), 'HRRN': int()}
                    wformat['ID'] = p['ID']
                    wformat['HRRN'] = int(p['Waiting Time'])
                    tformat['ID'] = p['ID']
                    tformat['HRRN'] = int(p['Turnaround Time'])
                    wait.append(wformat)
                    turnaround.append(tformat)
                io.outputfile(Gantt, wait, turnaround)
            elif io.command == 6 :
                Gantt,wait,turnaround = S.ALL(list)
                io.outputfile(Gantt,wait,turnaround)
        else :
            break


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
