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


#VARIABLE
urlRepository = "https://repositorio.ufpb.br"
urlReport = ""
#mainURL = 'https://repositorio.ufpb.br/jspui/handle/tede/3768/simple-search?query=&filter_field_1=type&filter_type_1=equals&filter_value_1=Tese&sort_by=score&order=desc&rpp=200&etal=0&start=0'
##mainURL = 'https://repositorio.ufpb.br/jspui/handle/tede/3768/simple-search?query=&filter_field_1=type&filter_type_1=equals&filter_value_1=Tese&sort_by=score&order=desc&rpp=2&etal=0&start=0'
#mainURL = 'https://repositorio.ufpb.br/jspui/handle/tede/3768/simple-search?location=tede%2F3768&query=&filtername=type&filtertype=equals&filterquery=Disserta%C3%A7%C3%A3o&rpp=300&sort_by=score&order=desc'
mainURL = 'https://repositorio.ufpb.br/jspui/handle/tede/3768/simple-search?location=tede%2F3768&query=&filtername=type&filtertype=equals&filterquery=Disserta%C3%A7%C3%A3o&rpp=2&sort_by=score&order=desc'

#FILES

fileCSV = "levantamento_ppga_2025.csv"

#COLOR
RED    = '\33[31m'
GREEN  = '\33[32m'
WHITE  = '\33[37m'
YELLOW = '\33[33m'

#ARRAY
summaryReportIndividual = []
summaryReport = []
specificURLArray = []


def bannerPrint():
    print ("""        
    ██╗    ██╗███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗     ██████╗ ██████╗  ██████╗  █████╗     ██╗   ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗    ██║   ██║██╔════╝██╔══██╗██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝    ██████╔╝██████╔╝██║  ███╗███████║    ██║   ██║█████╗  ██████╔╝██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║    ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║    ██║     ██║     ╚██████╔╝██║  ██║    ╚██████╔╝██║     ██║     ██████╔╝
    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ 
                                                                                                                                                                
           """ + "\ndeveloped by icarot\nVersion: 0.0.1\n")



bannerPrint()
print(f'{GREEN}[INFO] Replace manually the content of the variable "mainURL" to change the search made by this script.{WHITE}')
print(f'{GREEN}[INFO] Current URL: {WHITE}{mainURL}')

try:
    resMain = requests.get(mainURL)
except requests.exceptions.Timeout:
    print(f'{RED}[ERROR] Connection timeout. {WHITE}')
except requests.exceptions.TooManyRedirects:
    print(f'{RED}[ERROR] Too Many Redirects. {WHITE}')
except requests.exceptions.RequestException as e:
    raise SystemExit(e)

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
            try:
                resSpecific = requests.get(specificURL)
            except requests.exceptions.Timeout:
                print(f'{RED}[ERROR] Connection timeout. {WHITE}')
            except requests.exceptions.TooManyRedirects:
                print(f'{RED}[ERROR] Too Many Redirects. {WHITE}')
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)

            specificHTMLPage = resSpecific.text

            for string in re.findall(regexTypeDocumentPattern, str(specificHTMLPage)):
                if string:
                    Type = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexDateDocumentPattern, str(specificHTMLPage)):
                if string:
                    Date = string
                    break

            for string in re.findall(regexTitleDocumentPattern, str(specificHTMLPage)):
                if string:
                    Title = '"' + string.replace('&#x20;', ' ') + '"'
                    break

            for string in re.findall(regexAuthorDocumentPattern, str(specificHTMLPage)):
                if string:
                    Authors = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexAdvisorDocumentPattern, str(specificHTMLPage)):
                if string:
                    Advisor = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexCoAdvisorDocumentPattern, str(specificHTMLPage)):
                if string:
                    CoAdvisor = string.replace('&#x20;', ' ')
                    break
            if not CoAdvisor:
                CoAdvisor = "False"

            for string in re.findall(regexAbstractDocumentPattern, str(specificHTMLPage)):
                if string:
                    Abstract = '"' + string.replace('&#x20;', ' ') + '"'
                    break

            for string in re.findall(regexKeywordsDocumentPattern, str(specificHTMLPage)):
                if string:
                    Keywords = '"' + string.replace('&#x20;', ' ').replace('<br />',', ') + '"'
                    break
            
            for string in re.findall(regexLanguageDocumentPattern, str(specificHTMLPage)):
                if string:
                    Language = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexCitationDocumentPattern, str(specificHTMLPage)):
                if string:
                    Citation = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexURIDocumentPattern, str(specificHTMLPage)):
                if string:
                    reportURL = string.replace('&#x20;', ' ')
                    break

            for string in re.findall(regexPDFfileURLPattern, str(specificHTMLPage)):
                if string:
                    pdfURL = string.replace('&#x20;', ' ')
                    break

            writer.writerow([Type, Date, Title, Authors, Advisor, CoAdvisor, Abstract, Keywords, Language, Citation, reportURL, pdfURL])

if os.path.isfile(fileCSV):
    print(f'{GREEN}[INFO] File created {YELLOW}{fileCSV}{WHITE}')
else:
    print(f'{RED}[ERROR] File not created {YELLOW}{fileCSV}{WHITE}')
