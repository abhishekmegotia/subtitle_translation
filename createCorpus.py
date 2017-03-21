import os
import csv
import gzip
import re
import sys
import tarfile
import timeit
import urllib
import zipfile
from os import listdir
from multiprocessing import Pool
from collections import OrderedDict
from io import BytesIO
from tempfile import mktemp
from urllib.request import urlretrieve
from xml.dom.minidom import parse, parseString
from lxml import etree

from handleException import ErrorTypes, handleFileDownloadException

currentDirectory = os.path.dirname(__file__)
inputDir = os.path.join(currentDirectory, 'input12')
outputDir = os.path.join(currentDirectory, 'output12')

def parseSubtitlesXML(xmlFileContent):
    context = etree.iterparse(BytesIO(str.encode(xmlFileContent)))
    timeFrameText = ""
    sequenceDict = {}
    for action, elem in context:
        if not elem.text:
            text = "None"
        else:
            text = elem.text
        if (elem.tag == "w"):
            if (text.lower().startswith((".", "'", "!", "@", "?", ",", "%",
                                         "&", "(", ")", ";", ":", "\""))):
                timeFrameText = timeFrameText[:-1]
            timeFrameText += text + " "
        if (elem.tag == "s"):
            timeFrameText = timeFrameText[:-1]
            sequenceDict[elem.get("id")] = timeFrameText
            timeFrameText = ""
    return sequenceDict

def process_file(inputFile):
    if(inputFile == "1.txt"):
        print (inputFile)
        inputFileName = inputFile
        inputFile = os.path.join(inputDir, inputFile)
        currentTextFile = open(inputFile)
        completeDict = OrderedDict()
        for line in currentTextFile:
            line = re.split(r'\t+|\n', line)
            del line[-1]
            spanishId = re.split(r'\.', re.split(r'\/', line[1])[3])[0]
            if (spanishId in completeDict):
                completeDict[spanishId][2] = completeDict[spanishId][2] + "," + line[2]
                completeDict[spanishId][3] = completeDict[spanishId][3] + "," + line[3]
            else:
                completeDict[spanishId] = completeDict.get(spanishId, line)
        completeDict.popitem(last=False)[0]
        completeDict.popitem(last=True)[0]
        # print (completeDict.keys())
        # print (completeDict["4194238"])
        # print (completeDict["4194238"])
        # completeDictionary = {}
        # completeDictionary["4194238"] = completeDict["4194238"]

        for eachId, corpusList in completeDict.items():
            try:
                filename = mktemp('english.gz')
                urllib.request.urlretrieve(
                    "http://opus.lingfil.uu.se/OpenSubtitles2016/xml/" + corpusList[0],
                    filename)
                fileReader = gzip.open(filename)
                xmlContent = parseString(fileReader.read()).toxml()
                englishXMLFileContent = parseSubtitlesXML(xmlContent)
                filename = mktemp('spanish.gz')
                urllib.request.urlretrieve(
                    "http://opus.lingfil.uu.se/OpenSubtitles2016/xml/" + corpusList[1],
                    filename)
                fileReader = gzip.open(filename)
                xmlContent = parseString(fileReader.read()).toxml()
                spanishXMLFileContent = parseSubtitlesXML(xmlContent)
            except Exception as ex:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(exc_type, fname, exc_tb.tb_lineno)
                # handleFileDownloadException(ErrorTypes.FileDownloadError, message)
                continue

            enTimeFrameIds = corpusList[2].split(',')
            esTimeFrameIds = corpusList[3].split(',')
            movieTextEnglish = eachId + "$ "
            movieTextSpanish = eachId + "$ "
            if (len(enTimeFrameIds) == len(esTimeFrameIds)):
                for index, englishIds in enumerate(enTimeFrameIds):
                    spanishIds = esTimeFrameIds[index]
                    for value in englishIds.split(' '):
                        movieTextEnglish += str(englishXMLFileContent.get(value))
                    for value in spanishIds.split(' '):
                        movieTextSpanish += str(spanishXMLFileContent.get(value))
                    movieTextEnglish += "$ "
                    movieTextSpanish += "$ "

                try:
                    # print (inputFileName.split('.')[0])
                    # print (outputDir + "/" + inputFileName.split('.')[0] + "_en.txt")
                    fileReader = open(outputDir + "/" + inputFileName.split(".")[0]+"_en.txt", "a", encoding="utf8")
                    fileReader.write(movieTextEnglish + "\n")

                    fileReader = open(outputDir + "/" + inputFileName.split(".")[0]+"_es.txt", "a", encoding="utf8")
                    fileReader.write(movieTextSpanish + "\n")
                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
            else:
                handleFileDownloadException(
                    ErrorTypes.IdsMismatchError,
                    "Corpus not found : " + str(corpusList[0] + " : " + corpusList[1]))
            fileReader.close()

            print(
                str(eachId) + " : " + str(len(corpusList[2].split(','))) + " : " + str(
                    len(corpusList[3].split(','))))


if __name__ == '__main__':
    p = Pool(12)
    p.map(process_file, listdir(inputDir))
