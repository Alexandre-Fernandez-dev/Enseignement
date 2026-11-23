#!/usr/bin/env python3
"""Lit les progressions annuelles : la copie du dépôt et, en lecture seule, le classeur du Drive.

Pour chaque niveau, deux classeurs :
- dans le dépôt, <niveau>/progression.xlsx : la copie tenue à jour avec Claude (chapitres,
  décisions de progression) ;
- sur le Drive : le classeur Google Sheets que l'enseignant remplit au fil des séances (cahier de
  textes, liens des questions flash) ; c'est lui qui fait foi pour les séances. Les anciens .xlsx
  du même nom, rangés dans old/, sont des archives et ne sont pas lus. Il a normalement les mêmes colonnes que le dépôt ; si une colonne
  manque ou a été ajoutée, le décalage est repéré grâce aux en-têtes de la ligne 1 et signalé.

Accès au Drive en lecture seule : un compte de service Google, avec qui seuls ces deux classeurs
sont partagés, en « Lecteur ». Il ne voit rien d'autre du Drive et Google lui refuse toute
modification ; le script ne demande d'ailleurs que la portée drive.readonly.
Clé du compte de service (fichier JSON), cherchée dans cet ordre :
1. variable d'environnement GOOGLE_COMPTE_SERVICE : le contenu du JSON, brut ou en base64
   (session cloud : variables d'environnement de l'environnement cloud, sur claude.ai/code) ;
2. fichier ~/.config/lycee/compte-service.json (ordinateur).
Sans clé, ou si le Drive ne répond pas, seule la copie du dépôt est lue, et les scripts le disent.

Mise en place (une fois), sur console.cloud.google.com, avec le compte Google du Drive :
1. créer un projet, puis y activer « Google Drive API » (API et services > Bibliothèque) ;
2. IAM et administration > Comptes de service > Créer un compte de service, sans aucun rôle ;
3. sur ce compte : Clés > Ajouter une clé > Créer une clé > JSON ; ranger le fichier téléchargé
   dans ~/.config/lycee/compte-service.json (chmod 600) ;
4. dans Google Drive, partager les deux classeurs Google Sheets (pas leurs dossiers) avec l'adresse du compte
   (…@….iam.gserviceaccount.com), en « Lecteur », sans envoyer de notification ;
5. vérifier : python3 scripts/progressions.py verifier ;
6. pour le cloud : base64 -w0 ~/.config/lycee/compte-service.json | wl-copy, puis coller la
   valeur dans une variable GOOGLE_COMPTE_SERVICE de l'environnement cloud.
Révoquer l'accès : supprimer la clé dans la console, ou retirer le partage des classeurs.

N'utilise que la bibliothèque standard de Python (signature RSA comprise), pour fonctionner
aussi dans une session cloud.

Usage (depuis la racine du dépôt) :
    python3 scripts/progressions.py verifier              # teste l'accès au Drive
    python3 scripts/progressions.py comparer [16/11]      # ce que le Drive dit de différent du dépôt
    python3 scripts/progressions.py comparer 16/11 --tout # y compris les cases vides sur le Drive
    python3 scripts/progressions.py telecharger DOSSIER   # copie les classeurs du Drive dans DOSSIER
Variable PROGRESSIONS_DRIVE_DOSSIER : lire les classeurs « du Drive » dans ce dossier (copie
déjà téléchargée, sous le même nom) au lieu de les demander à Google.

Changement d'année ou de mise en page d'un classeur : mettre à jour ANNEE et NIVEAUX ci-dessous.
"""
import base64
import collections
import datetime as dt
import hashlib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

ANNEE = "2026-2027"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]

# Une ligne par semaine, la colonne A donnant le lundi. Pour chaque champ : identifiant, libellé,
# jour de la séance (None : information de la semaine), colonne (mise en page du dépôt, qui sert
# de référence), mot attendu dans l'en-tête de la ligne 1, et « remonter » : case vide = reprendre
# la dernière case remplie au-dessus (thèmes de questions flash écrits pour deux semaines,
# chapitre écrit à sa première semaine). Les en-têtes servent à repérer un classeur dont les
# colonnes sont décalées (une colonne supprimée ou ajoutée) et à le lire quand même.
Champ = collections.namedtuple("Champ", "id libelle jour col entete remonter", defaults=(None, False))

