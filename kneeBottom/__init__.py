def check_row(row):
    index = []
    for j in range(1,row.shape[0]):#col
        if row[j] > row[j-1] :
            index.append(j) #ขึ้น
        elif row[j] < row[j-1] :
            index.append(j-1) #ลง
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
  col_idx = 0
  row_idx = 0
  x = 0
  y = 0
  single_peak = []
  peaks = []
  #find W,H
  W = 0
  max_row = 0
  for i in range(mask.shape[0]):
    row = mask[i]
    index = check_row(row)
    if len(index) == 2:
      if index[1]-index[0] > max_row:
        max_row = index[1]-index[0]  
        W = i
  ###
  for i in range(mask.shape[0]):
    row = mask[i]
    index = check_row(row)
    if len(index) != 0: # เจอเข่า
      mid = (index[0]+index[1])//2
      Q1 = max_row//4
      H = W-i
      x,y = check_peak(mask[i:i+H,mid-Q1:mid+Q1],i,mid-Q1)
      break
  return x,y