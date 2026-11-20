from scripts.make_samples.iban import italian_iban
from scripts.make_samples.specs import Supplier

BUYER = [
    "Sila Roasting Co.",
    "Via Rossini 18",
    "87036 Rende (CS), Italy",
    "VAT IT03817450789",
]

ALTURA = Supplier(
    key="altura",
    name="Altura Green Coffee S.r.l.",
    vat="IT02294710325",
    address=["Riva del Mandracchio 4", "34124 Trieste (TS), Italy"],
    iban=italian_iban("X", "03069", "02233", "100000041872"),
    layout="altura",
)

IMBALLI = Supplier(
    key="imballi",
    name="Imballi Calabri S.n.c.",
    vat="IT01968230798",
    address=["Zona Industriale Lotto 22", "88046 Lamezia Terme (CZ), Italia"],
    iban=italian_iban("K", "05387", "42840", "000003318920"),
    layout="imballi",
    lang="it",
)

SPEEDLINE = Supplier(
    key="speedline",
    name="SpeedLine Logistics S.p.A.",
    vat="IT07731520963",
    address=["Via dell'Industria 61", "20037 Paderno Dugnano (MI), Italy"],
    iban=italian_iban("B", "02008", "33250", "000105562210"),
    layout="speedline",
)

BRUNO = Supplier(
    key="bruno",
    name="Bruno Espresso Service",
    vat="IT03550120784",
    address=["Corso Mazzini 140", "87100 Cosenza (CS), Italy"],
    iban=italian_iban("Q", "01030", "16200", "000000772415"),
    layout="bruno",
)

ENERGIA = Supplier(
    key="energia",
    name="Energia Sud S.p.A.",
    vat="IT05102840631",
    address=["Centro Direzionale Isola G1", "80143 Napoli (NA), Italy"],
    iban=italian_iban("M", "03111", "03400", "000000058391"),
    layout="energia",
)

PULITO = Supplier(
    key="pulito",
    name="Pulito Pro Servizi",
    vat="IT03971180786",
    address=["Via Kennedy 52", "87036 Rende (CS), Italy"],
    iban=italian_iban("T", "08887", "80880", "000000214406"),
    layout="pulito",
)