NIVEAUX = [
    {
        "nom": "Seconde",
        "depot": f"{ANNEE}/Secondes/progression.xlsx",
        "drive": "progression seconde 2026-2027 AF",  # Google Sheets (les .xlsx de old/ : archives)
        "sequences": f"{ANNEE}/Secondes/Ch */2nde_Ch*_Sequence.md",
        "champs": [
            Champ("chapitre", "Chapitre", None, "B", "cours", True),
            Champ("lundi", "Cours", "lundi", "C", "lundi"),
            Champ("fiche", "Fiche calcul (demi-groupe)", "lundi", "F", "fiche calcul"),
            Champ("fiche_detail", "Fiche calcul : détail", "lundi", "G"),
            Champ("jeudi", "Cours", "jeudi", "D", "jeudi"),
            Champ("ap", "AP (groupes de niveau)", "jeudi", "H", "AP"),
            Champ("ap_detail", "AP : détail", "jeudi", "I"),
            Champ("vendredi", "Cours", "vendredi", "E", "vendredi"),
            Champ("flash_num", "Questions flash : calcul numérique", None, "J", "flash", True),
            Champ("flash_litt", "Questions flash : calcul littéral", None, "K", None, True),
            Champ("flash_autre", "Questions flash : autre", None, "L", None, True),
        ],
    },
    {
        "nom": "1re ST2S",
        "depot": f"{ANNEE}/Premières ST2S/progression.xlsx",
        "drive": "progression 1 ST2S 2026-2027",  # Google Sheets
        "sequences": f"{ANNEE}/Premières ST2S/Ch */1ST2S_Ch*_Sequence.md",
        "champs": [
            Champ("chapitre", "Chapitre", None, "B", "cours", True),
            Champ("jeudi", "Jeudi (1 h)", "jeudi", "C", "jeudi"),
            Champ("vendredi1", "Vendredi, 1re heure", "vendredi", "D", "vendredi"),
            Champ("vendredi2", "Vendredi, 2e heure", "vendredi", "E", "vendredi"),
            Champ("flash_num", "Questions flash : calcul numérique", None, "F", "flash", True),
            Champ("flash_litt", "Questions flash : calcul littéral", None, "G", None, True),
            Champ("flash_autre", "Questions flash : autre", None, "H", None, True),
            Champ("remarques", "Remarques", None, "I", "remarques"),
        ],
    },
]


# --- Dates -------------------------------------------------------------------------------------

def _paris():
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo("Europe/Paris")
    except Exception:  # pas de base de fuseaux : heure de la machine
        return None


def aujourdhui():
    """Date du jour à Paris (une session cloud tourne souvent en UTC)."""
    return dt.datetime.now(_paris()).date()


def lire_date(arg):
    """Date depuis « aujourd'hui », « demain », « hier », 26/11, 26/11/2026 ou 2026-11-26."""
    jour = aujourdhui()
    if arg in (None, "aujourd'hui", "aujourdhui"):
        return jour
    if arg in ("demain", "hier"):
        return jour + dt.timedelta(days=1 if arg == "demain" else -1)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", arg)
    if m:
        return dt.date(int(m[1]), int(m[2]), int(m[3]))
    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})(?:/(\d{4}))?", arg)
    if m:
        j, mois = int(m[1]), int(m[2])
        if m[3]:
            return dt.date(int(m[3]), mois, j)
        debut, fin = (int(a) for a in ANNEE.split("-"))
        return dt.date(debut if mois >= 8 else fin, mois, j)
    raise SystemExit(f"Date non reconnue : {arg} (formats : 26/11, 26/11/2026, 2026-11-26, demain)")


def format_moment(moment):
    """« 22/11/2026 à 22 h 11 », heure de Paris."""
    if moment is None:
        return "date inconnue"
    paris = _paris()
    if paris and moment.tzinfo:
        moment = moment.astimezone(paris)
    return moment.strftime("%d/%m/%Y à %H h %M")


# --- Lecture d'un .xlsx avec la bibliothèque standard ---------------------------------------

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
NS_R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"


