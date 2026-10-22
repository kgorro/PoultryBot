"""Bilingual poultry lexicon: Cebuano (ceb) and Tagalog (tl) lemmas mapped to English concept tokens.

Each entry: lemma -> (language, [English gloss tokens]). Glosses match the vocabulary of the knowledge base so
that projected queries land on the right entries. Lemmas are base forms; affixed forms (mangitlog, gipakaon,
bumili) are reduced to these by dalan.normalize.

Loanwords that English-speaking farmers also use (balut, penoy, darak, broiler) are left out on purpose, so
they do not inflate the code-switch index of English queries. Extend this list from real user logs.
"""

LEXICON = {
    # ------------------------------------------------ question and function words
    "unsa": ("ceb", ["what"]), "unsaon": ("ceb", ["how"]), "giunsa": ("ceb", ["how"]),
    "asa": ("ceb", ["where"]), "diin": ("ceb", ["where"]), "kinsa": ("ceb", ["who"]),
    "pila": ("ceb", ["how", "many", "much"]), "kanusa": ("ceb", ["when"]), "ngano": ("ceb", ["why"]),
    "naa": ("ceb", ["there"]), "wala": ("ceb", ["not"]), "dili": ("ceb", ["not"]),
    "paano": ("tl", ["how"]), "saan": ("tl", ["where"]), "magkano": ("tl", ["how", "much", "cost"]),
    "kailan": ("tl", ["when"]), "ano": ("tl", ["what"]), "bakit": ("tl", ["why"]), "ilan": ("tl", ["how", "many"]),
    "mayroon": ("tl", ["there"]), "meron": ("tl", ["there"]), "hindi": ("tl", ["not"]), "ayaw": ("ceb", ["not", "stopped"]),
    "kinahanglan": ("ceb", ["need"]), "kailangan": ("tl", ["need"]), "angay": ("ceb", ["should"]), "dapat": ("tl", ["should"]),
    "kasagaran": ("ceb", ["common"]), "karaniwan": ("tl", ["common"]),
    # ------------------------------------------------ birds
    "manok": ("ceb", ["chicken"]), "piso": ("ceb", ["chick"]), "sisiw": ("tl", ["chick"]),
    "himungaan": ("ceb", ["hen", "layer", "laying"]), "inahin": ("tl", ["hen", "layer"]),
    "sunoy": ("ceb", ["rooster"]), "tandang": ("tl", ["rooster"]), "dumalaga": ("tl", ["pullet", "layer"]),
    "bisaya": ("ceb", ["native"]), "katutubo": ("tl", ["native"]), "lokal": ("ceb", ["local", "native"]),
    "pabo": ("ceb", ["turkey"]), "gansa": ("ceb", ["goose"]), "lahi": ("ceb", ["breed"]), "klase": ("ceb", ["kind", "type"]),
    # ------------------------------------------------ eggs and laying
    "itlog": ("ceb", ["egg", "laying"]), "pangitlog": ("ceb", ["laying", "egg", "production"]),
    "nangingitlog": ("tl", ["laying", "egg"]), "nangitlog": ("ceb", ["laying", "egg"]),
    "panit": ("ceb", ["shell"]), "balat": ("tl", ["shell"]), "nipis": ("ceb", ["thin"]), "manipis": ("tl", ["thin"]),
    "humok": ("ceb", ["soft"]), "malambot": ("tl", ["soft"]), "buak": ("ceb", ["broken", "cracked"]),
    "basag": ("tl", ["broken", "cracked"]), "gamay": ("ceb", ["small"]), "maliit": ("tl", ["small"]),
    "dako": ("ceb", ["large"]), "malaki": ("tl", ["large"]), "pula": ("ceb", ["yolk"]),
    "lumlum": ("ceb", ["broody", "incubate", "sitting"]), "limlim": ("tl", ["broody", "incubate", "sitting"]),
    "pisa": ("ceb", ["hatch"]), "pumisa": ("tl", ["hatch"]), "inkubeytor": ("ceb", ["incubator"]),
    "kandila": ("ceb", ["candling"]), "tuka": ("ceb", ["peck", "pecking"]),
    # ------------------------------------------------ housing and environment
    "tangkal": ("ceb", ["coop"]), "kulungan": ("tl", ["coop", "cage"]),
    "hawla": ("tl", ["cage"]), "balay": ("ceb", ["house"]), "bahay": ("tl", ["house"]),
    "atop": ("ceb", ["roof"]), "bubong": ("tl", ["roof"]), "salog": ("ceb", ["floor"]), "sahig": ("tl", ["floor"]),
    "upa": ("ceb", ["rice hull", "litter"]), "ipa": ("tl", ["rice hull", "litter"]),
    "hangin": ("ceb", ["air", "ventilation"]), "suga": ("ceb", ["light", "lighting"]), "ilaw": ("tl", ["light", "lighting"]),
    "bombilya": ("ceb", ["bulb", "light"]), "init": ("ceb", ["heat", "hot"]), "kainit": ("ceb", ["heat", "hot"]),
    "painit": ("ceb", ["heat", "brooding"]), "tugnaw": ("ceb", ["cold"]), "bugnaw": ("ceb", ["cold"]), "pabugnaw": ("ceb", ["cool"]), "palamig": ("tl", ["cool"]),
    "lamig": ("tl", ["cold"]), "ginaw": ("tl", ["cold"]), "basa": ("ceb", ["wet"]), "uga": ("ceb", ["dry"]),
    "baho": ("ceb", ["smell", "ammonia"]), "langaw": ("ceb", ["flies"]), "hugaw": ("ceb", ["dirty", "manure"]),
    "dumi": ("tl", ["dirty", "manure", "droppings"]), "abono": ("ceb", ["fertilizer", "manure"]),
    "lapok": ("ceb", ["dirty"]), "puwang": ("ceb", ["space"]), "luwag": ("tl", ["space"]), "hutok": ("ceb", ["crowding"]),
    "gawas": ("ceb", ["outdoor", "range"]), "labas": ("tl", ["outdoor", "range"]), "buhian": ("ceb", ["free range", "roam"]),
    "sagbot": ("ceb", ["grass", "forage"]), "damo": ("tl", ["grass", "forage"]),
    # ------------------------------------------------ predators
    "ilaga": ("ceb", ["rat", "rats"]), "daga": ("tl", ["rat", "rats"]), "bitin": ("ceb", ["snake"]), "ahas": ("tl", ["snake"]),
    "iro": ("ceb", ["dog"]), "aso": ("tl", ["dog"]), "iring": ("ceb", ["cat"]), "pusa": ("tl", ["cat"]),
    "banog": ("ceb", ["hawk"]), "lawin": ("tl", ["hawk"]), "kawatan": ("ceb", ["stolen"]), "magnanakaw": ("tl", ["stolen"]),
    # ------------------------------------------------ feed and water
    "pakaon": ("ceb", ["feed", "feeding"]), "pakain": ("tl", ["feed", "feeding"]), "patuka": ("tl", ["feed"]),
    "kaon": ("ceb", ["eat", "feed"]), "pagkaon": ("ceb", ["feed", "food"]), "kain": ("tl", ["eat", "feed"]),
    "pagkain": ("tl", ["feed", "food"]), "tahop": ("ceb", ["rice bran"]), "mais": ("ceb", ["corn"]),
    "tubig": ("ceb", ["water"]), "inom": ("ceb", ["drink", "water"]), "imnon": ("ceb", ["drink", "water"]),
    "imnanan": ("ceb", ["drinker"]), "sako": ("ceb", ["sack"]), "tipig": ("ceb", ["store", "storage"]),
    "tago": ("tl", ["store", "storage"]), "agup-op": ("ceb", ["mold", "moldy"]), "amag": ("tl", ["mold", "moldy"]),
    "inaamag": ("tl", ["moldy"]), "dunot": ("ceb", ["spoiled"]), "bulok": ("tl", ["spoiled"]),
    "barato": ("ceb", ["cheap"]), "mura": ("tl", ["cheap"]), "mahal": ("ceb", ["expensive"]),
    "gasto": ("ceb", ["cost", "expenses"]), "gastos": ("tl", ["cost", "expenses"]), "presyo": ("ceb", ["price", "cost"]),
    "makatipid": ("tl", ["save", "reduce"]), "makadaginot": ("ceb", ["save", "reduce"]), "daginot": ("ceb", ["save"]),
    "usik": ("ceb", ["waste", "wastage"]), "sayang": ("tl", ["waste", "wastage"]),
    # ------------------------------------------------ health
    "sakit": ("ceb", ["disease", "sick"]), "masakiton": ("ceb", ["sick"]), "may-sakit": ("tl", ["sick"]),
    "patay": ("ceb", ["dead", "death"]), "matay": ("ceb", ["dying", "dead"]), "mamatay": ("tl", ["dying", "dead"]),
    "namamatay": ("tl", ["dying", "dead"]), "mangamatay": ("ceb", ["dying", "dead", "many"]),
    "kalit": ("ceb", ["sudden"]), "bigla": ("tl", ["sudden"]), "daghan": ("ceb", ["many"]), "marami": ("tl", ["many"]),
    "kalibang": ("ceb", ["diarrhea", "droppings"]), "kalibanga": ("ceb", ["diarrhea", "droppings"]),
    "pagtatae": ("tl", ["diarrhea"]), "nagtatae": ("tl", ["diarrhea"]), "tae": ("ceb", ["droppings", "poop"]),
    "iti": ("ceb", ["droppings", "poop"]), "dugo": ("ceb", ["blood", "bloody"]), "lunhaw": ("ceb", ["green"]),
    "berde": ("ceb", ["green"]), "puti": ("ceb", ["white"]),
    "ubo": ("ceb", ["cough", "coughing"]), "inuubo": ("tl", ["cough", "coughing"]),
    "sipon": ("ceb", ["colds", "runny nose", "nasal discharge"]), "singa": ("ceb", ["nasal discharge"]),
    "ginhawa": ("ceb", ["breathing"]), "hinga": ("tl", ["breathing"]), "hingak": ("ceb", ["panting"]),
    "hingal": ("tl", ["panting"]), "hubag": ("ceb", ["swollen"]), "maga": ("tl", ["swollen"]),
    "namamaga": ("tl", ["swollen"]), "pamamaga": ("tl", ["swollen"]),
    "nawong": ("ceb", ["face"]), "mukha": ("tl", ["face"]), "mata": ("ceb", ["eyes"]), "ulo": ("ceb", ["head"]),
    "liog": ("ceb", ["neck", "twisted neck"]), "leeg": ("tl", ["neck", "twisted neck"]),
    "kiwi": ("ceb", ["twisted"]), "baluktot": ("tl", ["twisted"]), "pilay": ("ceb", ["paralysis", "lame"]),
    "lupay": ("ceb", ["weak"]), "luya": ("ceb", ["weak"]), "mahina": ("tl", ["weak"]),
    "bulutong": ("ceb", ["pox", "fowl pox"]), "butlig": ("ceb", ["bumps", "scabs"]), "nuka": ("ceb", ["lesions", "scabs"]),
    "bitok": ("ceb", ["worms", "deworm"]), "bulate": ("tl", ["worms", "deworm"]), "ulod": ("ceb", ["worms", "larvae"]),
    "hanip": ("ceb", ["mites"]), "kuto": ("ceb", ["lice"]), "katol": ("ceb", ["itching"]), "kati": ("tl", ["itching"]),
    "balhibo": ("ceb", ["feathers"]), "balahibo": ("tl", ["feathers"]), "lagas": ("ceb", ["falling", "losing"]),
    "kalbo": ("ceb", ["bald"]), "bakuna": ("ceb", ["vaccine", "vaccination"]),
    "tambal": ("ceb", ["medicine", "treatment"]), "gamot": ("tl", ["medicine", "treatment"]),
    "antibayotik": ("ceb", ["antibiotic"]), "bitamina": ("ceb", ["vitamin"]),
    "peste": ("ceb", ["newcastle", "outbreak"]), "trangkaso": ("ceb", ["influenza", "flu"]),
    "beterinaryo": ("ceb", ["veterinarian", "vet"]), "doktor": ("ceb", ["veterinarian", "doctor"]),
    "tabang": ("ceb", ["help"]), "tulong": ("tl", ["help"]), "pangayo": ("ceb", ["ask", "help"]), "ireport": ("ceb", ["report"]),
    "lubong": ("ceb", ["bury", "dispose"]), "libing": ("tl", ["bury", "dispose"]), "sunog": ("ceb", ["burn"]),
    "labay": ("ceb", ["throw", "dispose"]), "tapon": ("tl", ["throw", "dispose"]),
    # ------------------------------------------------ raising, growth, age
    "buhi": ("ceb", ["raise", "raising", "alive", "fertile"]), "alaga": ("tl", ["raise", "raising"]), "alima": ("ceb", ["care", "raise"]),
    "atiman": ("ceb", ["care"]), "sugod": ("ceb", ["start", "begin"]), "simula": ("tl", ["start", "begin"]),
    "tubo": ("ceb", ["grow", "growth"]), "laki": ("tl", ["grow", "growth"]), "timbang": ("ceb", ["weight"]),
    "bug-at": ("ceb", ["weight", "heavy"]), "paspas": ("ceb", ["fast"]), "mabilis": ("tl", ["fast"]),
    "hinay": ("ceb", ["slow"]), "mabagal": ("tl", ["slow"]), "edad": ("ceb", ["age", "old"]),
    "tigulang": ("ceb", ["old"]), "matanda": ("tl", ["old"]), "bata": ("ceb", ["young"]),
    "adlaw": ("ceb", ["day", "days"]), "araw": ("tl", ["day", "days"]), "semana": ("ceb", ["week", "weeks"]),
    "linggo": ("tl", ["week", "weeks"]), "bulan": ("ceb", ["month"]), "buwan": ("tl", ["month"]),
    "tuig": ("ceb", ["year"]), "taon": ("tl", ["year"]), "oras": ("ceb", ["hours"]),
    "gabii": ("ceb", ["night"]), "gabi": ("tl", ["night"]), "buntag": ("ceb", ["morning"]), "umaga": ("tl", ["morning"]),
    # ------------------------------------------------ processing and food safety
    "karne": ("ceb", ["meat"]), "unod": ("ceb", ["meat"]), "ihaw": ("ceb", ["slaughter", "dress"]),
    "katay": ("tl", ["slaughter", "dress"]), "limpyo": ("ceb", ["clean"]), "linis": ("tl", ["clean"]),
    "hugas": ("ceb", ["wash", "washing"]), "tipiganan": ("ceb", ["storage"]), "presko": ("ceb", ["fresh"]),
    "sariwa": ("tl", ["fresh"]), "luwas": ("ceb", ["safe"]), "ligtas": ("tl", ["safe"]),
    # ------------------------------------------------ business
    "negosyo": ("ceb", ["business"]), "puhunan": ("tl", ["capital", "cost"]), "puhonan": ("ceb", ["capital", "cost"]),
    "kapital": ("ceb", ["capital"]), "ganansya": ("ceb", ["profit"]), "ganansiya": ("ceb", ["profit"]),
"kwarta": ("ceb", ["money"]), "kuwarta": ("ceb", ["money"]), "pera": ("tl", ["money"]),
    "baligya": ("ceb", ["sell", "selling"]), "benta": ("ceb", ["sell", "selling"]), "palit": ("ceb", ["buy"]),
    "bili": ("tl", ["buy"]), "pumapalit": ("ceb", ["buyers"]), "mamalitay": ("ceb", ["buyers"]),
    "merkado": ("ceb", ["market"]), "palengke": ("tl", ["market"]), "permiso": ("ceb", ["permit"]),
    "lisensya": ("ceb", ["license", "permit"]), "rehistro": ("ceb", ["registration", "register"]),
    "listahan": ("tl", ["records"]), "rekord": ("ceb", ["records"]), "kompanya": ("ceb", ["company"]),
    "kontrata": ("ceb", ["contract"]),
    # ------------------------------------------------ common verbs (roots)
    "sulat": ("ceb", ["write", "records"]), "andam": ("ceb", ["prepare"]), "handa": ("tl", ["prepare"]),
    "abot": ("ceb", ["arrive", "arrival"]), "dating": ("tl", ["arrive", "arrival"]), "pundok": ("ceb", ["huddle", "crowding under"]),
    "nagkukumpulan": ("tl", ["huddle"]), "ilawom": ("ceb", ["under"]), "ilalim": ("tl", ["under"]),
    "kunhod": ("ceb", ["drop", "decrease", "low"]), "bawas": ("tl", ["drop", "decrease"]), "baba": ("tl", ["drop", "low"]),
    "ila": ("ceb", ["identify", "tell"]), "kilala": ("tl", ["identify", "tell"]), "kuha": ("ceb", ["remove"]), "wagtang": ("ceb", ["remove", "get rid"]), "mawala": ("tl", ["remove", "get rid"]),
    "likay": ("ceb", ["prevent", "avoid"]), "iwas": ("tl", ["prevent", "avoid"]), "sagol": ("ceb", ["mix"]),
    "halo": ("tl", ["mix"]), "hatag": ("ceb", ["give"]), "bigay": ("tl", ["give"]), "hibalo": ("ceb", ["know", "check"]),
    "alam": ("tl", ["know", "check"]), "sulod": ("ceb", ["into", "enter"]), "pasok": ("tl", ["into", "enter"]),
    "gagmay": ("ceb", ["small"]), "bago": ("tl", ["new", "newly"]), "bag-o": ("ceb", ["new", "newly"]),
    "ilang": ("tl", ["how", "many"]), "gaano": ("tl", ["how", "much"]), "iniinom": ("tl", ["drink", "water"]),
    "purga": ("ceb", ["deworm"]), "ani": ("ceb", ["harvest"]), "hulog": ("ceb", ["drop"]),
    # ------------------------------------------------ greetings
    "maayong": ("ceb", ["hello", "good"]), "kumusta": ("ceb", ["hello"]), "kamusta": ("ceb", ["hello"]),
    "magandang": ("tl", ["hello", "good"]), "salamat": ("ceb", ["thank"]),
    "maayo": ("ceb", ["good", "best"]), "nindot": ("ceb", ["best", "good"]), "maganda": ("tl", ["best", "good"]),
}
# Left out on purpose: "kita" (Cebuano "we" but Tagalog "income") and "baboy" (pig, out of scope).

