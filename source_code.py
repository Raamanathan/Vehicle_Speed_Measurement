import cv2
import sys
#import goturn_net
import time
from time import sleep

 
if __name__ == '__main__' :
 
    
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
    tracker_type = tracker_types[4]
    #tracker = cv2.Tracker_create(tracker_type)
 
    if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
    if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
    if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
 
    # Read video
    video = cv2.VideoCapture(0)
    
    v=0
 
    # Exit if video not opened.
    if not video.isOpened():
        print ("Could not open video")
        sys.exit()
 
    # Read first frame.
    ok, frame = video.read()
    #frame=frame[150:352,350:615]
    #615
    print(frame.shape[:2])
    if not ok:
        print ('Cannot read video file')
        sys.exit()
     
    # Define an initial bounding box
    #bbox = (1170,381 , 99, 101)
    bbox = (586,135,54,74)
    bbox = (0,141,54,80)
 
    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    print(bbox[0])
    print(bbox[1])
    print(bbox[2])
    print(bbox[3])
    n=bbox[0]
    #cv2.imwrite('bbox.jpg',bbox)
    #frame1=cv2.imread('bbox.jpg')
    #cv2.imshow('bbox',bbox.jpg)
    #print(frame1.shape[:2])
    #bbox=('bbox.jpg')
    avg=0
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    count=0
    start=time.time()
    fps=0
    prev=bbox[0]
    r=55
    #r=12
    q=0
    #r=input('Enter distance:')
    start1=time.time()
    f=time.time()
    flag=0
    while True:
        # Read a new frame
        ok, frame = video.read()
        frame=frame[150:352,350:615]
        #150:352,350:615
        count=count+1
        if(time.time()-start>1):
            fps=count/(time.time()-start)
            #print fps1
            
        if not ok:
            break
         
        # Start timer
       # timer = cv2.getTickCount()
 
        # Update tracker
        #f=time.time()
        
        ok, bbox = tracker.update(frame)
        
       # t=float(time.time()-f)
       # print t
       # print cX
 
        # Calculate Frames per second (FPS)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
 
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #p2 = (int(bbox[1]), int(bbox[3]))
            if(abs(bbox[0]-prev)>12):
               v=0
               q=0
               avg=0
               avg1=0
               prev=bbox[0]
               #continue
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
            #print bbox[0]
            d=abs(bbox[0]-prev)/(frame.shape[1]/r)
            prev=bbox[0]
            #t=time.time()-start1
            #print t
            #start1=time.time()
            
            if(time.time()-f>0.01):
                #print(time.time()-f)
                d=d/10
                d=d*3600
                v=d*(fps/30)
                #print(time.time()-f)
                #print (v)
                f=time.time()
            
            #d=10
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
            v=0
        if(flag!=1 and abs(n-bbox[0])>10):
            flag=1
        if(flag==1 and v):
            q=q+1
            avg=avg+v
            #print 'avg='
            #print avg
        avg1=0
        if(q!=0):
            avg1=avg/q
            if(avg1>5 and avg1<75):
              print (avg1)
        # Display tracker type on frame
        #cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
     
        # Display FPS on frame
        #cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        #cv2.putText(frame, "velocity : " + str(float(v)), (100,120), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
        cv2.putText(frame, "velocity : " + str(float(avg1)), (int(bbox[0]-10),int(bbox[1]-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
 
        # Display result
        cv2.imshow("Tracking", frame)
 
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
        #C:\Users\Ramanathan\Documents\Bandicam