def lire_premiere_feuille(source):
    """{référence: texte} et {référence: formule} de la première feuille (chemin ou octets)."""
    z = zipfile.ZipFile(io.BytesIO(source) if isinstance(source, bytes) else source)
    partages = []
    if "xl/sharedStrings.xml" in z.namelist():
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).iter(NS + "si"):
            partages.append("".join(t.text or "" for t in si.iter(NS + "t")))
    classeur = ET.fromstring(z.read("xl/workbook.xml"))
    rid = classeur.find(NS + "sheets")[0].get(NS_R + "id")
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    cible = next(r.get("Target") for r in rels if r.get("Id") == rid)
    cible = cible[1:] if cible.startswith("/") else "xl/" + cible
    valeurs, formules = {}, {}
    for c in ET.fromstring(z.read(cible)).iter(NS + "c"):
        ref, typ = c.get("r"), c.get("t")
        f, v = c.find(NS + "f"), c.find(NS + "v")
        if f is not None and f.text:
            formules[ref] = f.text.lstrip("=")
        if typ == "s" and v is not None:
            valeurs[ref] = partages[int(v.text)]
        elif typ == "inlineStr":
            valeurs[ref] = "".join(t.text or "" for t in c.iter(NS + "t"))
        elif v is not None and v.text is not None:
            valeurs[ref] = v.text
    return valeurs, formules


def dates_des_lignes(valeurs, formules):
    """Numéro de ligne -> lundi de la semaine, d'après la colonne A : DATE(…), puis A2+7, etc."""
    dates, ligne = {}, 2
    while True:
        ref = f"A{ligne}"
        f = formules.get(ref, "").strip()
        m = re.fullmatch(r"date\((\d+),\s*(\d+),\s*(\d+)\)", f, re.I)
        n = re.fullmatch(r"A(\d+)\s*\+\s*(\d+)", f, re.I)
        if m:
            jour = dt.date(int(m[1]), int(m[2]), int(m[3]))
        elif n and int(n[1]) in dates:
            jour = dates[int(n[1])] + dt.timedelta(days=int(n[2]))
        elif re.fullmatch(r"\d+(\.0+)?", valeurs.get(ref, "")):  # date déjà calculée (numéro de série)
            jour = dt.date(1899, 12, 30) + dt.timedelta(days=int(float(valeurs[ref])))
        else:
            return dates
        dates[ligne] = jour
        ligne += 1


def _decaler(col, k):
    """Lettre de colonne décalée de k (« C », -1 -> « B ») ; None avant la colonne B."""
    n = 0
    for lettre in col:
        n = n * 26 + ord(lettre) - 64
    n += k
    if n < 2:
        return None
    lettres = ""
    while n:
        n, r = divmod(n - 1, 26)
        lettres = chr(65 + r) + lettres
    return lettres


def normaliser(texte):
    return " ".join((texte or "").split())


class Classeur:
    """Un classeur de progression (dépôt ou Drive), lu avec les colonnes de NIVEAUX."""

    def __init__(self, niveau, source, contenu, modifie=None):
        self.source, self.modifie = source, modifie
        self.valeurs, self.formules = lire_premiere_feuille(contenu)
        self.dates = dates_des_lignes(self.valeurs, self.formules)
        self.champs = {c.id: c for c in niveau["champs"]}
        self.alertes, self.colonnes = [], {}
        controles = [c for c in niveau["champs"] if c.entete]
        # Décalage des colonnes par rapport au dépôt : celui qui fait correspondre le plus d'en-têtes.
        self.decalage = max((0, -1, 1, -2, 2),
                            key=lambda k: sum(self._entete_ok(c, _decaler(c.col, k)) for c in controles))
        for c in niveau["champs"]:
            col = _decaler(c.col, self.decalage)
            if c.entete and not self._entete_ok(c, col):
                self.alertes.append(f"{source} : colonne « {c.libelle} » absente (aucun en-tête contenant "
                                    f"« {c.entete} » à sa place).")
            elif col:
                self.colonnes[c.id] = col
        if self.decalage:
            self.alertes.append(f"{source} : colonnes décalées de {self.decalage:+d} par rapport au dépôt "
                                "(une colonne supprimée ou ajoutée) ; lecture adaptée.")
        if not self.dates:
            self.alertes.append(f"{source} : colonne A sans dates (DATE(…) en A2, puis A2+7…).")

    def _entete_ok(self, champ, col):
        return bool(col) and champ.entete.lower() in (self.valeurs.get(f"{col}1") or "").lower()

    def ligne(self, lundi):
        return next((l for l, d in self.dates.items() if d == lundi), None)

    def lire(self, champ_id, lundi, remonter=True):
        """(référence, texte, lundi de la case lue) ; None si le champ ou la semaine manque."""
        col, ligne = self.colonnes.get(champ_id), self.ligne(lundi)
        if col is None or ligne is None:
            return None
        remonter = remonter and self.champs[champ_id].remonter
        for l in range(ligne, 1, -1):
            texte = (self.valeurs.get(f"{col}{l}") or "").strip()
            if texte or not remonter:
                return f"{col}{l}", texte, self.dates.get(l, lundi)
        return f"{col}{ligne}", "", lundi


