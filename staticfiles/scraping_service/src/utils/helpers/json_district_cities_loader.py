import json

district_json = '''
[
  {
    "id": 1,
    "name": "Bánovce nad Bebravou",
    "veh_reg_num": "BN",
    "code": 301,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-banovce-nad-bebravou",
    "toprealityskurl": "banovce-nad-bebravou",
    "realityskurl": "okres-banovce-nad-bebravou"
  },
  {
    "id": 2,
    "name": "Banská Bystrica",
    "veh_reg_num": "BB",
    "code": 601,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-banska-bystrica",
    "toprealityskurl": "banska-bystrica",
    "realityskurl": "okres-banska-bystrica"
  },
  {
    "id": 3,
    "name": "Banská Štiavnica",
    "veh_reg_num": "BS",
    "code": 602,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-banska-stiavnica",
    "toprealityskurl": "banska-stiavnica",
    "realityskurl": "okres-banska-stiavnica"
  },
  {
    "id": 4,
    "name": "Bardejov",
    "veh_reg_num": "BJ",
    "code": 701,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-bardejov",
    "toprealityskurl": "bardejov",
    "realityskurl": "okres-bardejov"
  },
  {
    "id": 5,
    "name": "Bratislava I",
    "veh_reg_num": "BA, BL",
    "code": 101,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-braislava-i",
    "toprealityskurl": "bratislava-i",
    "realityskurl": "okres-bratislava-i"
  },
  {
    "id": 6,
    "name": "Bratislava II",
    "veh_reg_num": "BA, BL",
    "code": 102,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-bratislava-ii",
    "toprealityskurl": "bratislava-ii",
    "realityskurl": "okres-bratislava-ii"
  },
  {
    "id": 7,
    "name": "Bratislava III",
    "veh_reg_num": "BA, BL",
    "code": 103,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-bratislava-iii",
    "toprealityskurl": "bratislava-iii",
    "realityskurl": "okres-bratislava-iii"
  },
  {
    "id": 8,
    "name": "Bratislava IV",
    "veh_reg_num": "BA, BL",
    "code": 104,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-bratislava-iv",
    "toprealityskurl": "bratislava-iv",
    "realityskurl": "okres-bratislava-iv"
  },
  {
    "id": 9,
    "name": "Bratislava V",
    "veh_reg_num": "BA, BL",
    "code": 105,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-bratislava-v",
    "toprealityskurl": "bratislava-v",
    "realityskurl": "okres-bratislava-v"
  },
  {
    "id": 10,
    "name": "Brezno",
    "veh_reg_num": "BR",
    "code": 603,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-brezno",
    "toprealityskurl": "brezno",
    "realityskurl": "okres-brezno"
  },
  {
    "id": 11,
    "name": "Bytča",
    "veh_reg_num": "BY",
    "code": 501,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-bytca",
    "toprealityskurl": "bytca",
    "realityskurl": "okres-bytca"
  },
  {
    "id": 12,
    "name": "Čadca",
    "veh_reg_num": "CA",
    "code": 502,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-cadca",
    "toprealityskurl": "cadca",
    "realityskurl": "okres-cadca"
  },
  {
    "id": 13,
    "name": "Detva",
    "veh_reg_num": "DT",
    "code": 604,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-detva",
    "toprealityskurl": "detva",
    "realityskurl": "okres-detva"
  },
  {
    "id": 14,
    "name": "Dolný Kubín",
    "veh_reg_num": "DK",
    "code": 503,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-dolny-kubin",
    "toprealityskurl": "dolny-kubin",
    "realityskurl": "okres-dolny-kubin"
  },
  {
    "id": 15,
    "name": "Dunajská Streda",
    "veh_reg_num": "DS",
    "code": 201,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-dunajska-streda",
    "toprealityskurl": "dunajska-streda",
    "realityskurl": "okres-dunajska-streda"
  },
  {
    "id": 16,
    "name": "Galanta",
    "veh_reg_num": "GA",
    "code": 202,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-galanta",
    "toprealityskurl": "galanta",
    "realityskurl": "okres-galanta"
  },
  {
    "id": 17,
    "name": "Gelnica",
    "veh_reg_num": "GL",
    "code": 801,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-gelnica",
    "toprealityskurl": "gelnica",
    "realityskurl": "okres-gelnica"
  },
  {
    "id": 18,
    "name": "Hlohovec",
    "veh_reg_num": "HC",
    "code": 203,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-hlohovec",
    "toprealityskurl": "hlohovec",
    "realityskurl": "okres-hlohovec"
  },
  {
    "id": 19,
    "name": "Humenné",
    "veh_reg_num": "HE",
    "code": 702,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-humenne",
    "toprealityskurl": "humenne",
    "realityskurl": "okres-humenne"
  },
  {
    "id": 20,
    "name": "Ilava",
    "veh_reg_num": "IL",
    "code": 302,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-ilava",
    "toprealityskurl": "ilava",
    "realityskurl": "okres-ilava"
  },
  {
    "id": 21,
    "name": "Kežmarok",
    "veh_reg_num": "KK",
    "code": 703,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-kezmarok",
    "toprealityskurl": "kezmarok",
    "realityskurl": "okres-kezmarok"
  },
  {
    "id": 22,
    "name": "Komárno",
    "veh_reg_num": "KN",
    "code": 401,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-komarno",
    "toprealityskurl": "komarno",
    "realityskurl": "okres-komarno"
  },
  {
    "id": 23,
    "name": "Košice I",
    "veh_reg_num": "KE",
    "code": 802,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-kosice-i",
    "toprealityskurl": "kosice-i",
    "realityskurl": "okres-kosice-i"
  },
  {
    "id": 24,
    "name": "Košice II",
    "veh_reg_num": "KE",
    "code": 803,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-kosice-ii",
    "toprealityskurl": "kosice-ii",
    "realityskurl": "okres-kosice-ii"
  },
  {
    "id": 25,
    "name": "Košice III",
    "veh_reg_num": "KE",
    "code": 804,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-kosice-iii",
    "toprealityskurl": "kosice-iii",
    "realityskurl": "okres-kosice-iii"
  },
  {
    "id": 26,
    "name": "Košice IV",
    "veh_reg_num": "KE",
    "code": 805,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-kosice-iv",
    "toprealityskurl": "kosice-iv",
    "realityskurl": "okres-kosice-iv"
  },
  {
    "id": 27,
    "name": "Košice-okolie",
    "veh_reg_num": "KS",
    "code": 806,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-kosice-okolie",
    "toprealityskurl": "kosiceokolie",
    "realityskurl": "okres-kosiceokolie"
  },
  {
    "id": 28,
    "name": "Krupina",
    "veh_reg_num": "KA",
    "code": 605,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-krupina",
    "toprealityskurl": "krupina",
    "realityskurl": "okres-krupina"
  },
  {
    "id": 29,
    "name": "Kysucké Nové Mesto",
    "veh_reg_num": "KM",
    "code": 504,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-kysucke-nove-mesto",
    "toprealityskurl": "kysucke-nove-mesto",
    "realityskurl": "okres-kysucke-nove-mesto"
  },
  {
    "id": 30,
    "name": "Levice",
    "veh_reg_num": "LV",
    "code": 402,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-levice",
    "toprealityskurl": "levice",
    "realityskurl": "okres-levice"
  },
  {
    "id": 31,
    "name": "Levoča",
    "veh_reg_num": "LE",
    "code": 704,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-levoca",
    "toprealityskurl": "levoca",
    "realityskurl": "okres-levoca"
  },
  {
    "id": 32,
    "name": "Liptovský Mikuláš",
    "veh_reg_num": "LM",
    "code": 505,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-liptovsky-mikulas",
    "toprealityskurl": "liptovsky-mikulas",
    "realityskurl": "okres-liptovsky-mikulas"
  },
  {
    "id": 33,
    "name": "Lučenec",
    "veh_reg_num": "LC",
    "code": 606,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-lucenec",
    "toprealityskurl": "lucenec",
    "realityskurl": "okres-lucenec"
  },
  {
    "id": 34,
    "name": "Malacky",
    "veh_reg_num": "MA",
    "code": 106,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-malacky",
    "toprealityskurl": "malacky",
    "realityskurl": "okres-malacky"
  },
  {
    "id": 35,
    "name": "Martin",
    "veh_reg_num": "MT",
    "code": 506,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-martin",
    "toprealityskurl": "martin",
    "realityskurl": "okres-martin"
  },
  {
    "id": 36,
    "name": "Medzilaborce",
    "veh_reg_num": "ML",
    "code": 705,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-medzilaborce",
    "toprealityskurl": "medzilaborce",
    "realityskurl": "okres-medzilaborce"
  },
  {
    "id": 37,
    "name": "Michalovce",
    "veh_reg_num": "MI",
    "code": 807,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-michalovce",
    "toprealityskurl": "michalovce",
    "realityskurl": "okres-michalovce"
  },
  {
    "id": 38,
    "name": "Myjava",
    "veh_reg_num": "MY",
    "code": 303,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-myjava",
    "toprealityskurl": "myjava",
    "realityskurl": "okres-myjava"
  },
  {
    "id": 39,
    "name": "Námestovo",
    "veh_reg_num": "NO",
    "code": 507,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-namestovo",
    "toprealityskurl": "namestovo",
    "realityskurl": "okres-namestovo"
  },
  {
    "id": 40,
    "name": "Nitra",
    "veh_reg_num": "NR",
    "code": 403,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-nitra",
    "toprealityskurl": "nitra",
    "realityskurl": "okres-nitra"
  },
  {
    "id": 41,
    "name": "Nové Mesto nad Váhom",
    "veh_reg_num": "NM",
    "code": 304,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-nove-mesto-nad-vahom",
    "toprealityskurl": "nove-mesto-nad-vahom",
    "realityskurl": "okres-nove-mesto-nad-vahom"
  },
  {
    "id": 42,
    "name": "Nové Zámky",
    "veh_reg_num": "NZ",
    "code": 404,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-nove-zamky",
    "toprealityskurl": "nove-zamky",
    "realityskurl": "okres-nove-zamky"
  },
  {
    "id": 43,
    "name": "Partizánske",
    "veh_reg_num": "PE",
    "code": 305,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-partizanske",
    "toprealityskurl": "partizanske",
    "realityskurl": "okres-partizanske"
  },
  {
    "id": 44,
    "name": "Pezinok",
    "veh_reg_num": "PK",
    "code": 107,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-pezinok",
    "toprealityskurl": "pezinok",
    "realityskurl": "okres-pezinok"
  },
  {
    "id": 45,
    "name": "Piešťany",
    "veh_reg_num": "PN",
    "code": 204,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-piestany",
    "toprealityskurl": "piestany",
    "realityskurl": "okres-piestany"
  },
  {
    "id": 46,
    "name": "Poltár",
    "veh_reg_num": "PT",
    "code": 607,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-poltar",
    "toprealityskurl": "poltar",
    "realityskurl": "okres-poltar"
  },
  {
    "id": 47,
    "name": "Poprad",
    "veh_reg_num": "PP",
    "code": 706,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-poprad",
    "toprealityskurl": "poprad",
    "realityskurl": "okres-poprad"
  },
  {
    "id": 48,
    "name": "Považská Bystrica",
    "veh_reg_num": "PB",
    "code": 306,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-povazska-bystrica",
    "toprealityskurl": "povazska-bystrica",
    "realityskurl": "okres-povazska-bystrica"
  },
  {
    "id": 49,
    "name": "Prešov",
    "veh_reg_num": "PO",
    "code": 707,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-presov",
    "toprealityskurl": "presov",
    "realityskurl": "okres-presov"
  },
  {
    "id": 50,
    "name": "Prievidza",
    "veh_reg_num": "PD",
    "code": 307,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-prievidza",
    "toprealityskurl": "prievidza",
    "realityskurl": "okres-prievidza"
  },
  {
    "id": 51,
    "name": "Púchov",
    "veh_reg_num": "PU",
    "code": 308,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-puchov",
    "toprealityskurl": "puchov",
    "realityskurl": "okres-puchov"
  },
  {
    "id": 52,
    "name": "Revúca",
    "veh_reg_num": "RA",
    "code": 608,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-revuca",
    "toprealityskurl": "revuca",
    "realityskurl": "okres-revuca"
  },
  {
    "id": 53,
    "name": "Rimavská Sobota",
    "veh_reg_num": "RS",
    "code": 609,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-rimavska-sobota",
    "toprealityskurl": "rimavska-sobota",
    "realityskurl": "okres-rimavska-sobota"
  },
  {
    "id": 54,
    "name": "Rožňava",
    "veh_reg_num": "RV",
    "code": 808,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-roznava",
    "toprealityskurl": "roznava",
    "realityskurl": "okres-roznava"
  },
  {
    "id": 55,
    "name": "Ružomberok",
    "veh_reg_num": "RK",
    "code": 508,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-ruzomberok",
    "toprealityskurl": "ruzomberok",
    "realityskurl": "okres-ruzomberok"
  },
  {
    "id": 56,
    "name": "Sabinov",
    "veh_reg_num": "SB",
    "code": 708,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-sabinov",
    "toprealityskurl": "sabinov",
    "realityskurl": "okres-sabinov"
  },
  {
    "id": 57,
    "name": "Senec",
    "veh_reg_num": "SC",
    "code": 108,
    "region_id": 2,
    "nehnutelnostiskurl": "okres-senec",
    "toprealityskurl": "senec",
    "realityskurl": "okres-senec"
  },
  {
    "id": 58,
    "name": "Senica",
    "veh_reg_num": "SE",
    "code": 205,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-senica",
    "toprealityskurl": "senica",
    "realityskurl": "okres-senica"
  },
  {
    "id": 59,
    "name": "Skalica",
    "veh_reg_num": "SI",
    "code": 206,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-skalica",
    "toprealityskurl": "skalica",
    "realityskurl": "okres-skalica"
  },
  {
    "id": 60,
    "name": "Snina",
    "veh_reg_num": "SV",
    "code": 709,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-snina",
    "toprealityskurl": "snina",
    "realityskurl": "okres-snina"
  },
  {
    "id": 61,
    "name": "Sobrance",
    "veh_reg_num": "SO",
    "code": 809,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-sobrance",
    "toprealityskurl": "sobrance",
    "realityskurl": "okres-sobrance"
  },
  {
    "id": 62,
    "name": "Spišská Nová Ves",
    "veh_reg_num": "SN",
    "code": 810,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-spisska-nova-ves",
    "toprealityskurl": "spisska-nova-ves",
    "realityskurl": "okres-spisska-nova-ves"
  },
  {
    "id": 63,
    "name": "Stará Ľubovňa",
    "veh_reg_num": "SL",
    "code": 710,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-stara-lubovna",
    "toprealityskurl": "stara-lubovna",
    "realityskurl": "okres-stara-lubovna"
  },
  {
    "id": 64,
    "name": "Stropkov",
    "veh_reg_num": "SP",
    "code": 711,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-stropkov",
    "toprealityskurl": "stropkov",
    "realityskurl": "okres-stropkov"
  },
  {
    "id": 65,
    "name": "Svidník",
    "veh_reg_num": "SK",
    "code": 712,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-svidnik",
    "toprealityskurl": "svidnik",
    "realityskurl": "okres-svidnik"
  },
  {
    "id": 66,
    "name": "Šaľa",
    "veh_reg_num": "SA",
    "code": 405,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-sala",
    "toprealityskurl": "sala",
    "realityskurl": "okres-sala"
  },
  {
    "id": 67,
    "name": "Topoľčany",
    "veh_reg_num": "TO",
    "code": 406,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-topolcany",
    "toprealityskurl": "topolcany",
    "realityskurl": "okres-topolcany"
  },
  {
    "id": 68,
    "name": "Trebišov",
    "veh_reg_num": "TV",
    "code": 811,
    "region_id": 3,
    "nehnutelnostiskurl": "okres-trebisov",
    "toprealityskurl": "trebisov",
    "realityskurl": "okres-trebisov"
  },
  {
    "id": 69,
    "name": "Trenčín",
    "veh_reg_num": "TN",
    "code": 309,
    "region_id": 6,
    "nehnutelnostiskurl": "okres-trencin",
    "toprealityskurl": "trencin",
    "realityskurl": "okres-trencin"
  },
  {
    "id": 70,
    "name": "Trnava",
    "veh_reg_num": "TT",
    "code": 207,
    "region_id": 7,
    "nehnutelnostiskurl": "okres-trnava",
    "toprealityskurl": "trnava",
    "realityskurl": "okres-trnava"
  },
  {
    "id": 71,
    "name": "Turčianske Teplice",
    "veh_reg_num": "TR",
    "code": 509,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-turcianske-teplice",
    "toprealityskurl": "turcianske-teplice",
    "realityskurl": "okres-turcianske-teplice"
  },
  {
    "id": 72,
    "name": "Tvrdošín",
    "veh_reg_num": "TS",
    "code": 510,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-tvrdosin",
    "toprealityskurl": "tvrdosin",
    "realityskurl": "okres-tvrdosin"
  },
  {
    "id": 73,
    "name": "Veľký Krtíš",
    "veh_reg_num": "VK",
    "code": 610,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-velky-krtis",
    "toprealityskurl": "velky-krtis",
    "realityskurl": "okres-velky-krtis"
  },
  {
    "id": 74,
    "name": "Vranov nad Topľou",
    "veh_reg_num": "VT",
    "code": 713,
    "region_id": 5,
    "nehnutelnostiskurl": "okres-vranov-nad-toplou",
    "toprealityskurl": "vranov-nad-toplou",
    "realityskurl": "okres-vranov-nad-toplou"
  },
  {
    "id": 75,
    "name": "Zlaté Moravce",
    "veh_reg_num": "ZM",
    "code": 407,
    "region_id": 4,
    "nehnutelnostiskurl": "okres-zlate-moravce",
    "toprealityskurl": "zlate-moravce",
    "realityskurl": "okres-zlate-moravce"
  },
  {
    "id": 76,
    "name": "Zvolen",
    "veh_reg_num": "ZV",
    "code": 611,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-zvolen",
    "toprealityskurl": "zvolen",
    "realityskurl": "okres-zvolen"
  },
  {
    "id": 77,
    "name": "Žarnovica",
    "veh_reg_num": "ZC",
    "code": 612,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-zarnovica",
    "toprealityskurl": "zarnovica",
    "realityskurl": "okres-zarnovica"
  },
  {
    "id": 78,
    "name": "Žiar nad Hronom",
    "veh_reg_num": "ZH",
    "code": 613,
    "region_id": 1,
    "nehnutelnostiskurl": "okres-ziar-nad-hronom",
    "toprealityskurl": "ziar-nad-hronom",
    "realityskurl": "okres-ziar-nad-hronom"
  },
  {
    "id": 79,
    "name": "Žilina",
    "veh_reg_num": "ZA",
    "code": 511,
    "region_id": 8,
    "nehnutelnostiskurl": "okres-zilina",
    "toprealityskurl": "zilina",
    "realityskurl": "okres-zilina"
  }
]
'''
regions_json = '''
[
	{
		"id": 1,
		"name": "Banskobystrický kraj",
		"shortcut": "BC"
	},
	{
		"id": 2,
		"name": "Bratislavský kraj",
		"shortcut": "BL"
	},
	{
		"id": 3,
		"name": "Košický kraj",
		"shortcut": "KI"
	},
	{
		"id": 4,
		"name": "Nitriansky kraj",
		"shortcut": "NI"
	},
	{
		"id": 5,
		"name": "Prešovský kraj",
		"shortcut": "PV"
	},
	{
		"id": 6,
		"name": "Trenčiansky kraj",
		"shortcut": "TC"
	},
	{
		"id": 7,
		"name": "Trnavský kraj",
		"shortcut": "TA"
	},
	{
		"id": 8,
		"name": "Žilinský kraj",
		"shortcut": "ZI"
	}
]
'''


def get_cities():
    regions_data = json.loads(regions_json)
    districts_data = json.loads(district_json)

    region_districts_mapping = {}

    for district in districts_data:
        region_id = district['region_id']
        region_name = next((region['name'] for region in regions_data if region['id'] == region_id), "Unknown Region")
        district_record = {
            'name': district['name'],
            'nehnutelnostiskurl': district['nehnutelnostiskurl'],
            'toprealityskurl': district['toprealityskurl'],
            'realityskurl': district['realityskurl']
        }

        region_districts_mapping.setdefault(region_name, []).append(district_record)

    for region_name, cities in region_districts_mapping.items():
        region_districts_mapping[region_name] = sorted(cities, key=lambda x: x['name'])

    return dict(sorted(region_districts_mapping.items()))
