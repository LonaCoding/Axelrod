import shutil #move files
import os #get list of files in folder
import re #regular expression, for finding specific file names

#bookkeeping script
#puts output files in folder

def searchAndMoveFiles(FilePrefix,destFolder,fileDir=os.listdir()):
    numFileMoved=0
    for fileName in fileDir:
        t=re.search(FilePrefix,fileName) #check for match
        if t: #if file name matches
            outputNewPath = shutil.move(fileName, destFolder) #move the saved image plot to output folder
            print(outputNewPath)
            numFileMoved=numFileMoved+1
    return numFileMoved


#mainFileDir = os.listdir() #gets list of files in main/top-level Axelrod directory
#get file names that matches criteria

#First part of file names to look for and move
outPrefixText="outputMor"
outPrefixText2="NashEqOutput"
outPrefixPlot="EliteMoranProc"
#destination folder relative paths
destFolderText="MoranElitistExperiments_Output/TextOutputs"
destFolderPlot="MoranElitistExperiments_Output/Plots"

#execute functions
numberFileMovedText=searchAndMoveFiles(outPrefixText,destFolderText)
print("Number of Text files moved: {}".format(numberFileMovedText))
numberFileMovedText2=searchAndMoveFiles(outPrefixText2,destFolderText)
print("Number of Nash Text files moved: {}".format(numberFileMovedText2))
numberFileMovedPlot=searchAndMoveFiles(outPrefixPlot,destFolderPlot)
print("Number of plot files moved: {}".format(numberFileMovedPlot))
