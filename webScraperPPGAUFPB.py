"""
Projeto desenvolvido como parte da pesquisa científica conduzida pelas professoras Andressa Sullamyta Pessoa de Lima Torres, doutoranda do PPGA-UFPB e Anna Carolina Rodrigues Orsini - IFPB Guarabira.

Questão de pesquisa: Como a produção acadêmica e científica do Programa de Pós-Graduação em Administração
 da UFPB evoluiu ao longo dos últimos 50 anos, e de que maneira essa evolução contribuiu
 para sua consolidação como referência no ensino de Administração no Brasil?

Objetivo geral:  Analisar a evolução histórica da produção acadêmica e científica do Programa de Pós
Graduação em Administração da UFPB ao longo dos últimos 50 anos.

Objetivos específicos: 
- Mapear os principais temas e tendências das pesquisas desenvolvidas no programa;
- Mapear as abordagens metodológicas mais utilizadas nas dissertações e teses;
- Mapear as redes de colaboração entre pesquisadores do programa e outras instituições;
- Mapear outros dados que evidenciem a produtividade do PPGA no tempo;
- Propor uma reflexão sobre a evolução do PPGA e sua relevância para o ensino em
- Administração no Brasil
"""

#LIBS
import re
import os
import csv
import argparse
import requests
from bs4 import BeautifulSoup

#REGEX
regexRelativeURLPattern = r'\"(.+)\"\>'
regexURLIndexPattern = r'\/([0-9]+)$'
regexTypeDocumentPattern = r'class=\".+\">Tipo:.+value=.+">(.+)<\/a'
regexDateDocumentPattern = r'class=\".+\".+\">([0-9]+\-[A-z]+\-[0-9]+)\<\/'
regexTitleDocumentPattern = r'class=\".+\"\>Título:&nbsp;<\/td><td.+class=".+">(.+)<\/td'
regexAuthorDocumentPattern = r'class=\"author\".+\=.+">(.+)\<\/a'
regexAdvisorDocumentPattern = r'class=".+">.+Orientador:&nbsp;<\/td><td class=".+">(.+)<\/td'
regexCoAdvisorDocumentPattern = r'class=".+">metadata.dc.contributor.advisor-co1:&nbsp;<\/td><td class=".+">(.+)<\/td>'
regexAbstractDocumentPattern = r'class=".+">Resumo:&nbsp;<\/td><td class=".+">(.+)<\/td'
regexKeywordsDocumentPattern = r'class=".+l">Palavras-chave:&nbsp;<\/td><td class=".+">(.+)<\/td'
regexLanguageDocumentPattern = r'class=\".+\">Idioma.+\">(.+)<\/td>'
regexCitationDocumentPattern = r'class=".+">Citação:&nbsp;<\/td><td class=".+">(.+)\<\/td'
regexURIDocumentPattern = r'class=".+">URI:&nbsp;<\/td><td class=".+"><a href="(.+repositorio.+)\">'
regexPDFfileURLPattern = r'name="citation_pdf_url".content="(.+)\"'

#GLOBAL VARIABLES
urlRepository = "https://repositorio.ufpb.br"
urlReport = ""

#COLOR
RED    = '\33[31m'
GREEN  = '\33[32m'
WHITE  = '\33[37m'
YELLOW = '\33[33m'

#ARRAYS
specificURLArray = []
summaryReport = []

#FUNCTIONS
def bannerPrint():
    print ("""        
    ██╗    ██╗███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗     ██████╗ ██████╗  ██████╗  █████╗     ██╗   ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗    ██║   ██║██╔════╝██╔══██╗██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝    ██████╔╝██████╔╝██║  ███╗███████║    ██║   ██║█████╗  ██████╔╝██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║    ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║    ██║     ██║     ╚██████╔╝██║  ██║    ╚██████╔╝██║     ██║     ██████╔╝
    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ 
                                                                                                                                                                
           """ + "\ndeveloped by icarot\nrequested by Andressa Sullamyta Pessoa de Lima Torres (PPGA-UFPB) and Anna Carolina Rodrigues Orsini (IFPB Guarabira)\nVersion: 1.0.0\n")

def getRequest(URL):
    #Proceeds with a HTTP GET Request to a specific URL and returns all content of the HTTP response
    #Usage: varReturn = getRequest(URL)
    try:
        resRequest = requests.get(URL)    
    except requests.exceptions.Timeout:
        print(f'{RED}[ERROR] Connection timeout. {WHITE}')
    except requests.exceptions.TooManyRedirects:
        print(f'{RED}[ERROR] Too Many Redirects. {WHITE}')
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    if resRequest.status_code == 200:
        return resRequest

def findPatternString (regexStringDocumentPattern, specificHTMLPage, quoteFlag):
    #Search for a string pattern and returns with or without quotes
    #Usage: MatchString = findPatternString (regexStringDocumentPattern, specificHTMLPage, True|False)
    for string in re.findall(regexStringDocumentPattern, str(specificHTMLPage)): 
        if string:
            if quoteFlag == True:
                MatchString = '"' + string.replace('&#x20;', ' ').replace('<br />',', ') + '"'
            else:
                MatchString = string.replace('&#x20;', ' ').replace('<br />',', ')
            return MatchString
            
