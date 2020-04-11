from PIL import Image
import numpy as np
from ImageHelper import *
BLACK_PIXEL_COUNT_TOLERENCE=0.015
ROTATION_ERROR=0.009
figures={}
answeroptions={}
def SolveChallenge(figures, answeroptions):
    print("at E challenge")
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    #Challenge D-02 rotation
    #A-180*-B-180*-C
    check=degree90([figures['A'], figures['B'], figures['C']], [figures['D'], figures['E'], figures['F']], [figures['G'], figures['H']], answeroptions)
    confidencerating=Add_condifence_ratings(confidencerating,check)
    check=degree45([figures['A'], figures['B'], figures['C']], [figures['D'], figures['E'], figures['F']], [figures['G'], figures['H']], answeroptions)
    confidencerating = Add_condifence_ratings(confidencerating, check)
    pixelcheck([figures['A'], figures['B'], figures['C']], [figures['D'], figures['E'], figures['F']], [figures['G'], figures['H']], answeroptions)
    halfandhalf([figures['D'], figures['E'], figures['H']])
    return confidencerating

def degree90(triplet1, triplet2, triplet3, answeroptions):
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    # Challenge D-02 rotation
    # A-180*-B-180*-C
    ARotated = np.rot90(ImagetoArray(triplet1[0]),3)
    AsimilartoB = arrayidentical(ImagetoArray(triplet1[1]), ARotated)
    BsimilartoC=(arrayidentical(np.rot90(ImagetoArray(triplet1[1]),3), ImagetoArray(triplet1[2])))
    if AsimilartoB < ROTATION_ERROR and BsimilartoC < ROTATION_ERROR:

        DRotated = np.rot90(ImagetoArray(triplet2[0]),3)
        DsimilartoE = arrayidentical(ImagetoArray(triplet2[1]), DRotated)
        EsimilartoF=(arrayidentical(np.rot90(ImagetoArray(triplet2[0]),3), ImagetoArray(triplet2[1])))
        if DsimilartoE<ROTATION_ERROR and EsimilartoF < ROTATION_ERROR :
            print("90 degree rotation detected")
            HRotated=np.rot90(ImagetoArray(triplet3[1]),3)
            for key,value in answeroptions.items():
                confidencerating[key]=arrayidentical(HRotated,ImagetoArray(value))
    return confidencerating


def degree45(triplet1, triplet2, triplet3, answeroptions):
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    ARotated = np.rot90(ImagetoArray(triplet1[0]), 3)
    AsimilartoC = arrayidentical(ImagetoArray(triplet1[2]), ARotated)
    if AsimilartoC < ROTATION_ERROR :
        DRotated = np.rot90(ImagetoArray(triplet2[0]), 3)
        DsimilartoF = arrayidentical(ImagetoArray(triplet2[2]), DRotated)
        print(DsimilartoF)

        if DsimilartoF < ROTATION_ERROR:
            print("45 degree rotation detected")
            HRotated = np.rot90(ImagetoArray(triplet3[0]), 3)
            for key, value in answeroptions.items():
                confidencerating[key] = arrayidentical(HRotated, ImagetoArray(value))
    return confidencerating


def pixelcheck(triplet1, triplet2, triplet3, answeroptions):
    #p(A)=p(C)
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    pixelsAandC=pixeltolrence(triplet1[0],triplet1[2])
    pixelsDandF=pixeltolrence(triplet2[0],triplet2[1])
    if pixelsAandC < BLACK_PIXEL_COUNT_TOLERENCE and pixelsDandF <BLACK_PIXEL_COUNT_TOLERENCE:
        print("p(A)+p(C)=p(B) detected")
        for key,value in answeroptions.items():
            pixelsGandOption=pixeltolrence(triplet3[0],value)
            confidencerating[key]+=pixelsGandOption
    return confidencerating


def pixeltolrence(A,B):
    pixelsA = black_pixel_count_of_image(A)
    pixelsC = black_pixel_count_of_image(B)
    tolerence = ((abs(pixelsA - (pixelsC))) / (
            ImagetoArray(A).shape[0] * ImagetoArray(A).shape[1]))
    return tolerence

def convert_to_array(f,a):
    for key,value in f.items():
        figures[key]=ImagetoArray(value)
    for key,value in a.items():
        answeroptions[key]=ImagetoArray(value)



def halfandhalf(triplet1):
    WholeArray=ImagetoArray(triplet1[0])
    halfwidth=int(WholeArray.shape[1]/2)
    firthalf=WholeArray[0:,0:halfwidth]
    secondhalf=WholeArray[0:,halfwidth:]
    #Are the two images reflections of each other?
    print(arrayidentical(firthalf,secondhalf))
    print(arrayidentical(np.flipud(firthalf),secondhalf))
    print(arrayidentical(firthalf,np.fliplr(secondhalf)))
    Image.fromarray(firthalf).save('firsthalf.jpeg')
    Image.fromarray(secondhalf).save('secondhalf.jpeg')
    Image.fromarray(np.fliplr(secondhalf)).save('secondhalfdeduced.jpeg')

    if arrayidentical(firthalf,np.fliplr(secondhalf))< SIMILARITY:
        print("reflection detected")
        #sum should be equal to B.
        sum = np.logical_and(firthalf, np.fliplr(secondhalf))
        print(arrayidentical(sum,ImagetoArray(triplet1[1])))
        load_img_rz = np.array(triplet1[1].resize((92, 184)))
        Image.fromarray(load_img_rz).save('temp1.jpeg')
        Image.fromarray(sum).save('temp2.jpeg')

        print("After resizing:", load_img_rz.shape,sum.shape)
        print(arrayidentical(sum, load_img_rz))