# --- Drive, en lecture seule ----------------------------------------------------------------

PORTEE = "https://www.googleapis.com/auth/drive.readonly"
URL_JETON = "https://oauth2.googleapis.com/token"
URL_DRIVE = "https://www.googleapis.com/drive/v3/files"
FICHIER_CLE = os.path.expanduser("~/.config/lycee/compte-service.json")
XLSX = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
SHEETS = "application/vnd.google-apps.spreadsheet"


class DriveIndisponible(Exception):
    pass


def lire_compte_service():
    """Contenu du JSON du compte de service (dict), ou None s'il n'y a pas de clé."""
    brut = os.environ.get("GOOGLE_COMPTE_SERVICE", "").strip()
    if not brut and os.path.exists(FICHIER_CLE):
        with open(FICHIER_CLE, encoding="utf-8") as f:
            brut = f.read().strip()
    if not brut:
        return None
    try:
        if not brut.startswith("{"):
            brut = "".join(brut.split()).replace("-", "+").replace("_", "/")
            brut = base64.b64decode(brut + "=" * (-len(brut) % 4)).decode("utf-8")
        compte = json.loads(brut)
        compte["client_email"], compte["private_key"]
        return compte
    except (ValueError, KeyError, TypeError) as e:
        raise DriveIndisponible(f"clé du compte de service illisible ({type(e).__name__})") from None


def _der(octets, i=0):
    """Élément DER à la position i : (étiquette, contenu, position suivante)."""
    etiquette, n = octets[i], octets[i + 1]
    i += 2
    if n & 0x80:
        k = n & 0x7F
        n = int.from_bytes(octets[i:i + k], "big")
        i += k
    return etiquette, octets[i:i + n], i + n


def _elements(sequence):
    contenus, i = [], 0
    while i < len(sequence):
        _, contenu, i = _der(sequence, i)
        contenus.append(contenu)
    return contenus


def cle_rsa(pem):
    """(n, d) d'une clé privée RSA PEM : PKCS#8 (« PRIVATE KEY ») ou PKCS#1 (« RSA PRIVATE KEY »)."""
    lignes = [l.strip() for l in pem.strip().splitlines()]
    der = base64.b64decode("".join(l for l in lignes if l and not l.startswith("-----")))
    elements = _elements(_der(der)[1])
    if "BEGIN PRIVATE KEY" in pem:  # PKCS#8 : version, algorithme, puis la clé PKCS#1
        elements = _elements(_der(elements[2])[1])
    # PKCS#1 : version, n, e, d, p, q, …
    return int.from_bytes(elements[1], "big"), int.from_bytes(elements[3], "big")


_DIGESTINFO_SHA256 = bytes.fromhex("3031300d060960864801650304020105000420")


def signer_rs256(message, n, d):
    """Signature RSASSA-PKCS1-v1_5 avec SHA-256 (celle des jetons JWT « RS256 »)."""
    k = (n.bit_length() + 7) // 8
    t = _DIGESTINFO_SHA256 + hashlib.sha256(message).digest()
    em = b"\x00\x01" + b"\xff" * (k - len(t) - 3) + b"\x00" + t
    return pow(int.from_bytes(em, "big"), d, n).to_bytes(k, "big")


def _b64url(octets):
    return base64.urlsafe_b64encode(octets).rstrip(b"=")


def _requete(url, corps=None, jeton=None):
    hote = urllib.parse.urlsplit(url).netloc
    entetes = {"Authorization": f"Bearer {jeton}"} if jeton else {}
    if corps is not None:
        entetes["Content-Type"] = "application/x-www-form-urlencoded"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=corps, headers=entetes), timeout=30) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        detail = normaliser(e.read().decode("utf-8", "replace"))[:400]
        raise DriveIndisponible(f"erreur {e.code} de {hote} : {detail}") from None
    except (urllib.error.URLError, OSError) as e:
        raise DriveIndisponible(f"{hote} injoignable : {e}") from None


_ETAT = {"jeton": None, "erreur": None}


