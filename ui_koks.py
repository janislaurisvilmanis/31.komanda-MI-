import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from collections import defaultdict  # Izmanto, lai izveidotu defaultdict, kas palīdz skaitīt elementus (līdzīgi kā "skaitītāji")
import random  # Bibliotēka nejaušu skaitļu ģenerēšanai (izmanto, lai ģenerētu nejaušas virknes)
from math import inf  # Importējam bezgalības vērtību, ko izmantosim minimaks un alfa-beta algoritmos salīdzināšanai

# Klase, kas attēlo "virsotni" spēles koka struktūrā
class Virsotne:
    def __init__(self, id, virkne, p1, p2, limenis, pirmais):
        # Inicializējam virsotni, kuras parametri ir:
        self.id = id  # Virsotnes ID (unikāls identifikators)
        self.virkne = virkne  # Skaitļu virkne, kas ir pašreizējā virsotnē
        self.p1 = p1  # Datora spēles rezultāts
        self.p2 = p2  # Lietotāja spēles rezultāts
        self.limenis = limenis  # Virsotnes līmenis (kas nosaka spēles dziļumu)
        self.pirmais = pirmais  # Norāda, kurš spēlē pirmais (1 - dators, 2 - lietotājs)
        self.hfunction = None  # Heuristikas funkcija, kas novērtēs virsotni (tiek izmantota Minimax un Alfa-beta algoritmos)
        self.tagad_para_skaits = sum(1 for x in virkne if x % 2 == 0)  # Skaita pāra skaitļus pašreizējā virknes stāvoklī


def heuristika(virsotne, para_skaitlu_skaits_old):
    punktu_starpiba = virsotne.p1 - virsotne.p2 if virsotne.pirmais != 1 else  virsotne.p2 - virsotne.p1  # Punktu starpība starp datora un lietotāja rezultātiem

    # Pārbaudām, vai pašreizējā virsotnē ir mazāk pāra skaitļu nekā iepriekšējā
    if virsotne.tagad_para_skaits < para_skaitlu_skaits_old or virsotne.tagad_para_skaits == 0:
        korekcija = 2  # Pievienojam korekciju
    else:
        korekcija = 0
    return punktu_starpiba + korekcija


# Klase, kas attēlo spēles koku (kopsummu visām virsotnēm un lokiem)
class Speles_koks:
    def __init__(self):
        self.virsotnu_kopa = []  # Visu virsotņu saraksts spēles kokā
        self.loku_kopa = {}  # Loku saraksts, kas savieno virsotnes (iekšēja struktūra)

    def pievienot_virsotni(self, Virsotne):
        # Pievienojam virsotni spēles kokā
        self.virsotnu_kopa.append(Virsotne)
    
    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        # Pievienojam loku spēles kokā, kas sasaista sākuma un beigu virsotni
        if sakumvirsotne_id not in self.loku_kopa:
            self.loku_kopa[sakumvirsotne_id] = []  # Ja sākumvirsotne vēl nav, izveidojam tās sarakstu
        if beiguvirsotne_id not in self.loku_kopa[sakumvirsotne_id]:  # Izvairāmies no dublikātiem
            self.loku_kopa[sakumvirsotne_id].append(beiguvirsotne_id)

# Minimax algoritms, kas izvērtē visus iespējamos gājienus un izvēlas labāko
def minimax(virsotne, depth, maximizing_player, para_skaitlu_skaits_old):
    # Ja virkne ir tukša vai mēs esam sasnieguši maksimālo dziļumu, atgriežam heuristikas vērtību
    if not virsotne.virkne or depth == 0:
        virsotne.hfunction = heuristika(virsotne, para_skaitlu_skaits_old)
        return virsotne.hfunction

    if maximizing_player:  # Dators cenšas maksimizēt savu vērtību
        max_eval = -inf  # Sākotnēji iestatām maksimālo vērtību uz negatīvu bezgalību
        # Iterējam cauri visām bērnu virsotnēm
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)  # Atrodam bērnu virsotni
            eval = minimax(child, depth - 1, False, virsotne.tagad_para_skaits)  # Rekursīvi izsaucam minimax funkciju uz bērna
            max_eval = max(max_eval, eval)  # Saglabājam maksimālo vērtību
        virsotne.hfunction = max_eval  # Saglabājam virsotnes heuristikas vērtību
        return max_eval

    else:  # Lietotājs cenšas minimizēt savu vērtību
        min_eval = inf  # Sākotnēji iestatām minimālo vērtību uz pozitīvu bezgalību
        # Iterējam cauri visām bērnu virsotnēm
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)  # Atrodam bērnu virsotni
            eval = minimax(child, depth - 1, True, virsotne.tagad_para_skaits)  # Rekursīvi izsaucam minimax funkciju uz bērna
            min_eval = min(min_eval, eval)  # Saglabājam minimālo vērtību
        virsotne.hfunction = min_eval  # Saglabājam virsotnes heuristikas vērtību
        return min_eval

