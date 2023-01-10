# organize imports
import cv2
import numpy as np
from pygame import mixer

# color to detect - drum stick
lower = [17, 15, 100]
upper = [80, 76, 220]

# initialize mixer
mixer.init()

# region coordinates
k_top, k_bottom, k_right, k_left = 140, 240, 140, 240
h_top, h_bottom, h_right, h_left = 140, 240, 250, 350
s_top, s_bottom, s_right, s_left = 140, 240, 360, 460
c_top, c_bottom, c_right, c_left = 140, 240, 470, 570
t_top, t_bottom, t_right, t_left = 140, 240, 580, 680
r_top, r_bottom, r_right, r_left = 140, 240, 690, 790
cr_top, cr_bottom, cr_right, cr_left = 140, 240, 800, 900

# ----------------------
# play sounds
# ----------------------


def playKick():
    mixer.music.load('kick.mp3')
    mixer.music.play()


def playHihat():
    mixer.music.load('hihat.mp3')
    mixer.music.play()


def playSnare():
    mixer.music.load('snare.mp3')
    mixer.music.play()


def playClap():
    mixer.music.load('Clap.mp3')
    mixer.music.play()


def playTom():
    mixer.music.load('Tom.mp3')
    mixer.music.play()


def playRide():
    mixer.music.load('Ride.mp3')
    mixer.music.play()


def playCrash():
    mixer.music.load('Crash.mp3')
    mixer.music.play()

# ----------------------
# find contours
# ----------------------