def setParam():
    # Define the parameters of the script.
    #Usage: setParam()
    parser = argparse.ArgumentParser()
    mainOption = parser.add_mutually_exclusive_group()
    mainOption.add_argument("-dt", "--doctype", metavar='<thesis or dissertation>', help="Inform which document type do you want 'thesis' or 'dissertation'")
    parser.add_argument("-qtd", "--quantity", help="Inform the amount of lines/report details do you want.")
    parser.add_argument("-cfn", "--csvfilename", metavar='<e.g.: levantamento_ppga_ufpb_2025.csv>', help="Inform the CSV filename do you want.")

    global args
    args = parser.parse_args()

def menuFlow():
    #Checks parameters passed in the script execution
    #Usage: docType, qtdLines, fileCSV = menuFlow()
    if args.doctype:
        if args.doctype == "thesis":
            docType = "Tese"
        elif args.doctype == "dissertation":
            docType = "Disserta%C3%A7%C3%A3o"
        else:
            print(f'{RED}[ERROR] Inform which document type do you want "thesis" or "dissertation" {WHITE}')
            quit()
        if args.quantity:
            qtdLines = args.quantity
        else:
            print(f'{RED}[ERROR] Please inform the number of line with the param "-qtd" or "--quantity {WHITE}')
            quit()
        if args.csvfilename:
            fileCSV = args.csvfilename
        else:
            fileCSV = "levantamento_ppga_ufpb_2025.csv"
        return docType, qtdLines, fileCSV
    else:
        print(f'{RED}[ERROR] Please inform a document type with the param "-dt" or "--doctype", value "thesis" or "dissertation" {WHITE}')
        quit()

bannerPrint()
setParam()
docType, qtdLines, fileCSV = menuFlow()

mainURL = 'https://repositorio.ufpb.br/jspui/handle/tede/3768/simple-search?query=&filter_field_1=type&filter_type_1=equals&filter_value_1=' + str(docType) + '&sort_by=score&order=desc&rpp=' + str(qtdLines) + '&etal=0&start=0'

resMain = getRequest(mainURL)

#MAIN
mainHTMLPage = resMain.text
soupMain = BeautifulSoup(mainHTMLPage, 'html.parser')
table = soupMain.find('table', class_='table')
for row in table.find_all('tr'):
    urlReportLine = row.find('a',href=True)
    for urlReportRelative in re.findall(regexRelativeURLPattern, str(urlReportLine)):
        urlReport = urlRepository + urlReportRelative
    specificURLArray.append(urlReport)

with open(fileCSV, 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["type", "date", "title", "author", "advisor", "coadvisor", "abstract", "keywords", "language", "citation", "reportURL", "pdfURL"]
    writer.writerow(field)
    for specificURL in specificURLArray:
        Type = ""
        Date = ""
        Title = ""
        Authors = ""
        Advisor = ""
        CoAdvisor = ""
        Abstract = ""
        Keywords = ""
        Language = ""
        Citation = ""
        reportURL = ""
        pdfURL = ""
        specificHTMLPage = ""
        
        if specificURL != "":
            print(f'{GREEN}[INFO] Collecting data from page {YELLOW}{specificURL}{WHITE}')
            resSpecific = getRequest(specificURL)
            specificHTMLPage = resSpecific.text
            
            Type = findPatternString(regexTypeDocumentPattern, specificHTMLPage, False)
            Date = findPatternString(regexDateDocumentPattern, specificHTMLPage, False)
            Title = findPatternString(regexTitleDocumentPattern, specificHTMLPage, True)
            Authors = findPatternString(regexAuthorDocumentPattern, specificHTMLPage, False)
            Advisor = findPatternString(regexAdvisorDocumentPattern, specificHTMLPage, False)
            CoAdvisor = findPatternString(regexCoAdvisorDocumentPattern, specificHTMLPage, False)
            Abstract = findPatternString(regexAbstractDocumentPattern, specificHTMLPage, True)
            Keywords = findPatternString(regexKeywordsDocumentPattern, specificHTMLPage, True)
            Language = findPatternString(regexLanguageDocumentPattern, specificHTMLPage, False)
            Citation = findPatternString(regexCitationDocumentPattern, specificHTMLPage, False)
            reportURL = findPatternString(regexURIDocumentPattern, specificHTMLPage, False)
            pdfURL = findPatternString(regexPDFfileURLPattern, specificHTMLPage, False)
            
            writer.writerow([Type, Date, Title, Authors, Advisor, CoAdvisor, Abstract, Keywords, Language, Citation, reportURL, pdfURL])
            
if os.path.isfile(fileCSV):
    print(f'{GREEN}[INFO] File created {YELLOW}{fileCSV}{WHITE}')
else:
    print(f'{RED}[ERROR] File not created {YELLOW}{fileCSV}{WHITE}')