# Alfa-beta apgriešanas algoritms, kas optimizē minimax algoritmu
def alphabeta(virsotne, depth, alpha, beta, maximizing_player, para_skaitlu_skaits_old):
    # Ja virkne ir tukša vai mēs esam sasnieguši maksimālo dziļumu, atgriežam heuristikas vērtību
    if not virsotne.virkne or depth == 0:
        virsotne.hfunction = heuristika(virsotne, para_skaitlu_skaits_old)
        return virsotne.hfunction

    if maximizing_player:  # Dators cenšas maksimizēt savu vērtību
        max_eval = -inf
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            eval = alphabeta(child, depth - 1, alpha, beta, False, virsotne.tagad_para_skaits)  # Rekursīvi izsaucam alphabeta funkciju uz bērna
            max_eval = max(max_eval, eval)  # Saglabājam maksimālo vērtību
            alpha = max(alpha, eval)  # Atjauninām alfa vērtību
            if beta <= alpha:  # Ja beta ir mazāks vai vienāds ar alfa, pārtraucam
                break
        virsotne.hfunction = max_eval  # Saglabājam virsotnes heuristikas vērtību
        return max_eval

    else:  # Lietotājs cenšas minimizēt savu vērtību
        min_eval = inf
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            eval = alphabeta(child, depth - 1, alpha, beta, True, virsotne.tagad_para_skaits)
            min_eval = min(min_eval, eval)  # Saglabājam minimālo vērtību
            beta = min(beta, eval)  # Atjauninām beta vērtību
            if beta <= alpha:  # Ja beta ir mazāks vai vienāds ar alfa, pārtraucam
                break
        virsotne.hfunction = min_eval  # Saglabājam virsotnes heuristikas vērtību
        return min_eval


# Funkcija, kas ģenerē spēles koku līdz noteiktajam dziļumam
def generate_tree_from(virsotne, max_depth):
    # Ja sasniegts maksimālais dziļums vai pašreizējā virkne ir tukša, tad pārtraucam koka ģenerēšanu
    if max_depth == 0 or not virsotne.virkne:
        return
    
    # Iterējam pa visiem elementiem virknē, lai veiktu gājienu pārbaudes
    for i in range(len(virsotne.virkne)):
        gajiena_parbaude(i, virsotne)

    # Rekurzīvi paplašinām koku, apstrādājot visus bērnus (gājienus)
    for child_id in sp.loku_kopa.get(virsotne.id, []):
        child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
        generate_tree_from(child, max_depth - 1)

# Funkcija, kas nosaka skaitli, kas ir noņemts starp veco un jauno virkni
def atrast_noņemto_skaitli(vecais, jaunais):
    for i in range(len(vecais)):
        # Atgriežam pirmo skaitli, kas atšķiras starp veco un jauno virkni
        if i >= len(jaunais) or vecais[i] != jaunais[i]:
            return vecais[i]

# Funkcija, kas ģenerē skaitļu virkni ar norādīto garumu
def generet_virkni(garums):
    # Atgriežam virkni ar nejaušiem skaitļiem no 1 līdz 4
    return [random.randint(1, 4) for _ in range(garums)]

# Funkcija, kas pārveido virkni par multikopu (vārdnīcu ar skaitļu skaitiem), piemēram virknei [1, 3, 3, 3, 4] multivirkne būtu {1 : 1, 3 : 3, 4 : 1}, jo vienkārši salīdzīnāt masīvus
# nevar, tādēļ kā algoritms domās, ka virknes [1, 3, 3, 3, 4] un [1, 3, 4, 3, 3] nav vienādas, kaut gan spēlēs ietvaros tie ir, tāpēc medz veidoties dublikāti spēles virsotņu kopā
def virkne_uz_multikopu(virkne):
    # Izmanto defaultdict, jo tā nevajag veikt pārbaudi pai 'skaitlis' (key) jau ir vārdnīcā, defaultdict to izdara automātiski un, nepieciešamības gadījumā, pats to pievieno
    multikopa = defaultdict(int)
    for skaitlis in virkne:
        multikopa[skaitlis] += 1
    return multikopa

