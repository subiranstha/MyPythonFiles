from PyQt5 import QtCore, QtGui, QtWidgets
import copy
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog
import cv2
from peronaMaliktest import PeronaMalik
from slicing_openAI_revised import slicing_main  # Slicing Function for the external contour
from contour_sort import sortAndAdjustContours   # Function that takes contours, sorts it and returns in a directed manner.
from minAndMaxIndexOfContours import topPoint, bottomPoint # Calculates the extreme points
from slicing5 import slicing_function
from arcFunc import convert_arc, draw_ellipse   # To draw the arc in the image
from function_lowestPoint import find_lowestPoint  # To find the lowest point in the image
from function_InternalColorFill import internalContourFill # This function fills the whole fusion zone area
from function_ExternalContourFill import externalContourFill # This function fills the while fusion zone and HAZ area.
import numpy as np

class getColorLabel(QtWidgets.QLabel):
    def __init__(self, widget, ui_main_window_obj):
        super().__init__(widget)
        self.main = widget
        self.ui_main_window_obj = ui_main_window_obj

    def mousePressEvent(self, event):
        print("Mouse Pressed: ")

        pixmap = self.pixmap()

        if pixmap is not None:

            x = event.pos().x()
            y = event.pos().y()
            print("Self.width", self.width(), " And self height", self.height())

        ui_obj = self.ui_main_window_obj
        ui_obj.pointColoredImage(x,y)
        # Please note that these c and y values need to be adjusted again
