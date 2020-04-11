
from PIL import Image
import numpy as np

SIMILARITY=0.05
ADD_SIMILARITY_TOLERENCE=0.04
#ADD_SIMILARITY_TOLERENCE=0.01
CYCLE_TOLERENCE=0.0045
SUBTRACTTOLERENCE=0.02
BLACK_PIXEL_COUNT_TOLERENCE=0.005
XOR2_TOLERENCE=0.022

def xor(image1,image2,image3):
    image1=ImagetoArray(image1)
    image2=ImagetoArray(image2)
    image3=ImagetoArray(image3)
    #the assumption all are same dimension holds
    xor=np.zeros((image1.shape[0],image1.shape[1]),dtype=int)
    for l in range (image1.shape[0]):
        for b in range (image1.shape[1]):

            if image1[l][b]==image2[l][b]==image3[l][b]==1 or image1[l][b]==image2[l][b]==image3[l][b]==0:
                xor[l][b]=1
            else:
                xor[l][b]=0
    return xor

def SUM(image1,image2):
    image1 = ImagetoArray(image1)
    image2 = ImagetoArray(image2)

    # the assumption all are same dimension holds
    #sum = np.zeros((image1.shape[0], image1.shape[1]), dtype=int)
    sum=np.logical_and(image1,image2)
    return sum


def DIFFERENCE(image1,image2):
    image1 = ImagetoArray(image1)
    image2 = ImagetoArray(image2)

    # the assumption all are same dimension holds
    difference = np.zeros((image1.shape[0], image1.shape[1]), dtype=int)
    for l in range(image1.shape[0]):
        for b in range(image1.shape[1]):

            if image1[l][b] == 0 and  image2[l][b] == 1 or image1[l][b] == 1 and  image2[l][b] == 0:
                difference[l][b] = 1

            else:
                difference[l][b] = 0
    return difference


def black_pixel_count_differnce(image1,image2,image3):
    blace_pixelsA = black_pixel_count_of_image(image1)
    black_pixelsD = black_pixel_count_of_image(image2)
    black_pixelsG = black_pixel_count_of_image(image3)
    tolerence = ((abs(blace_pixelsA - (black_pixelsG + black_pixelsD))) / (
                ImagetoArray(image1).shape[0] * ImagetoArray(image1).shape[1]))
    return tolerence

def black_pixel_count_of_image(image):
    return (ImagetoArray(image).shape[0] * ImagetoArray(image).shape[1]) - int(
        np.sum(ImagetoArray(image)))
def pixelhelper(row1,row2,row3,answeroptions):
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    tolerence1 = black_pixel_count_differnce(row1[0], row1[1], row1[2])
    tolerence2 = black_pixel_count_differnce(row2[0], row2[1], row2[2])
    if tolerence1 < BLACK_PIXEL_COUNT_TOLERENCE and tolerence2 < BLACK_PIXEL_COUNT_TOLERENCE:
        print("we have found a pixel match A=B+C")
        for key, value in answeroptions.items():
            confidencerating[key] += black_pixel_count_differnce(row3[0], row3[1], value)
            existsalreadyG = arrayidentical(ImagetoArray(row3[0]), ImagetoArray(value))
            existsalreadyH = arrayidentical(ImagetoArray(row3[1]), ImagetoArray(value))
            if existsalreadyG < 0.02 or existsalreadyH < 0.02:
                confidencerating[key] += 100
    return confidencerating

def PixelSumCheckRow(row1,row2,row3,answeroptions):
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    #Pixels(A)=Pixels(B) +Pixels(C)
    confidencerating=Add_condifence_ratings(confidencerating,pixelhelper(row1,row2,row3,answeroptions))
    row1new=[row1[1],row1[0],row1[2]]
    row2new = [row2[1], row2[0], row2[2]]
    return confidencerating