# Funkcija, kas pārbauda gājienu, maina virkni un aprēķina jaunās vērtības
def gajiena_parbaude(gajiena_tips, pasreizeja_virsotne):
    global j
    id_new = 'A' + str(j)  # Veidojam jaunu id jaunajai virsotnei
    j += 1

    mainita_virkne = pasreizeja_virsotne.virkne[:]  # Veidojam kopiju pašreizējai virkne
    iznemtais_skaitlis = mainita_virkne.pop(gajiena_tips)  # Noņemam skaitli, pamatojoties uz izvēlēto gājiena tipu

    # Atjaunojam spēlētāju punktus atkarībā no gājiena
    p1_new, p2_new = pasreizeja_virsotne.p1, pasreizeja_virsotne.p2
    if pasreizeja_virsotne.limenis % 2 == 1:  # Ja līmenis ir nepāra, spēlētājs 1 veic gājienu
        if iznemtais_skaitlis % 2 == 0:
            p1_new -= 2 * iznemtais_skaitlis
        else:
            p2_new += iznemtais_skaitlis
    else:  # Ja līmenis ir pāra, spēlētājs 2 veic gājienu
        if iznemtais_skaitlis % 2 == 0:
            p2_new -= 2 * iznemtais_skaitlis
        else:
            p1_new += iznemtais_skaitlis

    limenis_new = pasreizeja_virsotne.limenis + 1  # Jaunais līmenis pēc gājiena
    pirmais = pasreizeja_virsotne.pirmais

    # Izveidojam jaunu virsotni ar atjaunotajiem datiem
    jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new, pirmais)
    jauna_multikopa = virkne_uz_multikopu(jauna_virsotne.virkne)  # Pārvēršam virkni par multikopu

    # Pārbaudām, vai šī virsotne jau eksistē spēles kokā
    parbaude = False
    i = 0
    while not parbaude and i < len(sp.virsotnu_kopa):
        existing_virsotne = sp.virsotnu_kopa[i]
        # Ja ir līdzība starp veco un jauno virsotni, pārtraucam meklēšanu
        if (virkne_uz_multikopu(existing_virsotne.virkne) == jauna_multikopa and
            existing_virsotne.p1 == jauna_virsotne.p1 and
            existing_virsotne.p2 == jauna_virsotne.p2 and
            existing_virsotne.limenis == jauna_virsotne.limenis):
            parbaude = True
        else:
            i += 1

    # Ja virsotne nav atrasta, pievienojam to spēles kokā
    if not parbaude:
        sp.pievienot_virsotni(jauna_virsotne)
        sp.pievienot_loku(pasreizeja_virsotne.id, id_new)
    else:
        # Ja virsotne jau eksistē, samazinām skaitītāju un pievienojam loku
        j -= 1
        sp.pievienot_loku(pasreizeja_virsotne.id, sp.virsotnu_kopa[i].id)

# Globālie mainīgie
sp = Speles_koks()
j = 2
MAX_DEPTH = 5
pirmais = 1  # Noklusējums: dators sāk
algoritms = 1  # Noklusējums: Minimax
sakuma_virkne = []
current_node = None

# Interfeisa mainīgie
izvele = None

# Interfeisa funkcijas
def sakuma_spele():
    global sakuma_virkne, current_node, sp, j
    sp = Speles_koks() # veido jaunu spēles koku
    j = 2
    try:
        # Iegūst virknes garumu no lietotāja ievades
        garums = int(entry_garums.get())
        # Tiek veikta pārbaude, vai virknes garums ir diapazonā
        if garums < 15 or garums > 25:
            messagebox.showerror("Kļūda", "Virknes garumam jābūt no 15 līdz 25!")
            return
        # Sākuma virknes ģenerēšana
        sakuma_virkne = generet_virkni(garums)
        # Izveido sākuma virsotni ar sākuma virkni un spēlētāju puntkiem
        current_node = Virsotne('A1', sakuma_virkne, 100, 100, 1, pirmais)
        atjaunot_spele_stavokli()
        spele_cikls()
    except ValueError:
        messagebox.showerror("Kļūda", "Lūdzu, ievadiet veselu skaitli!")

# Iestata, kurš spēlētājs sāks pirmais
def izveleties_pirmo(speletajs):
    global pirmais
    pirmais = speletajs
# Iestata, kurš algoritms tiks izmantots pirmais
def izveleties_algoritmu(alg):
    global algoritms
    algoritms = alg

