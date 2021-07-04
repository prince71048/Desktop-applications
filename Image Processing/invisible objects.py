import cv2
import numpy
# by default selected color is blue ------> if you want to select our color so you can set in Bar
# current Frame - my_colloth + first_frame  = Invisible cloak


#initial function for the callin of the trackbar

def hello(x):

	#only for referece
	print("")

## initialisation of the camera
cap = cv2.VideoCapture(1)



camera = "http://192.168.43.1:8080/video"
cap = cv2.VideoCapture(0)
cap.open(camera)


bars = cv2.namedWindow("bars")

cv2.createTrackbar("upper_hue","bars",110,180,hello)
cv2.createTrackbar("upper_saturation","bars",255, 255, hello)
cv2.createTrackbar("upper_value","bars",255, 255, hello)
cv2.createTrackbar("lower_hue","bars",68,180, hello)
cv2.createTrackbar("lower_saturation","bars",55, 255, hello)
cv2.createTrackbar("lower_value","bars",54, 255, hello)

#Capturing the initial frame for creation of background
while(True):
	cv2.waitKey(2000)
	ret,init_frame = cap.read()
	init_frame = cv2.flip(init_frame, 1)
	init_frame = cv2.resize(init_frame, (600, 600))
	#check if the frame is returned then brake
	if(ret):
		break

# Start capturing the frames for actual magic!!
while(True):
	ret,frame = cap.read()

	frame = cv2.resize(frame, (600, 600))
	frame = cv2.flip(frame, 1)
	inspect = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#getting the HSV values for masking the cloak
	upper_hue = cv2.getTrackbarPos("upper_hue", "bars")
	upper_saturation = cv2.getTrackbarPos("upper_saturation", "bars")
	upper_value = cv2.getTrackbarPos("upper_value", "bars")
	lower_value = cv2.getTrackbarPos("lower_value","bars")
	lower_hue = cv2.getTrackbarPos("lower_hue","bars")
	lower_saturation = cv2.getTrackbarPos("lower_saturation","bars")

	#Kernel to be used for dilation
	kernel = numpy.ones((3,3),numpy.uint8)

	upper_hsv = numpy.array([upper_hue,upper_saturation,upper_value])
	lower_hsv = numpy.array([lower_hue,lower_saturation,lower_value])

# inRange function is containe only those range lower_hsv and upper_hsv and frame that means those selected color of thick in what color and other is black into converted.
	mask = cv2.inRange(inspect, lower_hsv, upper_hsv)
	# print(mask)
	mask = cv2.medianBlur(mask,3)
	mask_inv = 255-mask
	# mask_inv has done to mask of complements. if in mask selected color has selected color is white then mask_inv is selected color is black
	mask = cv2.dilate(mask,kernel,5)
	
	#The mixing of frames in a combination to achieve the required frame
	b = frame[:,:,0]
	g = frame[:,:,1]
	r = frame[:,:,2]
	b = cv2.bitwise_and(mask_inv, b)   # in mask_inv selected object fg is black and bg is white if selected object color is blue then  after performed operation of mask_inv then it is blue object fg is black and ohter color is white then all color is black r = black (0)
	g = cv2.bitwise_and(mask_inv, g)   #----> mask_inv selected object fg is black and bg is while --> only green color is sepreted
	r = cv2.bitwise_and(mask_inv, r)   # as same only red is sepreted in r
	frame_inv = cv2.merge((b,g,r))     # find we have merge so red, green color is also merge but blue color is not merge because we have already selected object is blue and after we have performed to mask to mask_inv so blue colro is converted to blue to black so finaly --> (mask_inv && frame[blue]) also  b = black

	b = init_frame[:,:,0]
	g = init_frame[:,:,1]
	r = init_frame[:,:,2]
	b = cv2.bitwise_and(b,mask)        # in mask selected object fg is white and bg is black if selected object color is blue then  after performed operation blue color is slected
	g = cv2.bitwise_and(g,mask)        # in mask selected object fg is white and bg is black if selected object color is green then  after performed operation blue color is slected
	r = cv2.bitwise_and(r,mask)
	blanket_area = cv2.merge((b,g,r))  # our selected object is blue so (b=1,g=0,r=o) after merge find area--> blue objects

	final = cv2.bitwise_or(frame_inv, blanket_area)

	cv2.imshow("Original",frame)
	cv2.imshow("Man Parts Remove",final)
	cv2.imshow("Set Your color object(mask)", mask)

	if(cv2.waitKey(3) == ord('q')):
		break;

cv2.destroyAllWindows()
cap.release()
