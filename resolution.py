import math
import enum
from tabulate import tabulate

class CamType(enum.Enum):
    APSC = 1
    FullFrame = 2

class Camera:
    # class variables
    aspectRatio = 3 / 2
    fullFrameArea = 24 * 36  # mm
    apscArea = 22.2 * 14.8  # mm

    def __init__(self, name, camtype, resolution):
        self.name = name
        self.camtype = camtype
        self.sensorArea = Camera.fullFrameArea if self.camtype is CamType.FullFrame else Camera.apscArea
        self.resolution = resolution # MEGAPIXEL
        self.height, self.width = Camera.CalcHeightWidth(self.resolution, self.aspectRatio)
        self.widthxheight = str(self.width) + " x " + str(self.height)
        self.pixelDensity = Camera.CalcPixelDensity(self.resolution, self.sensorArea)

    def __str__(self):
        return str(self.name) + " - " + str(self.camtype) + " - sensor area mm^2: " + str(self.sensorArea) + \
               " - resolution in MP: " + str(self.resolution) + \
               " - " + str(self.widthxheight) + " - pixel density: " + str(self.pixelDensity)

    @staticmethod
    def CalcHeightWidth(Resolution, aspectRatio):
        x = math.sqrt(Resolution/aspectRatio)
        height = math.floor(x * 1000)
        width = math.floor(aspectRatio * x * 1000)
        return height, width

    @staticmethod
    def CalcPixelDensity(Resolution, Area):
        return math.floor(Resolution * 1000000 /Area)

    def PrintProperties(self, pixelDensityToNormalizeWith = None):
        if pixelDensityToNormalizeWith is None:
            pixelDensityToNormalizeWith = self. pixelDensity

        print(str(self.name) + " - resolution: " + str(self.resolution) + " MP: " +
              str(self.width) + " x " + str(self.height) +
              " with the pixel density of: " + str(self.pixelDensity) + " px/mm^2 which corresponds to " +
              str(round(self.pixelDensity / pixelDensityToNormalizeWith * 100, 2)) + " %")


def GetCameraObjectByName(cams, name):
    for cam in cams:
        if cam.name is name:
            return cam

def GenerateCameraTabulateEntry(camera, cameras_, camToNormalizeWith = None):
    camToNormalizeWith = GetCameraObjectByName(cameras_, camToNormalizeWith)
    if camToNormalizeWith is None:
        camToNormalizeWith = camera
    normalizedPixelDensity = str(round(camera.pixelDensity / camToNormalizeWith.pixelDensity * 100, 2)) + " %"
    return [camera.name, camera.resolution, camera.camtype.name, camera.widthxheight, camera.pixelDensity, normalizedPixelDensity]

def GenerateCameraTabulate(cameras_, camToNormalizeWith):
    cams = []
    for cam in cameras_:
        cams.append(GenerateCameraTabulateEntry(cam, cameras_, camToNormalizeWith))
    cams = sorted(cams, key=lambda x: float(x[5].strip(" %")))
    return tabulate(cams, headers=["camera", "megapixel", "sensor type","width x height", "pixel/mm^2", "normalization"], tablefmt="github")

def SortCamerasByPixelDensity(cams):
    return sorted(cams, key=lambda cam: cam.pixelDensity)

def GetFullframeCams(cams):
    return SortCamerasByPixelDensity([x for x in cams if x.camtype is CamType.FullFrame])

cameras = [Camera("6DII", CamType.FullFrame, 26.2),
           Camera("R6", CamType.FullFrame, 20.0),
           Camera("R5", CamType.FullFrame, 44.7),
           Camera("R",CamType.FullFrame, 30.1),
           Camera("700D", CamType.APSC, 18.0),
           Camera("TEST", CamType.FullFrame, 18.0),
           Camera("80D", CamType.APSC, 24.2),
           Camera("90D", CamType.APSC, 32.5),
           Camera("SonyA9", CamType.FullFrame, 24),
           Camera("Sony6100",CamType.APSC, 24)]

cameras = SortCamerasByPixelDensity(cameras)

cameraToNormalizeWith = "R6"
camTable = GenerateCameraTabulate(cameras, cameraToNormalizeWith)


print("\n")
print("-------------------------------- Camera Comparison ---------------------------------- ")
print("--------------------- " + "used " + cameraToNormalizeWith + " to normalize pixel densities" + " ------------------------- ")
print("\n")
print(camTable)

class Rectangle:
    def __init__(self, center, WidthxHeight):
        self.center = center
        self.centerX = center[0]
        self.centerY = center[1]
        self.width = WidthxHeight[0]
        self.height = WidthxHeight[1]
        self.widthxheight = WidthxHeight
        self.Topleft = (self.centerX - self.width/2, self.centerY - self.height/2)
        self.BottomRight = (self.centerX + self.width/2, self.centerY + self.height/2)

    def __str__(self):
        return "Center: " + str(self.center) + " - Width x Height: " + str(self.widthxheight) + \
               " - Top left: " + str(self.Topleft) + " - Bottom right: " + str(self.BottomRight)

from tkinter import *

window = Tk()

WindowWidth = 750
WindowHeight = 500
WindowSize= str(WindowWidth) + "x" + str(WindowHeight)
WindowCenter = (WindowWidth/2, WindowHeight/2)
BiggestRect = Rectangle(WindowCenter, (WindowWidth*0.8, WindowHeight*0.8))

#ffCams = GetFullframeCams(cameras)
ffCams = [cameras[1], cameras[3],cameras[5]]
ffCamTable = GenerateCameraTabulate(ffCams, cameraToNormalizeWith)
print(ffCamTable)


def CalcRectanglesFromCameras(NormalizationRectangle, cams):
    highestResolutionCam = max(cams, key=lambda cam: cam.pixelDensity)
    NormalizationFactor = 1 / (highestResolutionCam.width / NormalizationRectangle.width)
    return [Rectangle(NormalizationRectangle.center,(math.floor(cam.width * NormalizationFactor), math.floor(cam.height * NormalizationFactor))) for cam in cams]

import random

def generate_color():
    color = '#{:02x}{:02x}{:02x}'.format(*map(lambda x: random.randint(0, 255), range(3)))
    return color


rectangles = CalcRectanglesFromCameras(BiggestRect, ffCams)
for rect in rectangles:
    print(rect)


window.geometry(WindowSize)

canvas = Canvas(window)

from matplotlib import colors as pltcolors

matplotlibcolors = list(pltcolors.cnames.values())

index = 22

for rectangle in reversed(rectangles):
    color = matplotlibcolors[index]
    index += 15
    canvas.create_rectangle(rectangle.Topleft, rectangle.BottomRight, outline=color, fill=color)


canvas.pack(fill=BOTH, expand=1)

window.mainloop()

