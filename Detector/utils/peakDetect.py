import cv2
import numpy as np
from peakdetect import peakdetect

def smooth(y, box_pts=100):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def peakDetection(y, p_threshold=-1, v_threshold=-1):
  [peaks_raw, valleys_raw] = peakdetect(y, lookahead=256)
  peaks = []
  valleys=[]

  for peak in peaks_raw:
    if p_threshold == -1 or peak[1] > p_threshold:
      peaks.append(peak[0])

  for valley in valleys_raw:
    if v_threshold == -1 or valley[1] < v_threshold:
      valleys.append(valley[0])
  
  return peaks, valleys

def getBreakpoint(img, box_pts=256):
    _, img_thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    hist = np.sum(img_thresh, axis=0)

    hist = smooth(hist, box_pts=box_pts)
    peaks, valleys = peakDetection(hist)

    if len(valleys)==1:
        breakpoint_ = valleys[0]
    elif len(valleys)==0:
        breakpoint_ = len(hist)//2
    else:
        mid = len(hist)/2
        id_ = np.argmin([abs(v - len(hist)//2) for v in valleys])
        breakpoint_ = valleys[id_]
    
    return breakpoint_