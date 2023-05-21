import numpy as np

def check_row(row):
    row = np.append(row, 0, axis=None)
    row = np.insert(row, 0,0)
    index = []
    for j in range(1,row.shape[0]):#col
        if row[j] > row[j-1] :
            index.append(j-1) #ขึ้น
        elif row[j] < row[j-1] :
            index.append(j-2) #ลง
    return index # เก็บตำแหน่งขึนลง

def check_peak(mask,x,y):
    peaks = []
    for row in mask:
      index = check_row(row)
      peaks.append(index)
    for i in range(len(peaks)):
      if len(peaks[i]) != 2 and len(peaks[i])%2 == 0 and len(peaks[i]) > 0 and i < 0.2*(mask.shape[1]): #เจอ 2 peak
        first = (peaks[i][0]+peaks[i][1])//2
        second = (peaks[i][2]+peaks[i][3])//2
        y1 = (first+second)//2
        return x+i,y+y1
      if i == len(peaks)-1: #มีเขาลูกเดียว
        y1 = (peaks[0][0]+peaks[0][1])//2
        return x,y+y1

def find_tibia_point(mask):
  tmp = np.sum(mask, axis=1)
  row_where = np.where(tmp > 0)[0]
  lowest = row_where[-1]
  highest = row_where[0]  
  col_idx = 0
  row_idx = 0
  x = 0
  y = 0
  single_peak = []
  peaks = []
  #find W,H
  W = 0
  max_row_l = 0
  max_row_r = 0
  for i in range(highest,lowest):
    row = mask[i]
    index = check_row(row)
    if len(index) == 2:
      if index[1]-index[0] > max_row_r-max_row_l:
        max_row_r = index[1]
        max_row_l = index[0]  
        W = i
  ###
  mid_of_max = (max_row_r + max_row_l)//2
  Q1 = (max_row_r-max_row_l)//4
  for i in range(highest,lowest):
    row = mask[i, mid_of_max-Q1:mid_of_max+Q1] #แต่ละแถว
    tab = mid_of_max-Q1
    index = check_row(row)
    if len(index) != 0 and len(index)%2 == 0: # เจอเข่า
      mid = (index[0]+tab+index[1]+tab)//2
      x,y = check_peak(mask[i:W,mid-Q1:mid+Q1],i,mid-Q1)
      break
  return x,y