class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1668, 1037)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = getColorLabel(self.centralwidget, self)
        self.label.setGeometry(QtCore.QRect(40, 20, 500, 1000))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../img1.png"))
        self.label.setObjectName("label")
        self.label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.splitter_9 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_9.setGeometry(QtCore.QRect(750, 30, 451, 71))
        self.splitter_9.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_9.setObjectName("splitter_9")
        self.load = QtWidgets.QPushButton(self.splitter_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.load.setFont(font)
        self.load.setObjectName("load")
        self.rotate = QtWidgets.QPushButton(self.splitter_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.rotate.setFont(font)
        self.rotate.setObjectName("rotate")
        self.resize = QtWidgets.QPushButton(self.splitter_9)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.resize.setFont(font)
        self.resize.setObjectName("resize")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(750, 130, 451, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 421, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_for_iteration = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_for_iteration.setFont(font)
        self.label_for_iteration.setObjectName("label_for_iteration")
        self.gridLayout.addWidget(self.label_for_iteration, 0, 2, 1, 1)
        self.slider_for_kappa = QtWidgets.QSlider(self.layoutWidget)
        self.slider_for_kappa.setMinimum(0)
        self.slider_for_kappa.setMaximum(100)
        self.slider_for_kappa.setSingleStep(10)
        self.slider_for_kappa.setPageStep(10)
        self.slider_for_kappa.setProperty("value", 15)
        self.slider_for_kappa.setOrientation(QtCore.Qt.Horizontal)
        self.slider_for_kappa.setObjectName("slider_for_kappa")
        self.gridLayout.addWidget(self.slider_for_kappa, 2, 1, 1, 1)
        self.label_for_kappa = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_for_kappa.setFont(font)
        self.label_for_kappa.setObjectName("label_for_kappa")
        self.gridLayout.addWidget(self.label_for_kappa, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 4, 1, 1, 1)
        self.slider_for_iteration = QtWidgets.QSlider(self.layoutWidget)
        self.slider_for_iteration.setMinimum(0)
        self.slider_for_iteration.setMaximum(300)
        self.slider_for_iteration.setSingleStep(10)
        self.slider_for_iteration.setProperty("value", 70)
        self.slider_for_iteration.setOrientation(QtCore.Qt.Horizontal)
        self.slider_for_iteration.setObjectName("slider_for_iteration")
        self.gridLayout.addWidget(self.slider_for_iteration, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.slider_for_gamma = QtWidgets.QSlider(self.layoutWidget)
        self.slider_for_gamma.setMinimum(0)
        self.slider_for_gamma.setMaximum(150)
        self.slider_for_gamma.setSingleStep(5)
        self.slider_for_gamma.setPageStep(5)
        self.slider_for_gamma.setProperty("value", 20)
        self.slider_for_gamma.setOrientation(QtCore.Qt.Horizontal)
        self.slider_for_gamma.setObjectName("slider_for_gamma")
        self.gridLayout.addWidget(self.slider_for_gamma, 5, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 18, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 1, 1, 1)
        self.label_for_gamma = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_for_gamma.setFont(font)
        self.label_for_gamma.setObjectName("label_for_gamma")
        self.gridLayout.addWidget(self.label_for_gamma, 5, 2, 1, 1)
        self.sobel = QtWidgets.QPushButton(self.centralwidget)
        self.sobel.setGeometry(QtCore.QRect(750, 370, 451, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sobel.setFont(font)
        self.sobel.setObjectName("sobel")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(750, 480, 451, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.slicing1 = QtWidgets.QPushButton(self.groupBox_2)
        self.slicing1.setGeometry(QtCore.QRect(10, 30, 161, 51))
        self.slicing1.setObjectName("slicing1")
        self.contour_external = QtWidgets.QPushButton(self.groupBox_2)
        self.contour_external.setGeometry(QtCore.QRect(240, 30, 181, 51))
        self.contour_external.setObjectName("contour_external")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(750, 600, 451, 91))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.slicing2 = QtWidgets.QPushButton(self.groupBox_3)
        self.slicing2.setGeometry(QtCore.QRect(10, 30, 161, 51))
        self.slicing2.setObjectName("slicing2")
        self.contour_externalInternal = QtWidgets.QPushButton(self.groupBox_3)
        self.contour_externalInternal.setGeometry(QtCore.QRect(240, 30, 181, 51))
        self.contour_externalInternal.setObjectName("contour_externalInternal")
        self.interpolation = QtWidgets.QPushButton(self.centralwidget)
        self.interpolation.setGeometry(QtCore.QRect(750, 720, 451, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.interpolation.setFont(font)
        self.interpolation.setObjectName("interpolation")
        self.arc = QtWidgets.QPushButton(self.centralwidget)
        self.arc.setGeometry(QtCore.QRect(750, 890, 451, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.arc.setFont(font)
        self.arc.setObjectName("arc")
        self.default_PeronaMalik = QtWidgets.QPushButton(self.centralwidget)
        self.default_PeronaMalik.setGeometry(QtCore.QRect(1230, 210, 241, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.default_PeronaMalik.setFont(font)
        self.default_PeronaMalik.setObjectName("default_PeronaMalik")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(1250, 710, 381, 201))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.splitter_2 = QtWidgets.QSplitter(self.groupBox_4)
        self.splitter_2.setGeometry(QtCore.QRect(30, 30, 331, 151))
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.fill_internal = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fill_internal.setFont(font)
        self.fill_internal.setObjectName("fill_internal")
        self.fill_whole = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fill_whole.setFont(font)
        self.fill_whole.setObjectName("fill_whole")
        self.fill_separate = QtWidgets.QPushButton(self.splitter_2)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fill_separate.setFont(font)
        self.fill_separate.setObjectName("fill_separate")
        self.lowest_point = QtWidgets.QPushButton(self.centralwidget)
        self.lowest_point.setGeometry(QtCore.QRect(750, 820, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lowest_point.setFont(font)
        self.lowest_point.setObjectName("lowest_point")
        self.lowest_point2 = QtWidgets.QPushButton(self.centralwidget)
        self.lowest_point2.setGeometry(QtCore.QRect(970, 820, 191, 61))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lowest_point2.setFont(font)
        self.lowest_point2.setObjectName("lowest_point2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1668, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # All the connect buttons are written here:
        self.slider_for_iteration.valueChanged.connect(self.numChange_diffusion)
        self.slider_for_kappa.valueChanged.connect(self.numChange_diffusion)
        self.slider_for_gamma.valueChanged.connect(self.numChange_diffusion)
        self.default_PeronaMalik.clicked.connect(self.function_defaultPerona)

        # All the connect buttons are written here:
        self.load.clicked.connect(self.loadImage)
        self.resize.clicked.connect(self.resize_image)
        self.rotate.clicked.connect(self.rotate_image)
        self.sobel.clicked.connect(self.sobel_filter)

        # All connect buttons for the first slicing part:
        self.slicing1.clicked.connect(self.func_slicing1)
        self.contour_external.clicked.connect(self.func_contourDetection1)

        # All connect buttons for the second slicing part:
        self.slicing2.clicked.connect(self.func_slicing2)
        self.contour_externalInternal.clicked.connect(self.func_contourDetection2)
        self.lowest_point.clicked.connect(self.func_lowPoint)
        self.lowest_point2.clicked.connect(self.func_lowPoint2)

        # The connect button to draw the arc from the lowest point in the image
        #self.arc.clicked.connect(self.draw_arc)
        self.arc.clicked.connect(self.draw_arc)

        # The connect buttons for the filled internal and external contour:
        self.fill_internal.clicked.connect(self.func_fillInternalContour)
        self.fill_whole.clicked.connect(self.func_fillWholeContour)
        self.fill_separate.clicked.connect(self.func_fillAccordinngly)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # All the required variables are kept here:
        self.fileName = None  # Used to store the name of the file
        self.temp = None  # used to store the image before any processing

        self.imgForDiffusion = None  # Image before diffusion
        self.imgForSobel = None  # Image before Sobel
        self.imgForSlicing1 = None  # Image for first slicing, used for external or HAZ contour
        self.imgForContour1 = None  # Image for contour detection for external or HAZ contour
        self.imgForSlicing2 = None  # Image for second slicing
        self.imgForContour2 = None  # Image for second slicing

        self.imgForLower = None  # Image for detecting the lower point
        self.low_x = None
        self.low_y = None

        self.imgForUpper = None  # Image used for detecting the upper contour

        self.contours1 = None  # contours for HAZ

        self.contours2 = None  # contours for Fusion Zone

        self.copy1 = None  # Temporary images used for displaying purpose:
        self.copy2 = None  # To fill the internal contour only
        self.copy3 = None  # To fill the whole contour only because at last it is the difference

        # Filled Contours:
        self.filled_internal = None
        self.filled_whole = None

        # Coordinates of Two external contours:
        self.bottom_x_extL, self.bottom_y_extL = (None, None)
        self.bottom_x_extR, self.bottom_y_extR = (None, None)
        self.top_x_extL, self.top_y_extL = (None, None)
        self.top_x_extR, self.top_y_extR = (None, None)

        self.bottom_x_intL, self.bottom_y_intL = (None, None)
        self.bottom_x_intR, self.bottom_y_intR = (None, None)
        self.top_x_intL, self.top_y_intL = (None, None)
        self.top_x_intR, self.top_y_intR = (None, None)

        self.x_pos = None
        self.y_pos = None

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.load.setText(_translate("MainWindow", "1. Load"))
        self.rotate.setText(_translate("MainWindow", "2. Rotate"))
        self.resize.setText(_translate("MainWindow", "3. Resize"))
        self.groupBox.setTitle(_translate("MainWindow", "Step 4: Non Linear Diffusion Filter"))
        self.label_3.setText(_translate("MainWindow", "Kappa"))
        self.label_4.setText(_translate("MainWindow", "Gamma"))
        self.label_for_iteration.setText(_translate("MainWindow", "70"))
        self.label_for_kappa.setText(_translate("MainWindow", "20"))
        self.label_2.setText(_translate("MainWindow", "Iteration"))
        self.label_for_gamma.setText(_translate("MainWindow", "15"))
        self.sobel.setText(_translate("MainWindow", "Step 5: Sobel Filter"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Step 6: Slicing for External Contour"))
        self.slicing1.setText(_translate("MainWindow", "6 a. Slicing"))
        self.contour_external.setText(_translate("MainWindow", "6 b. Contour Detection"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Step 7: Slicing for Internal Contour"))
        self.slicing2.setText(_translate("MainWindow", "7 a. Slicing"))
        self.contour_externalInternal.setText(_translate("MainWindow", "7 b. Contour Detection"))
        self.interpolation.setText(_translate("MainWindow", "Step 8: Interpolation(Not Used for now)"))
        self.arc.setText(_translate("MainWindow", "Step 9: Draw Arc to join lower points"))
        self.default_PeronaMalik.setText(_translate("MainWindow", "Apply with default Parameters"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Step 10: Fill the Area of Zones"))
        self.fill_internal.setText(_translate("MainWindow", "10 a. Fill_InternalContours"))
        self.fill_whole.setText(_translate("MainWindow", "10 b. Fill_WholeContours"))
        self.fill_separate.setText(_translate("MainWindow", "10 c. Fill_Separately"))
        self.lowest_point.setText(_translate("MainWindow", "Lowest Point"))
        self.lowest_point2.setText(_translate("MainWindow", "If Not Found, TAP"))

    def numChange_diffusion(self):
        # This function notices the change in the Sliders which are the parameters of Perona Malik Filter and
        # if there is any change in the slider value then the Perona Malik filter is called.

        self.valueOfNumOfIteration = self.slider_for_iteration.value()  # The slider value of Num Of iteraion is extracted in this line of code
        self.label_for_iteration.setText(str(self.valueOfNumOfIteration))

        self.valueOfKappa = self.slider_for_kappa.value()  # The slider value for value of Kappa is extracted in this line of code
        self.label_for_kappa.setText(str(self.valueOfKappa))

        self.valueOfDelta = self.slider_for_gamma.value()  # The slider value for value of delta is extracted in this line of code.
        self.label_for_gamma.setText(str(self.valueOfDelta))

        self.valueOfDelta = self.valueOfDelta / 100  # Since the value of delta is between 0-1, thus the value of above delta is divided by 100
        self.function_peronaMalik(self.valueOfNumOfIteration, self.valueOfDelta, self.valueOfKappa)

    def loadImage(self):
        # This function is used to browse the file and select an image
        self.copy1 = None
        self.fileName = QFileDialog.getOpenFileName(filter="Image(*.*)")[
            0]  # the function to display all the files in the computer and then select a file
        self.image = cv2.imread(self.fileName)  # opencv function to read an image
        self.setPhoto(self.image, 0)  # self created function to display a image in the UI
        self.temp = copy.deepcopy(self.image)  # copy of an image for further processing
        print("Original Width = ", self.image.shape[1], "Original Height = ",
        self.image.shape[0])  # Just printing the original width and height of the image

    def setPhoto(self, image, flag=1):
        # This function displays any image in the UI. Also, one thing is that, if the width and height of image is larger then, width is fixed to 500 and height is fixed to 1000
        if (flag == 0):  # it means for the first time, just display according to the size of our displaying window
            height, width = image.shape[:2]
            if (width > 500 and height > 1000):  # Just checking if the image is too large to display or not
                # and if its too large then changing its size so that it fits the display window of ours
                image = cv2.resize(image, (500, 1000))
            elif (width > 500 and height < 1000):
                image = cv2.resize(image, (500, height))
            elif (width < 500 and height > 1000):
                image = cv2.resize(image, (width, 1000))
            else:
                image = image
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0],
                       QImage.Format_RGB888)  # necessary conversion of the image to dispaly in the screen
        self.label.setPixmap(QtGui.QPixmap.fromImage(
            image))  # The image in PyQT is displayed using the label, hence we are changing the label to a new image

    def resize_image(self):
        # The original Image is in self.temp. Now manipulate the self.temp according to the desired shape
        width = 500  # The width is fixed to 500
        org_h, org_w = self.temp.shape[:2]  # Original height and width of the image
        ratio = width / float(org_w)  # calculating the original aspect ratio
        new_height = int(org_h * ratio)  # Calculating the new height according to the aspect ratio and fixed widths
        if (org_h> 1000):  # Adjusting the new height to 1000, if the height is greater than 1000
            new_height = 1000
        else:
            if(new_height>1000):
                new_height = 1000
        dim = (width, new_height)  # The new dimension
        print("Resized Width = ", width, "Resized Height = ", new_height)
        resized_image = cv2.resize(self.temp, dim, interpolation=cv2.INTER_AREA)  # Resizing the Image
        self.temp = copy.deepcopy(resized_image)
        self.setPhoto(resized_image, 1)

    def rotate_image(self):  # This function rotates an image by 90 degrees
        image = copy.deepcopy(self.temp)  # because the latest image is in self.temps
        out = cv2.transpose(
            image)  # 90 degree of rotation is acheived by doing the transpose of an image followed by fliiping the image horizontally
        out = cv2.flip(out, flipCode=0)
        self.temp = copy.deepcopy(out)  # Temp holds the rotated image which can be further rotate or blurred
        self.setPhoto(out, 0)  # Displaying the flipped image

    def function_peronaMalik(self, value1, value2, value3):  # This function is used to apply the Perona Malik filter in an image
        print("Num of Iteration = ", value1, "Value of Kappa = ", value3, "Value of Delta = ", value2)
        self.imgForLower = copy.deepcopy(self.temp)  # image to find the lower point
        self.imgForUpper = copy.deepcopy(self.temp)  # the image to find the upper contour

        imgForDiffusion = copy.deepcopy(self.temp)
        imgForDiffusion = cv2.cvtColor(imgForDiffusion,
                                       cv2.COLOR_BGR2GRAY)  # Perona Malik filter only works for gray scale image
        imgForDiffusion = imgForDiffusion.astype(
            'float64')  # Before applying the Perona Malik filter, the format should be in float64, so as there is no any overflow value

        # Now Applying the Perona Malik Filter

        u = PeronaMalik(imgForDiffusion, value1, value2, value3)
        u = cv2.convertScaleAbs(u)


        # As the next step after the Perona Malik filter is Sobel, so initiating the image of Sobel step with the output of perona malik filter
        self.imgForSobel = copy.deepcopy(u)
        # u is here a grayscale image
        self.setPhoto(u, 1)

    def function_defaultPerona(self):  # If we dont want to use the slider for Perona Malik filter, then this function is called with the default value of the parameters that had worked best in the availabe image dataset.
        self.function_peronaMalik(60, 0.15, 20)

    def sobel_filter(self):  # This function is used to apply the Sobel filter in x direction. Since our desired eges is in X-Direction.
        Ix = cv2.Sobel(self.imgForSobel, cv2.CV_64F, dx=1, dy=0, ksize=3)  # dx = and dy =0 means the filter is applied in the x direction
        Ix = cv2.convertScaleAbs(Ix)

        Ix[Ix <= 5] = 0  # The output of filter is in the range of 0-255 and not so visible, thus we are making it a binary image which have the value of 0 or 255
        Ix[Ix > 5] = 255

        self.imgForSlicing1 = copy.deepcopy(Ix)
        self.imgForSlicing2 = copy.deepcopy(Ix)
        cv2.imwrite("C:\\Users\\Subiran\\Desktop\\Image111.jpg", Ix)

        self.setPhoto(Ix, 1)

    def func_slicing1(self):
        # This function is used to apply the slicing to detect the Heat Affected Zone or external contour.
        # Since, our edge from the above step is quite high, thus we require slicing operation to thin the edge in our image
        sliced_img1 = slicing_main(self.imgForSlicing1)
        dilated = cv2.dilate(sliced_img1, None,iterations=2)  # After the slicing, now the edge is not continuous at some point, thus to make the edge more continuous the dilation and erodition operation is performed in the image.
        eroded = cv2.erode(dilated, None, iterations=2)
        self.imgForContour1 = copy.deepcopy(eroded)
        self.setPhoto(eroded, 1)


        #kernel = np.ones((4,4), np.uint8)
        #thick_edges = cv2.dilate(sliced_img1, kernel, iterations=1)
        #self.imgForContour1 = copy.deepcopy(thick_edges)
        #self.setPhoto(thick_edges, 1)

    def func_contourDetection1(self):
        # After the thinning of edge of HAZ, the next operation is to detect the contour and this contour detection of HAZ is performed in this function.
        self.copy1 = copy.deepcopy(self.temp)
        self.contours1, hierarchy = cv2.findContours(self.imgForContour1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contours1 = sortAndAdjustContours(
            self.contours1)  # After detecting contours, there are many contours, thus we are finding two contours with largest length in this line of code.
        cv2.drawContours(self.copy1, self.contours1, 0, (0, 0, 255),
                         2)  # After finding the contour, now we are drawing the contour in the image and then displaying
        cv2.drawContours(self.copy1, self.contours1, 1, (0, 0, 255), 2)

        # Finding the extreme points of HAZ as well.

        self.top_x_extL, self.top_y_extL = topPoint(self.contours1,
                                                    0)  # NOt only this we are also finding the extreme points in the contour.
        self.top_x_extR, self.top_y_extR = topPoint(self.contours1, 1)

        self.bottom_x_extL, self.bottom_y_extL = bottomPoint(self.contours1, 0)
        self.bottom_x_extR, self.bottom_y_extR = bottomPoint(self.contours1, 1)
        self.drawTopAndBottomPoints(self.copy1, 1)

        self.setPhoto(self.copy1, 1)

    def func_slicing2(self):
        # In this function, we are performing the slicing operation for getting the sliced edge for Fusion Zone
        # The concept of "The end of HAZ is the start of fusion zone" is applied here.
        sliced_img2 = slicing_function(self.imgForSlicing2)
        dilated = cv2.dilate(sliced_img2, None,
                             iterations=2)  # After slicing the dilation and erodition is performed to make the edgde more continuous.
        eroded = cv2.erode(dilated, None, iterations=2)
        self.imgForContour2 = copy.deepcopy(eroded)

        self.setPhoto(eroded, 1)

    def func_contourDetection2(self):
        # After slicing 2, now the contour for that sliced_region is detected.
        contours, hierarchy = cv2.findContours(self.imgForContour2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for i in range(len(contours)):
            for j in range(len(contours[i])):
                x, y = contours[i][j][0][0], contours[i][j][0][0]
                if (x < 220):
                    contours[i][j][0][0] += 13
                elif (x > 250):
                    contours[i][j][0][0] -= 13  # It means shifting the HAZ by 13 as we know the end of HAZ is the start of FZ

        self.contours2 = sortAndAdjustContours(contours)
        cv2.drawContours(self.copy1, self.contours2, 0, (0, 0, 255), 2)  # for the left one
        cv2.drawContours(self.copy1, self.contours2, 1, (0, 0, 255), 2)  # drwaing the right Fusion zone contour in the image and then displaying

        # Finding th extreme points of Fusion zone now

        self.top_x_intL, self.top_y_intL = topPoint(self.contours2, 0)
        self.top_x_intR, self.top_y_intR = topPoint(self.contours2, 1)
        self.bottom_x_intL, self.bottom_y_intL = bottomPoint(self.contours2, 0)
        self.bottom_x_intR, self.bottom_y_intR = bottomPoint(self.contours2,
                                                             1)  # Finding the extreme points of the contours of Fusion zone
        self.drawTopAndBottomPoints(self.copy1, 0)

        self.setPhoto(self.copy1, 1)

    def func_lowPoint(self):
        self.low_x, self.low_y = find_lowestPoint(self.imgForLower)  # finding the lowest point in the image, so that two points are connected via that point.
        if(self.low_x==0 and self.low_y==0):
            print("Lowest Point not found and thus choose manually")
        else:
            copyn = copy.deepcopy(self.copy1)
            copyn = cv2.circle(copyn, (self.low_x, self.low_y), radius=5, color=(0, 255, 0), thickness=-1)  # drawing that lowest point in the image
            self.setPhoto(copyn, 1)

    def func_lowPoint2(self):
        self.low_x, self.low_y = self.x_pos, self.y_pos  # finding the lowest point in the image, so that two points are connected via that point.




    def draw_arc(self):
        # Since the contours of HAZ and FZ is not complete in the lowest point in the image, thus we have to to draw the arc to make them complete and this function does exactly that.
        print("Lowest Points", self.low_x, self.low_y)

        if (self.low_x == 0 and self.low_y == 0):  # means that we couldnot find the lowest point in the image and thus we have to sue another approach to find the third.
            # The reason we need three points is that, in a  circle there are three parameter, center(h,k) and radius and thus we need at least three points.
            center_ext, radius_ext, start_angle_ext, end_angle_ext = convert_arc(
                (self.bottom_x_extL, self.bottom_y_extL), (self.bottom_x_extR, self.bottom_y_extR), (None, None), 70)
        else:
            center_ext, radius_ext, start_angle_ext, end_angle_ext = convert_arc(
                (self.bottom_x_extL, self.bottom_y_extL), (self.bottom_x_extR, self.bottom_y_extR),
                (self.low_x, self.low_y), None)

        center_int, radius_int, start_angle_int, end_angle_int = convert_arc((self.bottom_x_intL, self.bottom_y_intL),
                                                                             (self.bottom_x_intR, self.bottom_y_intR),
                                                                             (self.low_x, self.low_y), None)

        axes_ext = (radius_ext, radius_ext)
        draw_ellipse(self.copy1, center_ext, axes_ext, 0, start_angle_ext, end_angle_ext, (0, 75, 150))

        axes_int = (radius_int, radius_int)
        draw_ellipse(self.copy1, center_int, axes_int, 0, start_angle_int, end_angle_int,
                     (0, 75, 150))  # After finding all the parameters, now are are drawing the arc in the image.

        self.setPhoto(self.copy1, 1)

    def func_fillInternalContour(self):
        self.copy2 = copy.deepcopy(self.temp)  # Filling the while Fusion zone area in this image.
        self.fill_internal = internalContourFill(self.temp,
                                                 self.contours2)  # This function returns the whole combined contour for the fusion zone and if we have a single contour that represents the whole area the  it is quite easy to fill.
        cv2.fillPoly(self.copy2, pts=[self.fill_internal], color=(0, 255,
                                                                  0))  # The whole area in the contour "self.fill_internal" is filled with green colour using this function.
        self.setPhoto(self.copy2, 1)

    def func_fillWholeContour(self):
        self.copy3 = copy.deepcopy(self.temp)
        self.fill_external = externalContourFill(self.temp,
                                                 self.contours1)  # Finding the whole single contour for the overall area part in the image.
        cv2.fillPoly(self.copy3, pts=[self.fill_external],
                     color=(0, 0, 255))  # Filling the whole area part with red colour.
        self.setPhoto(self.copy3, 1)

        # In self.copy2, we have the filled internal contour and in self.copy3 we have filled the whole contour:
        # In self.fill_external we have a big contour for the external one and in self.fill_internal we have a big whhole contour for the internal one

    def func_fillAccordinngly(self):
        self.copy4 = copy.deepcopy(self.temp)
        cv2.fillPoly(self.copy4, pts=[self.fill_external],
                     color=(0, 0, 255))  # At first filling the whole area with red region for HAZ+ FZ.
        cv2.fillPoly(self.copy4, pts=[self.fill_internal], color=(0, 255, 0))  # Then filling the FZ with green colour.

        self.setPhoto(self.copy4, 1)
        cv2.imwrite("SeparateFilled.jpg", self.copy4)

    def drawTopAndBottomPoints(self, image, flag):
        if (flag == 0):  # means draw for internal contours:
            image = cv2.circle(image, (self.top_x_intL, self.top_y_intL), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.top_x_intR, self.top_y_intR), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.bottom_x_intL, self.bottom_y_intL), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.bottom_x_intR, self.bottom_y_intR), radius=4, color=(0, 255, 0),
                               thickness=-1)
        else:  # draw for external contour
            image = cv2.circle(image, (self.top_x_extL, self.top_y_extL), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.top_x_extR, self.top_y_extR), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.bottom_x_extL, self.bottom_y_extL), radius=4, color=(0, 255, 0),
                               thickness=-1)
            image = cv2.circle(image, (self.bottom_x_extR, self.bottom_y_extR), radius=4, color=(0, 255, 0),
                               thickness=-1)

    def pointColoredImage(self, x, y):
        print("Hello")
        self.x_pos = x
        self.y_pos = y
        copyn = copy.deepcopy(self.temp)
        print(x, y)
        copyn = cv2.circle(copyn, (x, y), radius=5, color=(0, 255, 0), thickness=-1)
        self.setPhoto(copyn, 1)

    def draw_circle(self):
        p1 = (self.bottom_x_extL, self.bottom_y_extL)
        p2 = (self.bottom_x_extR, self.bottom_y_extR)
        p3 = (self.low_x, self.low_y)

        # calculate the perpendicular bisectors of the sides
        mid1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
        mid2 = ((p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2)
        m1 = (p2[0] - p1[0]) / (p1[1] - p2[1])
        m2 = (p3[0] - p2[0]) / (p2[1] - p3[1])
        x = (m1 * mid1[0] - m2 * mid2[0] + mid2[1] - mid1[1]) / (m1 - m2)
        y = (-1 / m1) * (x - mid1[0]) + mid1[1]


        # calculate the radius of the circle
        r = int(np.sqrt((p1[0] - x) ** 2 + (p1[1] - y) ** 2))
        # calculate the angles of the arc
        theta1 = np.arctan2(p1[1] - y, p1[0] - x)
        theta2 = np.arctan2(p3[1] - y, p3[0] - x)

        # draw the arc on the image
        cv2.ellipse(self.copy1, (int(x), int(y)), (r, r), 0, theta1 * 180 / np.pi, theta2 * 180 / np.pi, (0, 255, 0), 2)
        self.setPhoto(self.copy1, 1)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
