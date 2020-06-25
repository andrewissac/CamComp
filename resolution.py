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
        self.resolution = resolution
        self.height, self.width = Camera.CalcHeightWidth(self.resolution, self.aspectRatio)
        self.heightxwidth = str(self.height) + " x " + str(self.width)
        self.pixelDensity = Camera.CalcPixelDensity(self.resolution, self.sensorArea)

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
              str(self.height) + " x " + str(self.width) +
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
    return [camera.name, camera.resolution, camera.camtype.name, camera.heightxwidth, camera.pixelDensity, normalizedPixelDensity]

def GenerateCameraTabulate(cameras_, camToNormalizeWith):
    cams = []
    for cam in cameras_:
        cams.append(GenerateCameraTabulateEntry(cam, cameras_, camToNormalizeWith))
    return tabulate(cams, headers=["camera", "megapixel", "sensor type","height x width", "pixel/mm^2", "normalization"], tablefmt="github")

cameras = [Camera("6DII", CamType.FullFrame, 26.2),
           Camera("R6", CamType.FullFrame, 20.0),
           Camera("R5", CamType.FullFrame, 44.7),
           Camera("700D", CamType.APSC, 18.0),
           Camera("80D", CamType.APSC, 24.2),
           Camera("90D", CamType.APSC, 32.5)]

cameraToNormalizeWith = "700D"
camTable = GenerateCameraTabulate(cameras, cameraToNormalizeWith)


print("\n")
print("-------------------------------- Camera Comparison ---------------------------------- ")
print("--------------------- " + "used " + cameraToNormalizeWith + " to normalize pixel densities" + " ------------------------- ")
print("\n")
print(camTable)