def ROWXOR(image1,image2,checkimage1,image3,image4,checkimage2,image5,image6,answeroptions):
    BxorC = xor2(image1, image2)
    BxorCequalsA = arrayidentical(BxorC, ImagetoArray(checkimage1))
    ExorF = xor2(image3, image4)
    ExorFequalsD = arrayidentical(ExorF, ImagetoArray(checkimage2))
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    if BxorCequalsA < XOR2_TOLERENCE and ExorFequalsD < XOR2_TOLERENCE:
        print(" A = B xor C detected")
        for key, value in answeroptions.items():
            HxorOption = xor2(image5, value)
            HxorOptionequalsG = arrayidentical(HxorOption, ImagetoArray(image6))
            confidencerating[key] += HxorOptionequalsG
    # B= A xor C

    # C= B xor A
    return confidencerating

def ROWSUM(image1,image2,checkimage1,image3,image4,checkimage2,image5,image6,answeroptions):
    BxorC = SUM(image1, image2)
    BxorCequalsA = arrayidentical(BxorC, ImagetoArray(checkimage1))
    ExorF = SUM(image3, image4)
    ExorFequalsD = arrayidentical(ExorF, ImagetoArray(checkimage2))
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    if BxorCequalsA < ADD_SIMILARITY_TOLERENCE and ExorFequalsD < ADD_SIMILARITY_TOLERENCE:
        print(" A = B + C detected")
        for key, value in answeroptions.items():
            HxorOption = SUM(image5, value)
            HxorOptionequalsG = arrayidentical(HxorOption, ImagetoArray(image6))
            confidencerating[key] += HxorOptionequalsG
    return confidencerating

def PerformROWSUM(row1,row2,row3,answeroptions):
    # A= B + C
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    confidencerating1 = ROWSUM(row1[1], row1[2], row1[0], row2[1], row2[2], row2[0], row3[1], row3[0], answeroptions)
    confidencerating = Add_condifence_ratings(confidencerating, confidencerating1);
    return confidencerating

    # B=A xor C
    confidencerating1 = ROWSUM(row1[0], row1[2], row1[1], row2[0], row2[2], row2[1], row3[1], row3[0], answeroptions)
    confidencerating = Add_condifence_ratings(confidencerating, confidencerating1);
    return confidencerating
    # A xor B = C
    AxorB = SUM(row1[0], row1[1])
    AxorBequalsC = arrayidentical(AxorB, ImagetoArray(row1[2]))

    DxorE = SUM(row2[0], row2[1])

    DxorEequalsF = arrayidentical(DxorE, ImagetoArray(row2[2]))

    confidencerating1 = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    if AxorBequalsC < ADD_SIMILARITY_TOLERENCE and DxorEequalsF < ADD_SIMILARITY_TOLERENCE:
        print(" C = A xor B detected")
        GxorH = SUM(row3[0], row3[1])
        for key, value in answeroptions.items():
            GxorHequalsoption = arrayidentical(GxorH, ImagetoArray(value))
            confidencerating1[key] += GxorHequalsoption
    confidencerating = Add_condifence_ratings(confidencerating, confidencerating1);
    return confidencerating

