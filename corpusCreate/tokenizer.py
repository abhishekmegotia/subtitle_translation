import re

class Tokenizer:
    CorpusDict = {}

    def readFile(self):
        # with open("2_en.txt", "r", encoding="utf8") as file:
        enOut = open("en.txt", "w")
        with open("2_en.txt", "r", encoding="utf8") as file:
            for line in file:
                if line:
                    line = line.rstrip()
                    #line = line.lower()
                    line = re.sub("[^'$A-z\d ]", ' ', line)
                    # print(line)
                    subtitles = line.split('$')

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

        enOut.close()

        esOut = open("es.txt", "w")
        with open("2_es.txt", "r", encoding="utf8") as file:
            for line in file:
                if line:
                    line = line.rstrip()
                    symToRemove = re.sub("(?i)(?:(?![×Þß÷þø])[a-zA-Z0-9À-ÿ$])", "", line)

                    symbols = symToRemove.split(' ')
                    for sym in symbols:
                        line = line.replace(sym,"")

                    subtitles = line.split('$')

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
        esOut.close()


obj = Tokenizer()
obj.readFile()
