import threading
import cv2
import numpy as np
import datetime
from imutils.video import VideoStream
from app.models import Livestream, User
from flask_login import current_user
import imutils
from app.snitcher.motion_detection.singlemotiondetector import \
    SingleMotionDetector

stop_threads = False

def terminate():
    global stop_threads
    stop_threads = True
    t.join() # Killing threads
    for stream in vs:
        stream.stop() # Shutting off all cameras

def init():
    global outputFrame, lock, vs, fourcc, writer, h, w, zeros_, names, t
    outputFrame = None
    lock = threading.Lock()
    # Fetching internal_ip of all cameras in the network
    user_id = current_user.get_id()
    ips = Livestream.query.filter_by(id_user=user_id).all()
    vs = [VideoStream(src=str(x.internal_ip)).start() for x in ips]
    names = [x.name for x in ips]
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    buff = [None for x in range(len(vs))] # NoneType
    writer = buff
    h = buff
    w = buff
    zeros_ = buff
    t = threading.Thread(target=detect_motion, args=(32,))
    t.daemon = True
    t.start()

# Runs with the thread
def detect_motion(frameCount):
    global stop_threads
    # grab global references to the video stream, output frame, and
    # lock variables

    # initialize the motion detector and the total number of frames
    # read thus far
    md = SingleMotionDetector(accumWeight=0.1)
    #detector = MTCNN() # Initializng face detector
    total = 0

    # loop over frames from the video stream
    while True:
        if stop_threads:
            break
        # read the next frame from the video stream, resize it,
        # convert the frame to grayscale, and blur it
        
        # No list comprehension because of many operations
        for i, vsi in enumerate(vs): # vsi is a tuple (videoObject, livestream_name)
            frame = vsi.read()
            frame = cv2.flip(frame, 1)
            frame = imutils.resize(frame, width=400)
            #faces = detector.detect_faces(frame)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (7, 7), 0)

            if writer[i] is None:
                (m, n) = frame.shape[:2]
                h[i]=m
                w[i]=n
                writer_ = cv2.VideoWriter("data/motion/{0}.avi".format(names[i]), fourcc, 20,
                (n, m), True)
                writer[i] = writer_
                zeros_[i] = np.zeros((m, n), dtype="uint8")

            # grab the current timestamp and draw it on the frame
            timestamp = datetime.datetime.now()

            # Comparing original files
            '''
            for face in faces:
                x, y, width, height = face["box"]
                sub_face = frame[y-20:y + height+20, x-20:x + width+20]
                #cv2.imwrite("data/new/"+str(timestamp.strftime("%d%B%Y%I%M%S%p"))+".jpg", sub_face)
                cv2.rectangle(frame, (x, y), (x+width, y+height), (255,0,0), 2)'''
            cv2.putText(frame, "Dotmole", (10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,191,0), 2)

            cv2.putText(frame, timestamp.strftime(
                "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 191, 0), 1)
            # if the total number of frames has reached a sufficient
            # number to construct a reasonable background model, then
            # continue to process the frame
            if total > frameCount:
                # detect motion in the image
                motion = md.detect(gray)

                # cehck to see if motion was found in the frame
                if motion is not None:
                    # unpack the tuple and draw the box surrounding the
                    # "motion area" on the output frame
                    (thresh, (minX, minY, maxX, maxY)) = motion
                    output = np.zeros((m, n, 3), dtype="uint8")
                    output[0:m, 0:n] = frame

                    # write the output frame to file
                    writer_.write(output)
                    cv2.putText(frame, "Motion", (minX, minY -10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.35, (255,191,0),1)
                    cv2.rectangle(frame, (minX, minY), (maxX, maxY),
                        (255, 191, 0), 2)  # Send the motion-ed area as a notification
                    
                    # Do face_recognition
                    # face with images would be there
                    # Now recognize
            
            # update the background model and increment the total number
            # of frames read thus far
            md.update(gray)
            total += 1

            # acquire the lock, set the output frame, and release the
            # lock
            with lock:
                outputFrame = frame.copy()
'''
# Helps to show		
def generate():
    global outputFrame, lock
	# grab global references to the output frame and lock variables

	# loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue

            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

            # ensure the frame was successfully encoded
            if not flag:
                continue

        # yield the output frame in the byte format
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encodedImage) + b'\r\n')'''