def findContours(image):
    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresholded = cv2.threshold(img, 15, 255, cv2.THRESH_BINARY)[1]
    (cnts, _) = cv2.findContours(thresholded.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    return len(cnts)


# bool for each drum
e_snare = 0
e_kick = 0
e_hihat = 0
e_clap = 0
e_tom = 0
e_ride = 0
e_crash = 0

# ----------------------
# main function
# ----------------------
if __name__ == "__main__":
    # accumulated weight
    aWeight = 0.5

    # get reference to camera
    cam = cv2.VideoCapture(0)

    # camera related tuning
    cam.set(3, 1280)
    cam.set(4, 720)
    cam.set(cv2.CAP_PROP_FPS, 60)

    # loop till user presses "q"
    while True:
        # read a frame from the camera
        status, frame = cam.read()

        # take a clone
        clone = frame.copy()
        clone = cv2.flip(clone, 1)
        clone = cv2.resize(clone, (1280, 720))

        # get the three drum regions
        reg_kick = clone[k_top:k_bottom, k_right:k_left]
        reg_hihat = clone[h_top:h_bottom, h_right:h_left]
        reg_snare = clone[s_top:s_bottom, s_right:s_left]
        reg_clap = clone[c_top:s_bottom, s_right:s_left]
        reg_tom = clone[t_top:s_bottom, s_right:s_left]
        reg_ride = clone[r_top:s_bottom, s_right:s_left]
        reg_crash = clone[cr_top:cr_bottom, cr_right:cr_left]

        # blur the regions
        reg_kick = cv2.GaussianBlur(reg_kick,  (7, 7), 0)
        reg_hihat = cv2.GaussianBlur(reg_hihat, (7, 7), 0)
        reg_snare = cv2.GaussianBlur(reg_snare, (7, 7), 0)
        reg_clap = cv2.GaussianBlur(reg_clap, (7, 7), 0)
        reg_tom = cv2.GaussianBlur(reg_tom, (7, 7), 0)
        reg_ride = cv2.GaussianBlur(reg_ride, (7, 7), 0)
        reg_crash = cv2.GaussianBlur(reg_crash, (7, 7), 0)

        l = np.array(lower, dtype="uint8")
        u = np.array(upper, dtype="uint8")

        mask_kick = cv2.inRange(reg_kick,  l, u)
        mask_hihat = cv2.inRange(reg_hihat, l, u)
        mask_snare = cv2.inRange(reg_snare, l, u)
        mask_clap = cv2.inRange(reg_clap, l, u)
        mask_tom = cv2.inRange(reg_tom, l, u)
        mask_ride = cv2.inRange(reg_ride, l, u)
        mask_crash = cv2.inRange(reg_crash, l, u)

        out_kick = cv2.bitwise_and(reg_kick,  reg_kick,  mask=mask_kick)
        out_hihat = cv2.bitwise_and(reg_hihat, reg_hihat, mask=mask_hihat)
        out_snare = cv2.bitwise_and(reg_snare, reg_snare, mask=mask_snare)
        out_clap = cv2.bitwise_and(reg_clap, reg_clap, mask=mask_clap)
        out_tom = cv2.bitwise_and(reg_tom, reg_tom, mask=mask_tom)
        out_ride = cv2.bitwise_and(reg_ride, reg_ride, mask=mask_ride)
        out_crash = cv2.bitwise_and(reg_crash, reg_crash, mask=mask_crash)

        cnts_kick = findContours(out_kick)
        cnts_hihat = findContours(out_hihat)
        cnts_snare = findContours(out_snare)
        cnts_clap = findContours(out_clap)
        cnts_tom = findContours(out_tom)
        cnts_ride = findContours(out_ride)
        cnts_crash = findContours(out_crash)

        if (cnts_kick > 0) and (e_kick == 0):
            playKick()
            e_kick = 1
        elif (cnts_kick == 0):
            e_kick = 0

        if (cnts_hihat > 0) and (e_hihat == 0):
            playHihat()
            e_hihat = 1
        elif (cnts_hihat == 0):
            e_hihat = 0

        if (cnts_snare > 0) and (e_snare == 0):
            playSnare()
            e_snare = 1
        elif (cnts_snare == 0):
            e_snare = 0

        if (cnts_clap > 0) and (e_clap == 0):
            playClap()
            e_clap = 1
        elif (cnts_clap == 0):
            e_clap = 0

        if (cnts_tom > 0) and (e_tom == 0):
            playTom()
            e_tom = 1
        elif(cnts_tom == 0):
            e_tom = 0

        if (cnts_ride > 0) and (e_ride == 0):
            playRide()
            e_ride = 1
        elif (cnts_ride == 0):
            e_ride = 0

        if (cnts_crash > 0) and (e_crash == 0):
            playCrash()
            e_crash = 1
        elif (cnts_crash == 0):
            e_crash = 0

        # draw the drum regions
        a = cv2.rectangle(clone, (k_left, k_top),
                      (k_right, k_bottom), (0, 255, 0, 0.5), 2)
        cv2.rectangle(clone, (h_left, h_top),
                      (h_right, h_bottom), (255, 0, 0, 0.5), 2)
        cv2.rectangle(clone, (s_left, s_top),
                      (s_right, s_bottom), (0, 0, 255, 0.5), 2)
        cv2.rectangle(clone, (c_left, c_top),
                      (c_right, c_bottom), (0, 0, 255, 0.5), 2)
        cv2.rectangle(clone, (t_left, t_top),
                      (t_right, t_bottom), (0, 0, 255, 0.5), 2)
        cv2.rectangle(clone, (r_left, r_top),
                      (r_right, r_bottom), (0, 0, 255, 0.5), 2)
        cv2.rectangle(clone, (cr_left, cr_top),
                      (cr_right, cr_bottom), (0, 0, 255, 0.5), 2)

 		# Texts
		
		# cv2.putText(, 'Hithat')
		# cv2.putText(, 'Snare')
		# cv2.putText(, 'Clap')
		# cv2.putText(, 'Tom')
		# cv2.putText(, 'Ride')
		# cv2.putText(, 'Crash')



        # display the frame
        cv2.namedWindow("video", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("video", clone)

        # if user presses 'q', quit the program
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    # release the camera
    cam.release()

    # destroy all windows
    cv2.destroyAllWindows()
