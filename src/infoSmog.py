import re

file = open("2dayex.txt", "r").read()
regex_startfile = re.compile("FLCN41 CWUL")
regex_end = "END"

#####
# regions
reg_gatineau = re.compile("GATINEAU\.")
reg_GMA = re.compile(
    "METRO MONTREAL - LAVAL\nVAUDREUIL - SOULANGES - HUNTINGDON\nRICHELIEU VALLEY - SAINT-HYACINTHE\nLACHUTE - SAINT-JEROME\nLANAUDIERE\.")
reg_laurent = re.compile("LAURENTIANS\.")
reg_drum = re.compile("DRUMMONDVILLE - BOIS-FRANCS\.")
reg_maur = re.compile("MAURICIE\.")
reg_town = re.compile("EASTERN TOWNSHIPS\.")
reg_GQA = re.compile("QUEBEC\nMONTMAGNY - L'ISLET\nBEAUCE\.")
reg_abit = re.compile("ABITIBI\.")
reg_temis = re.compile("TEMISCAMINGUE\.")
reg_LSJ = re.compile("LAC-SAINT-JEAN\.")
reg_sag = re.compile("SAGUENAY\.")
reg_riv = re.compile("KAMOURASKA - RIVIERE-DU-LOUP - TROIS-PISTOLES\nTEMISCOUATA\.")
reg_montLaur = re.compile("MONT-LAURIER\.")
reg_latuq = re.compile("LA TUQUE/.")
reg_upperGat = re.compile("UPPER GATINEAU - LIEVRE - PAPINEAU\.")
reg_ = re.compile("KAMOURASKA - RIVIERE-DU-LOUP - TROIS-PISTOLES\nTEMISCOUATA\.")

lst = [re.compile("GATINEAU\."), re.compile(
    "METRO MONTREAL - LAVAL\nVAUDREUIL - SOULANGES - HUNTINGDON\nRICHELIEU VALLEY - SAINT-HYACINTHE\nLACHUTE - SAINT-JEROME\nLANAUDIERE\.")]

for a in lst:
    for b in a.finditer(file):
        print(b)
