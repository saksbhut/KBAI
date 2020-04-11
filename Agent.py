# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import random
from Echallenge import *
SIMILARITY=0.05
ADD_SIMILARITY_TOLERENCE=0.04
#ADD_SIMILARITY_TOLERENCE=0.01
CYCLE_TOLERENCE=0.0045
SUBTRACTTOLERENCE=0.02
BLACK_PIXEL_COUNT_TOLERENCE=0.005
XOR2_TOLERENCE=0.022
from ImageHelper import *


def AllTransformations(figures,answeroptions,problem):
    # Check Row patterns and transformations
    row1 = [figures['A'], figures['B'], figures['C']]
    row2 = [figures['D'], figures['E'], figures['F']]
    row3 = [figures['G'], figures['H']]
    confidenceratingrow = RowTransformationsCheck(row1, row2, row3, answeroptions)

    # Check Column patterns and transformations
    col1=[figures['A'], figures['D'], figures['G']]
    col2 = [figures['B'], figures['E'], figures['H']]
    col3 = [figures['G'], figures['H']]
    confidenceratingcol=ColTransformations(col1,col2,col3,answeroptions)

    #Combine the confidence ratings from Row and Coloumn
    confidencerating={}
    for key in confidenceratingcol:
       confidencerating[key]=confidenceratingcol[key]+confidenceratingrow[key]
    print(confidencerating)
    print(int(min(confidencerating, key=confidencerating.get)))
    if "Challenge" in problem.problemSetName:
        confidencerating=Add_condifence_ratings(confidencerating,SolveChallenge(figures, answeroptions))

    return int(min(confidencerating, key=confidencerating.get))

#Column Inspection
def ColTransformations(col1,col2,col3,answeroptions):
    confidencerating = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    #1. Pixels
    #1.1 NoOfPixels(A)=NoOfPixels(D)+NoOfPixels (G)
    tolerence1=black_pixel_count_differnce(col1[0],col1[1],col1[2])
    tolerence2=black_pixel_count_differnce(col2[0],col2[1],col2[2])
    if tolerence1 < BLACK_PIXEL_COUNT_TOLERENCE and tolerence2 <BLACK_PIXEL_COUNT_TOLERENCE:
        print("we have found a pixel match A=D+G")
        for key, value in answeroptions.items():
         confidencerating[key] = black_pixel_count_differnce(col3[0], col3[1], value)

    #2. The AND operation i.e.common elements check.
    #2.1 A+G=D
    sumAandG = SUM(col1[0], col1[2])
    # check if sum equals D
    sumAandGequalsD = arrayidentical(sumAandG, ImagetoArray(col1[1]))
    sumBandH = SUM(col2[0], col2[2])
    sumBandHequalsE = arrayidentical(sumBandH, ImagetoArray(col2[1]))
    if sumAandGequalsD < ADD_SIMILARITY_TOLERENCE and sumBandHequalsE < ADD_SIMILARITY_TOLERENCE:
        print("A+G=D detected")
        for key, value in answeroptions.items():
            sumCandOption= SUM(col3[0], value)
            confidence=arrayidentical(sumCandOption,ImagetoArray(col3[1]))
            confidencerating[key] += confidence

    return confidencerating

