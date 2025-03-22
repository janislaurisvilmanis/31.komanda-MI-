import random
from collections import defaultdict

# Klase, kas atbilst vienai spēles koka virsotnei
class Virsotne:
    def __init__(self, id, virkne, p1, p2, limenis, pirmais):
        self.id = id #virsotnse indikātors
        self.virkne = virkne #skaitļu virkne šajā virsotnē
        self.p1 = p1  # Datora punkti
        self.p2 = p2  # Lietotāja punkti
        self.limenis = limenis #virsotnes atrašanās koka dziļumā
        self.pirmais = pirmais  # 1 - dators, 2 - lietotājs
        self.hfunction = None  # Heuristika tiks aprēķināta tikai lapas virsotnēm

 # Heuristikas aprēķināšana lapas virsotnēm
    def calculate_heuristic(self):
        # Saskaita cik pāra skaitļi vēl palikuši virknes rindā.
        para_skaitli = sum(1 for skaitlis in self.virkne if skaitlis % 2 == 0) #saskaita pāra skaitļus

        if self.pirmais == 1:  # dators uzsāk spēli
            punktu_starpiba = self.p2 - self.p1
             # Aprēķina punktu starpību: lietotāja punkti - datora punkti.
            # Ja šī vērtība ir pozitīva, tas nozīmē, ka dators ir priekšā (viņam ir mazāk punktu)
            return punktu_starpiba + 6 if para_skaitli % 2 == 0 else punktu_starpiba - 6
        else:  # lietot. uzsāk spēli
            # Šoreiz skatāmies no lietotāja perspektīvas — mēs aprēķinām punktu starpību kā dators - lietotājs.
            # Pozitīva vērtība nozīmē, ka lietotājs ir vadībā (tas ir slikti datoram).
            punktu_starpiba = self.p1 - self.p2
            return punktu_starpiba - 6 if para_skaitli % 2 == 0 else punktu_starpiba + 6

# klase, kas pārstāv isu spēles koku
class Speles_koks:
    def __init__(self):
        self.virsotnu_kopa = [] #saraksts ar visām virsotnēm
        self.loku_kopa = dict()

    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne) #pievieno jaunu virsotni koka struktūrai

    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(sakumvirsotne_id, []) + [beiguvirsotne_id]

#minimax algoritms lēmumu pieņemšanai

def minimax(virsotne, depth, maximizing_player):
     # Ja esam sasnieguši maksimālo dziļumu vai virkne ir tukša (vairs nav iespējamo gājienu),
    # tad aprēķinām heuristisko vērtību šai virsotnei un atgriežam to.
    if not virsotne.virkne or depth == 0: #ja vairs nav iespējamo gajienu vai sasniegts maksimālais dziļums
        virsotne.hfunction = virsotne.calculate_heuristic()
        return virsotne.hfunction

    # Ja šajā līmenī ir datora gājiens (maksimizējošais spēlētājs):
    if maximizing_player: 
        max_eval = -float('inf')
        for child_id in sp.loku_kopa.get(virsotne.id, []): # Apstrādā visus bērnus
            # Atrodam bērnu virsotni pēc ID
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            # Izsaucam minimax rekursīvi nākamajam līmenim, pārslēdzoties uz minimizējošo spēlētāju
            eval = minimax(child, depth - 1, False)
            # Izvēlamies lielāko no iegūtajām vērtībām
            max_eval = max(max_eval, eval)
        virsotne.hfunction = max_eval # Saglabājam labāko vērtību šajā mezglā
        return max_eval
    else: 
        # Ja gājiens pieder lietotājam (minimizējošais spēlētājs)
        min_eval = float('inf')
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            # Rekursīvi izsaucam nākamo līmeni, pārslēdzoties atpakaļ uz maksimizējošo spēlētāju (datoru)
            eval = minimax(child, depth - 1, True)
            # Izvēlamies mazāko no iegūtajām vērtībām
            min_eval = min(min_eval, eval)
        virsotne.hfunction = min_eval # Saglabājam šajā virsotnē
        return min_eval

# Sākotnējas skaitļu virknes ģenerēšana
def generet_virkni(garums):
    return [1,2,3,4]

# Konvertē skaitļu virkni par multikopu
def virkne_uz_multikopu(virkne):
    multikopa = defaultdict(int)
    for skaitlis in virkne:
        multikopa[skaitlis] += 1
    return multikopa

# Pārbauda un izveido jaunas virsotnes iespējamajiem gājieniem
def gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne):
    global j
    id_new = 'A' + str(j)
    j += 1

    mainita_virkne = pasreizeja_virsotne[1].copy()
    iznemtais_skaitlis = mainita_virkne.pop(gajiena_tips)


# Punktu aprēķins
    if pasreizeja_virsotne[4] % 2 == 1:
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2] - 2 * iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]
        else:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] + iznemtais_skaitlis
    else:
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] - 2 * iznemtais_skaitlis
        else:
            p1_new = pasreizeja_virsotne[2] + iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]

    limenis_new = pasreizeja_virsotne[4] + 1
    pirmais = pasreizeja_virsotne[5]
    jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new, pirmais)
    jauna_multikopa = virkne_uz_multikopu(jauna_virsotne.virkne)

    parbaude = False
    i = 0
    while not parbaude and i <= len(sp.virsotnu_kopa) - 1:
        if (virkne_uz_multikopu(sp.virsotnu_kopa[i].virkne) == jauna_multikopa and
            sp.virsotnu_kopa[i].p1 == jauna_virsotne.p1 and
            sp.virsotnu_kopa[i].p2 == jauna_virsotne.p2 and
            sp.virsotnu_kopa[i].limenis == jauna_virsotne.limenis):
            parbaude = True
        else:
            i += 1

    if not parbaude:
        sp.pievienot_virsotni(jauna_virsotne)
        generetas_virsotnes.append([id_new, mainita_virkne, p1_new, p2_new, limenis_new, pirmais])
        sp.pievienot_loku(pasreizeja_virsotne[0], id_new)
    else:
        j -= 1
        sp.pievienot_loku(pasreizeja_virsotne[0], sp.virsotnu_kopa[i].id)

# Spēles inicializācija
sp = Speles_koks()
generetas_virsotnes = []

pirmais = int(input("Kurš sāk spēli? (1 - dators, 2 - lietotājs): "))
while pirmais not in [1, 2]:
    pirmais = int(input("Lūdzu ievadiet tikai 1 (dators) vai 2 (lietotājs): "))

garums = int(input("Ievadiet skaitļu virknes garumu (no 15 līdz 25): "))
sakuma_virkne = generet_virkni(garums)
sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, 100, 100, 1, pirmais))
generetas_virsotnes.append(['A1', sakuma_virkne, 100, 100, 1, pirmais])
j = 2

while len(generetas_virsotnes) > 0:
    pasreizeja_virsotne = generetas_virsotnes[0]
    if pasreizeja_virsotne[4] < 4:
        for gajiena_tips in range(len(pasreizeja_virsotne[1])):
            gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne)
    generetas_virsotnes.pop(0)

best_value = minimax(sp.virsotnu_kopa[0], depth=4, maximizing_player=True)
print("Labākā vērtība:", best_value)

for x in sp.virsotnu_kopa:
    print(x.id, x.virkne, x.p1, x.p2, x.limenis, x.hfunction)
for x, y in sp.loku_kopa.items():
    print(x, y)