# Tiek veikta spēles stāvokļa atjaunināšana lietotāja saskarsnē
def atjaunot_spele_stavokli():
    if current_node:
        # Atjaunina spēlētāja un datora punktu skaitu
        player_points.config(text=current_node.p2 if pirmais == 1 else current_node.p1)
        ai_points.config(text=current_node.p1 if pirmais == 1 else current_node.p2)
        # Atjaunina pašreizējās virknes attēlojumu
        virkne_label.config(text=f"Pašreizējā virkne: {current_node.virkne}" )
        # Izvada un atjaunina virkni kopā ar indeksiem
        virkne_ar_indeksiem = " ".join([f"{num}({i+1})" for i, num in enumerate(current_node.virkne)])
        indeksi_label.config(text = f"Indeksi: {virkne_ar_indeksiem}")
    else:
        # Noklusējuma vērtības
        player_points.config(text="XXX")
        ai_points.config(text="XXX")
        virkne_label.config(text="Pašreizējā virkne: ")
        indeksi_label.config(text = "Indeksi: ")

def spele_cikls():
    global current_node
    if not current_node.virkne:
        if current_node.p1 > current_node.p2:
            virkne_label.config(text = "Spēle beigusies!\nUzvarētājs: Dators")
        elif current_node.p1 < current_node.p2:
            virkne_label.config(text = "Spēle beigusies!\nUzvarētājs: Lietotājs")
        else:
            virkne_label.config(text = "Spēle beigusies!\nNeizšķirts")
    
    # Pārbauda vai ir datora gājiens
    if (current_node.limenis % 2 == 1 and pirmais == 1) or (current_node.limenis % 2 == 0 and pirmais == 2):
        generate_tree_from(current_node, MAX_DEPTH)
        best_value = minimax(current_node, MAX_DEPTH, True, current_node.tagad_para_skaits) if algoritms == 1 else alphabeta(current_node, MAX_DEPTH, -inf, inf, True, current_node.tagad_para_skaits)
        best_child = next(v for v in sp.virsotnu_kopa if v.id in sp.loku_kopa.get(current_node.id, []) and v.hfunction == best_value)
        current_node = best_child
        atjaunot_spele_stavokli()
        root.after(1000, spele_cikls)  # Pagaida 1 sekundi pirms nākamā gājiena
    else:
        # Ja ir lietotāja gājiens, tiek izvadīta lietotāja gājiena ievades poga
        izvele_poga = tk.Button(frame_right, text="Iesniegt", font=("Arial", 12), bg="#5C6B7D", fg="white", width=10, command=lietotaja_gajiens)
        izvele_poga.grid(row=7, column=0, columnspan=2)

def lietotaja_gajiens():
    global current_node, izvele
    try:
        # Iegūst lietotāja izvēlēto indeksu un samazina to par 1, lai tā vērtība tiktu atbalstīta saraksta indeksācijai
        izvele = int(entry_izvele.get()) - 1
        # Indeksa derīguma pārbaude
        if izvele < 0 or izvele > len(current_node.virkne):
            messagebox.showerror("Kļūda", "Nepareizs indekss!")
            return
        # Tiek veikts lietotāja gājiens
        gajiena_parbaude(izvele, current_node)
        temp_virkne = virkne_uz_multikopu(current_node.virkne[:izvele] + current_node.virkne[izvele + 1:])
        current_node = next(v for v in sp.virsotnu_kopa if v.id in sp.loku_kopa.get(current_node.id, []) and virkne_uz_multikopu(v.virkne) == temp_virkne)
        atjaunot_spele_stavokli()
        # Notīra ievades lauku, katru reizi, kad tiek uzspiesta poga iesniegt, lai varētu ievadīt nākamo gājienu
        entry_izvele.delete(0, tk.END)
        spele_cikls()
    except ValueError:
        messagebox.showerror("Kļūda", "Lūdzu, ievadiet veselu skaitli!")


def restart_spele():
    # Tiek izsaukta funkcija, lai varētu sākt spēli no jauna
    sakuma_spele()

# Interfeisa izveide
root = tk.Tk()
root.title("Spēle") # Programmas virsraksts
root.geometry("1200x600") # Loga izmēra mērogošana
root.configure(bg="#5C6B7D") # Fona krāsa

# Kreisās loga puses iestatījumi
frame_left = tk.Frame(root, bg="#5C6B7D", width=400, height=550)
frame_left.place(x=70, y=20)

