#!/usr/bin/env python

# ------------------------
#   IMPORTS
# ------------------------
from __future__ import print_function

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import roslib
roslib.load_manifest('carla_ros_image_converter')


class Image_Converter:
    """
    Class used for converting ROS images to OpenCV images
    """
    def __init__(self):
        self.image_pub = rospy.Publisher("/carla/ego_vehicle/camera/rgb/front/image_color_2", Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/carla/ego_vehicle/camera/rgb/front/image_color", Image, self.callback)

    def callback(self, data):
        cv_img = None
        try:
            cv_img = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

        (rows, cols, channels) = cv_img.shape
        if cols > 60 and rows > 60:
            cv.circle(cv_img, (50,50), 10, 255)

        cv.imshow("Image Window", cv_img)
        cv.waitKey(3)

        try:
            self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_img, "bgr8"))
        except CvBridgeError as e:
            print(e)


def main(args):
    img_converter = Image_Converter()
    rospy.init_node('image_converter', anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting Down!")
    cv.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)

