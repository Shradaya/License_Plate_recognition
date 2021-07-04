from datetime import datetime
def date():
    dateandtime = str(datetime.now())
    date = dateandtime.split(' ')[0]
    return date
def time():
    dateandtime = str(datetime.now())
    time = dateandtime.split(' ')[1]
    time0 = time.split(':')
    time1 = ':'.join(time0[0:2])
    return time1


def retrieve(number_plate):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://collegeproject-b5a1d.firebaseio.com', None)
    result1 = firebase.get('AndroidApplication/booking07090325/BookingCount/Bgmall',number_plate)
    result2 = firebase.get('Bgmall/EntryExitRecords/',number_plate)
    if(result1==None and result2==None):
        return None
    else:
        return 'Booked'

def updatewhenentry(number_plate):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://collegeproject-b5a1d.firebaseio.com', None)
    data1 = {'Entry':time(),'Exit':'','Date':date(), 'LicensePlate':number_plate}
    data2 = {'Entry':number_plate}
    result1 = firebase.put('Bgmall/EntryExitRecords/'+number_plate,'a',data1)
    result2 = firebase.put('EntryExitRecordBackup/BGMall/'+date()+'/'+'Entry/'+time(),'b',data2)
    firebase.delete('AndroidApplication/booking07090325/BookingCount/Bgmall',number_plate)
    countVehiclesInParking()
    return 'entry'

def updatewhenexit(number_plate):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://collegeproject-b5a1d.firebaseio.com', None)
    dictname=[]
    for i in firebase.get('Bgmall/EntryExitRecords/',number_plate).keys():
        dictname.append(i)
    entry = firebase.get('Bgmall/EntryExitRecords/'+number_plate+'/'+dictname[-1]+'/','Entry')
    firebase.delete('Bgmall/EntryExitRecords/',number_plate)
    data1 = {'Entry':entry,'Exit':time(),'Date':date(), 'LicensePlate':number_plate}
    data2 = {'Exit':number_plate}
    result1 = firebase.put('Bgmall/EntryExitRecords/'+number_plate,'a',data1)
    result2 = firebase.put('EntryExitRecordBackup/BGMall/'+date()+'/'+'Exit/'+time(),'b',data2)
    countVehiclesInParking()
    return 'exit'


def checkforentryorexit(number_plate):
    from firebase import firebase
    firebase = firebase.FirebaseApplication('https://collegeproject-b5a1d.firebaseio.com', None)
    result = firebase.get('Bgmall/EntryExitRecords/',number_plate)
    dictname=[]
    if(result==None):
        rvar = updatewhenentry(number_plate)
        return rvar
    else:
        for i in result.keys():
            dictname.append(i)
        exit = firebase.get('Bgmall/EntryExitRecords/'+number_plate+'/'+dictname[-1]+'/','Exit')
        if(len(exit.split(':'))==2):
            result = firebase.get('AndroidApplication/booking07090325/BookingCount/Bgmall',number_plate)
            if(result == None):
                return None
            else:
                rvar = updatewhenentry(number_plate)
                return rvar
        else:    
            rvar = updatewhenexit(number_plate)	
            return rvar


def countVehiclesInParking():
    from firebase import firebase
    r1=[]
    a = 0
    firebase = firebase.FirebaseApplication('https://collegeproject-b5a1d.firebaseio.com', None)
    result1 = firebase.get('EntryExitRecordBackup/BGMall/'+date()+'/','Entry')
    result2 = firebase.get('EntryExitRecordBackup/BGMall/'+date()+'/','Exit')
    result3 = firebase.get('AndroidApplication/booking07090325/BookingCount','Bgmall')
    resultList = [result1,result2,result3]
    for j in resultList:
        try:    
            for i in j.keys():
                r1.append(i)
            if j==result2:
                a=a-len(r1)
            else:
                a=a+len(r1)
            del r1[:]
        except Exception as e:
            print("Error Encountered")
    if a<=0:
        data = {'Filled':0}
    else:
        data = {'Filled':a-1}
    result4 = firebase.put('Bgmall/FilledParkingSpace','a',data)