import requests
import subprocess
import dirD
import rechercheUrl
import os
import sendEmail

def connectTor():
    session = requests.session()
    session.proxies = {'http':  'socks5h://127.0.0.1:9150',
                   'https': 'socks5h://127.0.0.1:9150'}
    return session

def siteExploitable():

    #Déclaration des variables
    arraySites = []
    siteAenum = "/Users/pierrechemin/Desktop/Cyllene/darkScan/wordlists/sitesUtilisables.txt"
    url = "/Users/pierrechemin/Desktop/Cyllene/darkScan/wordlists/urlUtilisables.txt"
    #On run le dirb et on remplis le rapport et les urls utilisables
    dirD.main()

    #On remplie l'array qui va recevoir les urls à tester
    with open(url, 'r') as f:
        for sites in f:
            arraySites.append(sites)
    return arraySites

def dataWanted():
    arrayData = []
    with open('wordlists/dataWanted.txt', 'r') as f:
        for data in f:
            arrayData.append(data)
    return arrayData

def testTor():
    testTor = subprocess.run(['nc', '-zv', 'localhost', '9150'], capture_output=True, text=True, timeout=5)
    if 'succeeded' in str(testTor):
        print("connecté à TOR")
    else :
        print("pas connecté à TOR - ARRET -")
        return 0

def purgeArray(array):
    for i, string in enumerate(array):
        array[i] = string.replace("\n", "")
    return array

def checkP(string, fichier):

    with open(fichier, 'r', encoding='utf-8') as f:
        for line in f :
            if string in line :
                return True

    return False

def main():
    #Récupération de la session de connection à Tor et test
    session = connectTor()
    if testTor() == 0: return 0

    #Déclaration des fichiers
    resultF = 'result/dataFound.txt'
    recupF = 'wordlists/pageRecup.txt'

    #Refresh du fichier contenant les résultats 
    dirD.clear_file(resultF)
    lengthS = os.path.getsize(resultF)


    #Lancement de la recherhce d'url
    rechercheUrl.main()
    print("RECHERCHE URL FINI")
    
    #Reset du fichier contenant les résultats
    with open(resultF, 'w') as f:
        f.write("")

    #Récupération des données à traiter
    arraySites = purgeArray(siteExploitable()) #Array des url à tester
    arrayData = purgeArray(dataWanted()) #Array des données à tester

    for sites in arraySites:
        if 'http' not in sites: sites = "https://google.com"
        try:
            response = session.get(sites, timeout=10)
        except requests.Timeout:
            print("la requête a été trop longue a répondre: ", sites)
        except requests.ConnectionError:
            print("n'a pas réussi à se connecter: ", sites)
        except requests.HTTPError:
            print("erreur http: ", sites)
        except Exception as e:
            print("Une erreur inattendue s'est produite: ", sites)
            pass
        with open(recupF, 'w', encoding='utf-8') as f:
            f.write(response.text)
        for data in arrayData:
            with open(recupF, 'r', encoding='utf-8') as f:
                for line in f:
                    if data in line:
                        with open(resultF, 'a') as f:
                            string = data+" found in "+sites+"\n"
                            if (checkP(string, resultF) == False):
                                f.write(string)

    lengthE = os.path.getsize(resultF)

    if(lengthS != lengthE): sendEmail.main()

    print("TOUS LES FICHIERS ONT ÉTÉ CHANGÉS")

if __name__ == "__main__":
    main()