def jeton_acces():
    """Jeton d'accès Google (portée drive.readonly), demandé une fois par exécution."""
    if _ETAT["erreur"]:
        raise DriveIndisponible(_ETAT["erreur"])
    if _ETAT["jeton"]:
        return _ETAT["jeton"]
    try:
        compte = lire_compte_service()
        if compte is None:
            raise DriveIndisponible("pas de clé de compte de service (variable GOOGLE_COMPTE_SERVICE "
                                    "ou ~/.config/lycee/compte-service.json)")
        try:
            n, d = cle_rsa(compte["private_key"])
        except (ValueError, IndexError, TypeError):
            raise DriveIndisponible("clé privée du compte de service illisible") from None
        instant = int(time.time()) - 30
        entete = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
        charge = _b64url(json.dumps({"iss": compte["client_email"], "scope": PORTEE, "aud": URL_JETON,
                                     "iat": instant, "exp": instant + 3600}).encode())
        a_signer = entete + b"." + charge
        assertion = (a_signer + b"." + _b64url(signer_rs256(a_signer, n, d))).decode()
        corps = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                        "assertion": assertion}).encode()
        _ETAT["jeton"] = json.loads(_requete(URL_JETON, corps))["access_token"]
        return _ETAT["jeton"]
    except DriveIndisponible as e:
        _ETAT["erreur"] = str(e)
        raise


def lister(jeton, q="trashed = false"):
    """Fichiers visibles par le compte de service (seulement ceux qui lui sont partagés)."""
    champs = "files(id,name,mimeType,modifiedTime,capabilities/canEdit)"
    params = {"q": q, "fields": champs, "orderBy": "modifiedTime desc", "pageSize": "100"}
    return json.loads(_requete(URL_DRIVE + "?" + urllib.parse.urlencode(params), jeton=jeton))["files"]