# Virknes ievades lauka izveide
title_label = tk.Label(frame_left, text="Ievadiet virknes garumu, (15 - 25)", font=("Arial", 14), bg="#5C6B7D", fg="white")
title_label.pack(pady=10)

entry_garums = ttk.Entry(frame_left, font=("Arial", 12))
entry_garums.pack(pady=5, padx=10, ipadx=40, ipady=5)

# Punktu skaita loga izveide
frame_points = tk.Frame(frame_left, bg="#5C6B7D")
frame_points.pack(pady=20)

player_label = tk.Label(frame_points, text="Player points", font=("Arial", 10), bg = "#5C6B7D", fg = "white")
player_label.grid(row=0, column=0, padx=20)

ai_label = tk.Label(frame_points, text="AI points", font=("Arial", 10), bg = "#5C6B7D", fg = "white")

ai_label.grid(row=0, column=1, padx=20)

player_points = tk.Label(frame_points, text="XXX", font=("Arial", 12, "bold"), bg="white", width = 6, height = 2)
player_points.grid(row=1, column=0, padx=10, pady=5)

ai_points = tk.Label(frame_points, text="XXX", font=("Arial", 12, "bold"), bg="white", width = 6, height = 2)
ai_points.grid(row=1, column=1, padx=10, pady=5)

# Virknes un indeksu izvades lauks
virkne_label = tk.Label(frame_left, text="Pašreizējā virkne: ", font=("Arial", 10), bg="#5C6B7D", fg="white")
virkne_label.pack(pady=10)

indeksi_label = tk.Label(frame_left, text="Indeksi: ", font=("Arial", 10), bg="#5C6B7D", fg="white") # Pievienots indeksi_label
indeksi_label.pack(pady=5)

# Labās loga puses iestatījumi
frame_right = tk.Frame(root, bg="#5C6B7D")
frame_right.place(x=900, y=50)

# Izvēles pogu izveide
start_label = tk.Label(frame_right, text="Kurš uzsāks spēli:", font=("Arial", 12, "bold"), bg ="#5C6B7D")
start_label.grid(row=0, column=0, columnspan=2, pady=5)

player_button = tk.Button(frame_right, text="Player", font=("Arial", 12), bg="#5C6B7D", fg="white", width=10, command = lambda: izveleties_pirmo(2)) # command atbilst poga funkcijas izsaukšanai, kad tā tiek nospiesta
player_button.grid(row=1, column=0, padx=5, pady=5)

ai_button = tk.Button(frame_right, text="AI", font=("Arial", 12), bg="#5C6B7D", fg="white", width=10, command = lambda: izveleties_pirmo(1))
ai_button.grid(row=1, column=1, padx=5, pady=5)

ai_method_label = tk.Label(frame_right, text="AI method:", font=("Arial", 12, "bold"), bg="#5C6B7D")
ai_method_label.grid(row=2, column=0, columnspan=2, pady=5)

minimax_button = tk.Button(frame_right, text="Minimax", font=("Arial", 12), bg="#D3D3D3", width=10, command = lambda: izveleties_algoritmu(1))
minimax_button.grid(row=3, column=0, padx=5, pady=5)

alpha_beta_button = tk.Button(frame_right, text="Alfa - beta", font=("Arial", 12), bg="#D3D3D3", width=10, command = lambda: izveleties_algoritmu(2))
alpha_beta_button.grid(row=3, column=1, padx=5, pady=5)

# Darbības pogu izveide
start_button = tk.Button(frame_right, text="START", font=("Arial", 12, "bold"), bg="#5C6B7D", fg="white", width=10, command = sakuma_spele)
start_button.grid(row=4, column=0, padx=5, pady=10)

restart_button = tk.Button(frame_right, text="RESTART", font=("Arial", 12, "bold"), bg="#B22222", fg="white", width=10, command = restart_spele)
restart_button.grid(row=4, column=1, padx=5, pady=10)

# Indeksa ievades lauka izveide
izvele_label = tk.Label(frame_right, text="Ievadiet kārtas numuru:", font=("Arial", 12, "bold"), bg="#5C6B7D")
izvele_label.grid(row=5, column=0, columnspan=2, pady=5)

entry_izvele = ttk.Entry(frame_right, font=("Arial", 12))
entry_izvele.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop() # Cilpa, kas ir atbildīga par to, lai lietojumprogramma reaģētu uz 
               # lietotāja ievadi, bez šīs cilpas lietojumprogramma nereaģēs uz nekādiem notikumiem un būs nefunkcionāla