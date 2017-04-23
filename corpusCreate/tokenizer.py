import re

class Tokenizer:
    CorpusDict = {}

    def readFile(self):
        # with open("2_en.txt", "r", encoding="utf8") as file:
        enOut = open("tokenized_en.en", "w", encoding="utf8")
        with open("en.en", "r", encoding="utf8") as file:
            countEn = 0
            for line in file:
                if line:
                    line = line.rstrip()

                    #line = line.replace("+ + + + +","")

                    countEn += line.count("+++++")

                    #line = line.lower()
                    line = re.sub("[^'+A-z\d ]", ' ', line)
                    #print(line)
                    subtitles = line.split("+++++")

                    count = 0
                    for sub in subtitles:
                        if sub == '':
                            continue
                        if count == 0:
                            subID = sub
                            count = count + 1
                            continue


                        words = sub.split(' ')

                        newLine = ""
                        for word in words:
                            if word == ' ' or word == '':
                                continue
                            word = word.strip()
                            if newLine == "":
                                newLine = word
                            else:
                                newLine = newLine + " " + word


                        enOut.write(newLine.strip())
                        enOut.write("\n")
            print(countEn)
        enOut.close()

        esOut = open("tokenized_es.es", "w", encoding="utf8")
        with open("es.es", "r", encoding="utf8") as file:
            countEs = 0
            for line in file:
                if line:
                    line = line.rstrip()

                    countEs += line.count("+++++")

                    symToRemove = re.sub("(?i)(?:(?![×Þß÷þø])[a-zA-Z0-9À-ÿ+])", "", line)

                    symbols = symToRemove.split(' ')
                    for sym in symbols:
                        line = line.replace(sym,"")

                    #print(line)
                    subtitles = line.split("+++++")

                    count = 0
                    for sub in subtitles:
                        if sub == '':
                            continue
                        if count == 0:
                            subID = sub
                            count = count + 1
                            continue


                        words = sub.split(' ')

                        newLine = ""
                        for word in words:
                            if word == ' ' or word == '':
                                continue
                            word = word.strip()
                            if newLine == "":
                                newLine = word
                            else:
                                newLine = newLine + " " + word


                        esOut.write(newLine.strip())
                        esOut.write("\n")


                        #print(self.CorpusDict)
            print(countEs)
        esOut.close()


obj = Tokenizer()
obj.readFile()