def moment_drive(fichier):
    return dt.datetime.strptime(fichier["modifiedTime"][:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=dt.timezone.utc)


def lire_sur_drive(nom):
    """(octets du classeur au format xlsx, date de modification) d'un classeur du Drive."""
    dossier = os.environ.get("PROGRESSIONS_DRIVE_DOSSIER")
    if dossier:
        chemin = os.path.join(dossier, nom + ".xlsx")
        if not os.path.exists(chemin):
            raise DriveIndisponible(f"{chemin} introuvable (PROGRESSIONS_DRIVE_DOSSIER)")
        with open(chemin, "rb") as f:
            return f.read(), dt.datetime.fromtimestamp(os.path.getmtime(chemin), dt.timezone.utc)
    jeton = jeton_acces()
    nom_q = nom.replace("\\", "\\\\").replace("'", "\\'")
    fichiers = lister(jeton, f"name = '{nom_q}' and mimeType = '{SHEETS}' and trashed = false")
    if not fichiers:
        raise DriveIndisponible(f"classeur Google Sheets « {nom} » introuvable : est-il partagé avec le "
                                "compte de service (en Lecteur), et porte-t-il toujours ce nom ?")
    fichier = fichiers[0]  # exporté au format xlsx pour la lecture
    url = f"{URL_DRIVE}/{fichier['id']}/export?" + urllib.parse.urlencode({"mimeType": XLSX})
    return _requete(url, jeton=jeton), moment_drive(fichier)


def charger(niveau, drive=True):
    """(classeur du dépôt, classeur du Drive ou None, raison si le Drive n'a pas été lu)."""
    depot = Classeur(niveau, "dépôt", os.path.join(ROOT, niveau["depot"]))
    if not drive:
        return depot, None, "lecture du Drive non demandée"
    try:
        contenu, modifie = lire_sur_drive(niveau["drive"])
        return depot, Classeur(niveau, "Drive", contenu, modifie), None
    except (DriveIndisponible, zipfile.BadZipFile, KeyError, ET.ParseError) as e:
        return depot, None, str(e) or type(e).__name__


def versions(depot, drive, champ_id, lundi):
    """Ce qu'il faut afficher pour un champ : [(étiquette, texte, lundi de la case lue)].

    Une seule version si les deux classeurs disent la même chose, ou si un seul en parle ;
    les deux sinon (le Drive d'abord : c'est la saisie la plus récente)."""
    vd = depot.lire(champ_id, lundi)
    vv = drive.lire(champ_id, lundi) if drive else None
    if vv is None or (vd is not None and not vv[1] and vd[1]):
        if vd is None:
            return []
        etiquette = f"dépôt {vd[0]}" + (", rien sur le Drive" if vv is not None else "")
        return [(etiquette, vd[1], vd[2])]
    if vd is None or not vd[1]:
        return [(f"Drive {vv[0]}", vv[1], vv[2])]
    if normaliser(vv[1]) == normaliser(vd[1]):
        return [(f"Drive {vv[0]} = dépôt {vd[0]}", vv[1], vv[2])]
    return [(f"Drive {vv[0]}", vv[1], vv[2]), (f"dépôt {vd[0]}, différent", vd[1], vd[2])]


# --- Commandes ------------------------------------------------------------------------------

def verifier():
    compte = lire_compte_service()
    if compte is None:
        print(f"Pas de clé : ni variable GOOGLE_COMPTE_SERVICE, ni fichier {FICHIER_CLE}.")
        return 1
    print(f"Compte de service : {compte['client_email']}")
    jeton = jeton_acces()
    fichiers = lister(jeton)
    attendus = {niv["drive"] for niv in NIVEAUX}
    print("Fichiers qu'il voit :" if fichiers else "Il ne voit aucun fichier : partager les classeurs avec lui.")
    code = 0
    for f in fichiers:
        droit = "PEUT MODIFIER" if f.get("capabilities", {}).get("canEdit") else "lecture seule"
        print(f"- {f['name']} ({droit}, modifié le {format_moment(moment_drive(f))})")
        if droit != "lecture seule":
            print("  Attention : repartager ce classeur en « Lecteur ».")
            code = 1
    autres = [f["name"] for f in fichiers if f["name"] not in attendus]
    if autres:
        print("Attention : partages en trop, à retirer s'ils ne sont pas voulus : " + ", ".join(autres))
    for niv in NIVEAUX:
        _, drive, raison = charger(niv)
        if drive is None:
            print(f"{niv['nom']} : échec, {raison}")
            code = 1
        else:
            print(f"{niv['nom']} : lu, {len(drive.dates)} semaines.")
            for a in drive.alertes:
                print(f"  Attention : {a}")
    return code


def comparer(depuis, tout=False):
    """Cases où le Drive dit autre chose que le dépôt, semaine par semaine à partir de « depuis »."""
    lundi0 = depuis - dt.timedelta(days=depuis.weekday())
    for niv in NIVEAUX:
        depot, drive, raison = charger(niv)
        print(f"## {niv['nom']}")
        if drive is None:
            print(f"Drive non lu : {raison}\n")
            continue
        print(f"Drive : {niv['drive']}, modifié le {format_moment(drive.modifie)}. Dépôt : {niv['depot']}.")
        for a in depot.alertes + drive.alertes:
            print(f"Attention : {a}")
        communs = [c for c in niv["champs"] if c.id in depot.colonnes and c.id in drive.colonnes]
        rien = True
        for lundi in sorted(d for d in drive.dates.values() if d >= lundi0):
            ecarts = []
            for c in communs:
                vv, vd = drive.lire(c.id, lundi, remonter=False), depot.lire(c.id, lundi, remonter=False)
                tv, td = (vv[1] if vv else ""), (vd[1] if vd else "")
                if normaliser(tv) != normaliser(td) and (tv or tout):
                    jour = f" ({c.jour})" if c.libelle == "Cours" else ""
                    tv, td = (t.replace("\n", "\n    ") for t in (tv, td))
                    ecarts.append(f"- {c.libelle}{jour} : Drive {vv[0] if vv else '—'} / dépôt {vd[0] if vd else '—'}\n"
                                  f"  Drive : {tv or '(vide)'}\n  Dépôt : {td or '(vide)'}")
            if ecarts:
                rien = False
                print(f"\n### Semaine du {lundi.strftime('%d/%m')}")
                print("\n".join(ecarts))
        print("\nAucune différence." if rien else "")
        print()


def telecharger(dossier):
    os.makedirs(dossier, exist_ok=True)
    for niv in NIVEAUX:
        contenu, modifie = lire_sur_drive(niv["drive"])
        chemin = os.path.join(dossier, niv["drive"] + ".xlsx")
        with open(chemin, "wb") as f:
            f.write(contenu)
        print(f"{chemin} (modifié sur le Drive le {format_moment(modifie)})")


def main(args):
    if not args or args[0] in ("-h", "--help", "aide"):
        print(__doc__)
        return 0
    commande, reste = args[0], args[1:]
    try:
        if commande == "verifier":
            return verifier()
        if commande == "comparer":
            tout = "--tout" in reste
            dates = [a for a in reste if a != "--tout"]
            depuis = lire_date(dates[0]) if dates else aujourdhui() - dt.timedelta(days=7)
            comparer(depuis, tout)
            return 0
        if commande == "telecharger" and len(reste) == 1:
            telecharger(reste[0])
            return 0
    except DriveIndisponible as e:
        print(f"Drive indisponible : {e}")
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
