#xlrd library reads excel files
import xlrd
# numpy lib works with linear algerbra
import numpy as np

#both xlwt and xlrd work only with .xls files (excel 97-03) !!!!!
import sys
#GUI to select file
from Tkinter import Tk
from tkFileDialog import askopenfilename

flag = input("Enter manually End Member Matrix (0) or Read a file (1), enter 0/1:")
end_m=[]
if flag == 0 :  
    data = input("Enter 1 row 1 value: ")
    end_m.append(data)
    data = input("Enter 1 row 2 value: ")
    end_m.append(data)
    data = input("Enter 1 row 3 value: ")
    end_m.append(data)
    data = input("Enter 1 row 4 value: ")
    end_m.append(data)
    data = input("Enter 2 row 1 value: ")
    end_m.append(data)
    data = input("Enter 2 row 2 value: ")
    end_m.append(data)
    data = input("Enter 2 row 3 value: ")
    end_m.append(data)
    data = input("Enter 2 row 4 value: ")
    end_m.append(data)
    data = input("Enter 3 row 1 value: ")
    end_m.append(data)
    data = input("Enter 3 row 2 value: ")
    end_m.append(data)
    data = input("Enter 3 row 3 value: ")
    end_m.append(data)
    data = input("Enter 3 row 4 value: ")
    end_m.append(data)
elif flag ==1 :
    #taken from https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog
    print 'Select End Member Matrix File'
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    Path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    end_m = np.genfromtxt(Path, delimiter = ',')
    row = input("Enter which is first row of data: ")-1
    col = input("Enter which is first column of data: ")-1
    end_m = end_m[row:,col:]

else:
    print 'Wrong input; should be 0 or 1'
end_m=np.asarray(end_m)
end_m=end_m.reshape([3,4])

#taken from https://stackoverflow.com/questions/3579568/choosing-a-file-in-python-with-simple-dialog

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
Path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
print 'Select Data File'
#fi=open(Path, 'r')
data = np.genfromtxt(Path, delimiter = ',')

row = input("Enter which is first row of data: ")-1
col = input("Enter which is first column of data: ")-1

data = data[row:,col:]
# creating B matrix
B = np.transpose(np.matrix('0,0,1'))

flag = input("Enter the output format  (0) for csv; (1) for excel,\n note that for excel it is necessary to intall xlwt library\n enter 0/1:")
fo = raw_input("Enter output file name ")

if flag==0:
    csv = open(str(fo)+'.csv', "w")
    csv.write('fxb, fyb, fzb, fx.13C, fy.13C, fz.13C, fx.CN, fy.CN, fz.CN\n')
else:
    # xlwt lib writes output to excel file
    import xlwt
    #opening excel workbook to write there output
    wb = xlwt.Workbook()
    #opening first spreadsheet in workbook
    ws = wb.add_sheet('Sheet 1')
    #writing headers into excel file
    ws.write(0, 0, 'fxb')
    ws.write(0, 1, 'fyb')
    ws.write(0, 2, 'fzb')
    ws.write(0, 3, 'fx,13C')
    ws.write(0, 4, 'fy,13C')
    ws.write(0, 5, 'fz,13C')
    ws.write(0, 6, 'fx,CN')
    ws.write(0, 7, 'fy,CN')
    ws.write(0, 8, 'fz,CN')

#creating loop which goes from the second row to the end row of the document          
for i in range(len (data)):
    calc_data=[]
    for j in range(len(end_m)):
        calc_data.append((end_m[j][0]-data[i][0])*end_m[j][2])
        calc_data.append((end_m[j][1]-data[i][1])*end_m[j][3])
        calc_data.append(1)
    Data_M= np.linalg.inv(np.transpose(np.asarray(calc_data).reshape((3, 3))))
    Data_final = np.dot(Data_M,B)
    fx_13c=float(Data_final[0]*end_m.item((0, 2))/(Data_final[0]*end_m.item((0, 2))+Data_final[1]*end_m.item((1, 2))+Data_final[2]*end_m.item((2, 2))))
    fy_13c=float(Data_final[1]*end_m.item((1, 2))/(Data_final[0]*end_m.item((0, 2))+Data_final[1]*end_m.item((1, 2))+Data_final[2]*end_m.item((2, 2))))
    fz_13c=float(Data_final[2]*end_m.item((2, 2))/(Data_final[0]*end_m.item((0, 2))+Data_final[1]*end_m.item((1, 2))+Data_final[2]*end_m.item((2, 2))))

    fx_CN=float(Data_final[0]*end_m.item((0, 3))/(Data_final[0]*end_m.item((0, 3))+Data_final[1]*end_m.item((1, 3))+Data_final[2]*end_m.item((2, 3))))
    fy_CN=float(Data_final[1]*end_m.item((1, 3))/(Data_final[0]*end_m.item((0, 3))+Data_final[1]*end_m.item((1, 3))+Data_final[2]*end_m.item((2, 3))))
    fz_CN=float(Data_final[2]*end_m.item((2, 3))/(Data_final[0]*end_m.item((0, 3))+Data_final[1]*end_m.item((1, 3))+Data_final[2]*end_m.item((2, 3))))
    if flag == 0 :
        csv.write( str(float(Data_final[0]))+','+str(float(Data_final[1]))+','+str(float(Data_final[2]))+','+str(fx_13c)+','+str(fy_13c)+','+str(fz_13c)+','+str(fx_CN)+','+str(fy_CN)+','+str(fz_CN)+'\n')
    else:
        ws.write(i+1, 0, float(Data_final[0]))
        ws.write(i+1, 1, float(Data_final[1]))
        ws.write(i+1, 2, float(Data_final[2]))
        ws.write(i+1, 3, float(fx_13c))
        ws.write(i+1, 4, float(fy_13c))
        ws.write(i+1, 5, float(fz_13c))
        ws.write(i+1, 6, float(fx_CN))
        ws.write(i+1, 7, float(fy_CN))
        ws.write(i+1, 8, float(fz_CN))
if flag==0:
    csv.close()
else:
    wb.save(str(fo)+'.xls')