def RowTransformationsCheck(row1, row2, row3, answeroptions):
    confidencerating={'1':0,'2':0,'3':0,'4':0,'5':0,'6':0,'7':0,'8':0}
    #Pixel check
    confidencerating=Add_condifence_ratings(confidencerating,PixelSumCheckRow(row1,row2,row3,answeroptions))
    #COMBINATION A+B =C and D+E =F
    sumAandB=SUM(row1[0],row1[1])
    #check if sum equals C
    sumAandBequalsC=arrayidentical(sumAandB,ImagetoArray(row1[2]))
    sumDandE=SUM(row2[0],row2[1])
    sumDandEequalsF=arrayidentical(sumDandE,ImagetoArray(row2[2]))
    if sumAandBequalsC < ADD_SIMILARITY_TOLERENCE and sumDandEequalsF < ADD_SIMILARITY_TOLERENCE:
        sumGandH=SUM(row3[0],row3[1])
        ADDsimilarity=similarityindex1(sumGandH,answeroptions)
        for key,value in ADDsimilarity.items():
            confidencerating[str(key)]+=value
        return confidencerating

    # COMBINATION A+C =B and D+F =E
    sumAandC = SUM(row1[0], row1[2])

    sumAandCequalsB = arrayidentical(sumAandC, ImagetoArray(row1[1]))
    sumDandF = SUM(row2[0], row2[2])
    sumDandFequalsE = arrayidentical(sumDandF, ImagetoArray(row2[1]))
    if sumAandCequalsB < ADD_SIMILARITY_TOLERENCE and sumDandFequalsE < ADD_SIMILARITY_TOLERENCE:
        print("A+C=B detected")
        for key,value in answeroptions.items():
            sumGandOption=SUM(row3[1],value)
            confidencerating[key]+=arrayidentical(sumGandOption,ImagetoArray(row3[1]))

    print("attempting row xor")
    confidenceratingxor=PerformROWXORS(row1,row2,row3,answeroptions)
    confidencerating= Add_condifence_ratings(confidencerating,confidenceratingxor)
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


def DandEproblems(figures, answeroptions,problem):
    #Horizontal identical?
    if identical(figures['A'],figures['B'])< SIMILARITY and identical(figures['B'],figures['C'])<SIMILARITY:
        print("Horizontal similarity detected")
        #Finding closest option from options to image G and H
        similarityindexG=similarityindex(figures['G'],answeroptions)
        similarityindexH=similarityindex(figures["H"],answeroptions)
        similarityindexcombined={}
        for key,value in similarityindexG.items():
            if value < similarityindexH[key]:
                similarityindexcombined[key]=similarityindexH[key]
            else:
                similarityindexcombined[key]=similarityindexG[key]
        #return (min(similarityindexcombined, key=similarityindexcombined.get))
    #TODO: Add vertical and diagnoal similarities.

    #cyclicity check?
    ABDifference=identical(figures['A'],figures['B'])
    EFDifference=identical(figures['E'],figures['F'])
    BCDifference=identical(figures['B'],figures['C'])
    FDDifference=identical(figures['F'],figures['D'])
    if abs(EFDifference-ABDifference)<=CYCLE_TOLERENCE and abs(BCDifference-FDDifference)<=CYCLE_TOLERENCE:
        print("cycle detection")
        for key, value in answeroptions.items():
            optionGDifference=identical(value,figures['G'])
            optionHDifference=identical(value,figures['H'])
            optionDEDifference=identical(figures['E'],figures['D'])
            if abs(optionGDifference-ABDifference)<=CYCLE_TOLERENCE and abs(optionHDifference-optionDEDifference)<=CYCLE_TOLERENCE:
                return int(key)

    #Vertical subtraction is consistent
    ADDifference=identical(figures['A'],figures['D'])
    BEDifference=identical(figures['B'],figures['E'])
    CFDifference=identical(figures['C'],figures['F'])
    DEDifference=identical(figures['D'],figures['E'])

    #ROW XOR

    return AllTransformations(figures,answeroptions,problem)
    return -1
#returns an array that stores the degree of simularity between given image(an array) and all the answeroptions.
def similarityindex(image,answeroptions):
    simindex={}
    for key, value in answeroptions.items():
        simindex[int(key)] = identical(image, value)
    return simindex




class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass



    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        #creating two dictionaries representing the figures and potential answers
        figures,answeroptions=createdictionaries(problem);

        print("Now starting to solve problem",problem.name)
        if problem.problemType=="3x3":
            return DandEproblems(figures, answeroptions,problem)
        else:
            random.randint(1, 6)

        return random.randint(1, 8)