# Clitic and contracted forms common in chat Cebuano/Tagalog -> expansion ("" drops the word)
CONTRACTIONS = {
    "unsay": "unsa ang", "asay": "asa ang", "pilay": "pila ang", "kinsay": "kinsa ang", "naay": "naa ang",
    "asang": "asa ang", "unsang": "unsa ang", "pilang": "pila ang", "nganong": "ngano ang", "diay": "", "man": "",
    "ba": "", "og": "ug", "nga": "", "ang": "", "ug": "", "sa": "", "si": "", "ni": "", "ko": "", "mo": "", "ka": "",
    "ta": "", "kami": "", "mi": "", "nako": "", "akong": "", "imong": "", "ako": "", "mga": "", "ng": "", "na": "",
    "po": "", "lang": "", "pa": "", "ra": "", "kaayo": "", "kung": "", "kapag": "", "pwede": "", "puwede": "", "ilang": "ilang", "kini": "", "kana": "", "ito": "", "yung": "",
    "yong": "", "ang mga": "", "nila": "", "ila": "", "iyang": "", "aking": "", "mag": "", "kay": "",
    "para": "", "for": "", "pano": "paano", "nasaan": "saan", "asan": "asa", "hain": "asa", "aha": "asa", "nganu": "ngano",
}

PREFIXES = ["makakapag", "makaka", "maipa", "mai", "makapang", "makapag", "makapa", "pagpa", "gina", "nagpa", "mi", "makig", "maka", "magpa", "mag", "nag", "nang", "mang", "man", "pag", "gipa",
            "gi", "ma", "na", "mo", "ni", "ka", "pa", "i", "pinaka", "pang", "nanga", "manga"]
SUFFIXES = ["anan", "hanan", "han", "hon", "ng", "an", "on", "in", "a"]