def PerformROWXORS(row1,row2,row3,answeroptions):
    #A= B xor C
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    confidencerating1=ROWXOR(row1[1],row1[2],row1[0],row2[1],row2[2],row2[0],row3[1],row3[0],answeroptions)
    if confidencerating1!=confidencerating:
       confidencerating=Add_condifence_ratings(confidencerating,confidencerating1);
       return confidencerating

    #B=A xor C
    confidencerating1 = ROWXOR(row1[0], row1[2], row1[1], row2[0], row2[2], row2[1], row3[1], row3[0], answeroptions)
    if confidencerating1 != confidencerating:
        confidencerating = Add_condifence_ratings(confidencerating, confidencerating1);
        return confidencerating
    #A xor B = C
    AxorB = xor2(row1[0], row1[1])
    AxorBequalsC = arrayidentical(AxorB, ImagetoArray(row1[2]))

    DxorE = xor2(row2[0], row2[1])


    DxorEequalsF = arrayidentical(DxorE, ImagetoArray(row2[2]))


    confidencerating1 = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    if AxorBequalsC < XOR2_TOLERENCE and DxorEequalsF < XOR2_TOLERENCE:
        print(" C = A xor B detected")
        GxorH = xor2(row3[0], row3[1])
        for key, value in answeroptions.items():
            GxorHequalsoption = arrayidentical(GxorH, ImagetoArray(value))
            confidencerating1[key] += GxorHequalsoption
        confidencerating = Add_condifence_ratings(confidencerating, confidencerating1);

        return confidencerating
    #3-way XOR
    row1xor = xor(row1[0], row1[1], row1[2])
    row2xor = xor(row2[0], row2[1], row2[2])
    print("at XOR")
    if identical(row1xor, row2xor) < SIMILARITY:
        print("XOR detected")
        optionxorarray = {}
        for key, value in answeroptions.items():
            rowoptionxor = xor(row3[0], row3[1], value)
            optionxorarray[key] = rowoptionxor
        similarityarray = similarityindex(row1xor, optionxorarray)
        for key, value in similarityarray.items():
            confidencerating[str(key)] += value
    print("after row xors",confidencerating)
    return confidencerating



def Add_condifence_ratings(conf1, conf2):
    for key in conf1:
      conf1[key] = conf1[key] + conf2[key]
    return conf1


def xor2(image1,image2):
    image1 = ImagetoArray(image1)
    image2 = ImagetoArray(image2)

    # the assumption all are same dimension holds
    xor = np.zeros((image1.shape[0], image1.shape[1]), dtype=int)
    for l in range(image1.shape[0]):
        for b in range(image1.shape[1]):

            if  ((image1[l][b] == 1 and  image2[l][b] == 1) or(image1[l][b] == 0 and  image2[l][b] == 0) ):
                xor[l][b] = 1

            else:
                xor[l][b] = 0

    return xor

def similarityindex1(image,answeroptions):
    simindex={}
    for key, value in answeroptions.items():
        simindex[int(key)] = arrayidentical(image, ImagetoArray(value))
    return simindex
def arrayidentical(array1,array2):
    length = array1.shape[0]
    breadth = array1.shape[1]
    # check the difference
    difference = np.zeros((length, breadth), dtype=float)
    for l in range(length):
        for b in range(breadth):
            # overflow detected; using floats
            difference[l][b] = abs(float(array1[l][b]) - float(array2[l][b]))

    meandifference = np.mean(difference)

    # does not work; will need to traverse individually
    # averagedifference=np.mean(np.abs(image1binary - image2binary))

    return meandifference

def identical(image1, image2):


    #This method currently considers images with identical dimesnsions
    #TODO: convert images down to similar dimesnions and compare.
    #converting images to arrays
    #
    image1array=ImagetoArray(image1);
    image2array=ImagetoArray(image2);

    #comparison = image1binary == image2binary
    #equal_arrays = comparison.all()
    length=image1array.shape[0]
    breadth=image1array.shape[1]
    #check the difference
    difference=np.zeros((length,breadth),dtype=float)
    for l in range(length):
        for b in range(breadth):
            #overflow detected; using floats
            difference[l][b]= abs(float(image1array[l][b])-float(image2array[l][b]))

    meandifference=np.mean(difference)

    #does not work; will need to traverse individually
    #averagedifference=np.mean(np.abs(image1binary - image2binary))


    return meandifference

def ImagetoArray(image):

    imagearray = np.array(image)
    for l in range(imagearray.shape[0]):
        for b in range(imagearray.shape[1]):
            imagearray[l][b]/= 255

    return imagearray

def createdictionaries(problem):
    figures={}
    answeroptions={}

    for name,figure in problem.figures.items():
        image = Image.open(figure.visualFilename).convert("L")
        if name.isdigit():
            answeroptions[name] = image
        else:
           figures[name]=image
    return figures, answeroptions

