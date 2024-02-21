import subprocess
import re
import dirD

def checkw(kw):
    if(" " in kw):
        return kw.replace(" ", "+")
    else:
        return kw

def purgeB(string):
    newS = ""
    for i in range(len(string) - 1):
        if (string[i] == "\\") and (string[i + 1] == "n"): newS = newS
        else: newS += string[i]
    return newS

def urlFilter(url):
    url = str(url)
    url = url.replace("<cite>", "")
    url = url.replace("</cite>", "")
    url = purgeB(url)
    return url
 
def urlFilter2(url):
    url = str(url)
    newUrl = ""
    if url == "[]":
        return ""
    else:
        for i in range(len(url)):
            if url[i] == "'":
                newUrl = newUrl
            elif url[i] == "]":
                newUrl = newUrl
            elif url[i] == "[":
                newUrl = newUrl
            else:
                newUrl += url[i]
    return newUrl

def checkP(url, array):
    if(url in array and url != ""): return True
    else: return False

def parseUrl():
    arrayUrl = []
    with open("result/urlRecup.txt", "r+", encoding='utf-8') as f:
        for ligne in f:
            mots = ligne.split()
            for mot in mots :
                if ('href' in mot):
                    mot = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', mot)
                    mot = urlFilter2(mot)
                    if(checkP(mot, arrayUrl) == False): arrayUrl.append(urlFilter2(mot))
                elif '<cite>' in mot :
                    mot = urlFilter(mot)
                    if(checkP(mot, arrayUrl) == False): arrayUrl.append(mot)
    return arrayUrl

def writeInFile(array, file):
    with open(file, "w", encoding='utf-8') as f:
        for url in array:
            if url[:8] != "https://":
                string = "http://" + str(url) + "\n"
                f.write(string)
            else:
                f.write(str(url) + "\n")

def checkArray(array):
    newArray = []
    for i in array:
        if i[:7] != "http://" and i != '':
            newArray.append(i)
    return newArray

def main():
    
    #Remise à 0 du fichier urlRecup.txt
    dirD.clear_file("result/urlRecup.txt")

    #Mise en place des variables
    resultF = "wordlists/sitesUtilisables.txt" 
    array4KW = ["Cyllene", "ITS", "hacker", "data leak", "french leak", "french company", "french data"]
    
    for kw in array4KW:
            kw = checkw(kw)
            request = "https://ahmia.fi/search/?q=" + kw
            answer = subprocess.run(['curl', request], capture_output=True, text=True, encoding='utf-8')
            with open("result/urlRecup.txt", "a+", encoding='utf-8') as f:
                f.write(str(answer))
    arrayUrl = parseUrl()
    arrayUrl = checkArray(arrayUrl)
    writeInFile(arrayUrl, resultF)
    print("done")
    
    #Remise à 0 du fichier urlRecup.txt
    dirD.clear_file("result/urlRecup.txt")
    return 0


if __name__ == "__main__":
    main()
    