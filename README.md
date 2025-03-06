# Web Scraper PPGA - UFPB


Projeto desenvolvido como parte da pesquisa científica conduzida pelas professoras Andressa Sullamyta Pessoa de Lima Torres, doutoranda do PPGA-UFPB e Anna Carolina Rodrigues Orsini - IFPB Guarabira.

**Questão de pesquisa:** Como a produção acadêmica e científica do Programa de Pós-Graduação em Administração
 da UFPB evoluiu ao longo dos últimos 50 anos, e de que maneira essa evolução contribuiu
 para sua consolidação como referência no ensino de Administração no Brasil?

**Objetivo geral:**  Analisar a evolução histórica da produção acadêmica e científica do Programa de Pós
Graduação em Administração da UFPB ao longo dos últimos 50 anos.

**Objetivos específicos:** 
- Mapear os principais temas e tendências das pesquisas desenvolvidas no programa;
- Mapear as abordagens metodológicas mais utilizadas nas dissertações e teses;
- Mapear as redes de colaboração entre pesquisadores do programa e outras instituições;
- Mapear outros dados que evidenciem a produtividade do PPGA no tempo;
- Propor uma reflexão sobre a evolução do PPGA e sua relevância para o ensino em Administração no Brasil

## Usage:

* **Help:**

```
$ python3 webScraperPPGAUFPB.py --help
        
    ██╗    ██╗███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗     ██████╗ ██████╗  ██████╗  █████╗     ██╗   ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗    ██║   ██║██╔════╝██╔══██╗██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝    ██████╔╝██████╔╝██║  ███╗███████║    ██║   ██║█████╗  ██████╔╝██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║    ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║    ██║     ██║     ╚██████╔╝██║  ██║    ╚██████╔╝██║     ██║     ██████╔╝
    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ 
                                                                                                                                                                
           
developed by icarot
requested by Andressa Sullamyta Pessoa de Lima Torres (PPGA-UFPB) and Anna Carolina Rodrigues Orsini (IFPB Guarabira)
Version: 1.0.0

usage: webScraperPPGAUFPB.py [-h] [-dt <thesis or dissertation>] [-qtd QUANTITY] [-cfn <e.g.: levantamento_ppga_ufpb_2025.csv>]

options:
  -h, --help            show this help message and exit
  -dt, --doctype <thesis or dissertation>
                        Inform which document type do you want 'thesis' or 'dissertation'
  -qtd, --quantity QUANTITY
                        Inform the amount of lines/report details do you want.
  -cfn, --csvfilename <e.g.: levantamento_ppga_ufpb_2025.csv>
                        Inform the CSV filename do you want.
```
* **Command variation 1:**
```
$ python3 webScraperPPGAUFPB.py --doctype thesis -qtd 2
        
    ██╗    ██╗███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗     ██████╗ ██████╗  ██████╗  █████╗     ██╗   ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗    ██║   ██║██╔════╝██╔══██╗██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝    ██████╔╝██████╔╝██║  ███╗███████║    ██║   ██║█████╗  ██████╔╝██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║    ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║    ██║     ██║     ╚██████╔╝██║  ██║    ╚██████╔╝██║     ██║     ██████╔╝
    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ 
                                                                                                                                                                
           
developed by icarot
requested by Andressa Sullamyta Pessoa de Lima Torres (PPGA-UFPB) and Anna Carolina Rodrigues Orsini (IFPB Guarabira)
Version: 1.0.0

[INFO] Collecting data from page https://repositorio.ufpb.br/jspui/handle/tede/8271
[INFO] Collecting data from page https://repositorio.ufpb.br/jspui/handle/tede/7942
[INFO] File created levantamento_ppga_ufpb_2025.csv
```

* **Command variation 2:**
```
$ python3 webScraperPPGAUFPB.py --doctype thesis -qtd 2 --csvfilename newnameCSVfile.csv
        
    ██╗    ██╗███████╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗     ██████╗ ██████╗  ██████╗  █████╗     ██╗   ██╗███████╗██████╗ ██████╗ 
    ██║    ██║██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗    ██║   ██║██╔════╝██╔══██╗██╔══██╗
    ██║ █╗ ██║█████╗  ██████╔╝███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝    ██████╔╝██████╔╝██║  ███╗███████║    ██║   ██║█████╗  ██████╔╝██████╔╝
    ██║███╗██║██╔══╝  ██╔══██╗╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗    ██╔═══╝ ██╔═══╝ ██║   ██║██╔══██║    ██║   ██║██╔══╝  ██╔═══╝ ██╔══██╗
    ╚███╔███╔╝███████╗██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║    ██║     ██║     ╚██████╔╝██║  ██║    ╚██████╔╝██║     ██║     ██████╔╝
    ╚══╝╚══╝ ╚══════╝╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚═╝     ╚═╝     ╚═════╝ 
                                                                                                                                                                
           
developed by icarot
requested by Andressa Sullamyta Pessoa de Lima Torres (PPGA-UFPB) and Anna Carolina Rodrigues Orsini (IFPB Guarabira)
Version: 1.0.0

[INFO] Collecting data from page https://repositorio.ufpb.br/jspui/handle/tede/8271
[INFO] Collecting data from page https://repositorio.ufpb.br/jspui/handle/tede/7942
[INFO] File created newnameCSVfile.csv
```
