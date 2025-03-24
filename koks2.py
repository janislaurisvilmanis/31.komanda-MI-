from collections import defaultdict

class Virsotne:
    def __init__(self, id, virkne, p1, p2, limenis, pirmais, start_sequence=None):
        self.id = id
        self.virkne = virkne
        self.p1 = p1
        self.p2 = p2
        self.limenis = limenis
        self.pirmais = pirmais  # 1 - dators, 2 - lietotājs
        self.hfunction = None
        self.start_sequence = start_sequence if start_sequence is not None else virkne.copy()

def heuristika_dators_pirmais(virsotne):
    punktu_starpība = virsotne.p2 - virsotne.p1

    sakuma_pāra_skaits = sum(1 for x in virsotne.start_sequence if x % 2 == 0)
    tagad_pāra_skaits = sum(1 for x in virsotne.virkne if x % 2 == 0)

    sakuma_pāra_rezultāts = sakuma_pāra_skaits % 2
    tagad_pāra_rezultāts = tagad_pāra_skaits % 2

    korekcija = -6 if sakuma_pāra_rezultāts == tagad_pāra_rezultāts else 6

    return punktu_starpība + korekcija

def heuristika_lietotajs_pirmais(virsotne):
    punktu_starpība = virsotne.p1 - virsotne.p2

    sakuma_pāra_skaits = sum(1 for x in virsotne.start_sequence if x % 2 == 0)
    tagad_pāra_skaits = sum(1 for x in virsotne.virkne if x % 2 == 0)

    sakuma_pāra_rezultāts = sakuma_pāra_skaits % 2
    tagad_pāra_rezultāts = tagad_pāra_skaits % 2

    korekcija = 6 if sakuma_pāra_rezultāts == tagad_pāra_rezultāts else -6

    return punktu_starpība + korekcija

class Speles_koks:
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()

    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne)

    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(sakumvirsotne_id, []) + [beiguvirsotne_id]

def minimax(virsotne, depth, maximizing_player):
    if not virsotne.virkne or depth == 0:
        if virsotne.pirmais == 1:
            virsotne.hfunction = heuristika_dators_pirmais(virsotne)
        else:
            virsotne.hfunction = heuristika_lietotajs_pirmais(virsotne)
        return virsotne.hfunction

    if maximizing_player:
        max_eval = -float('inf')
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            eval = minimax(child, depth - 1, False)
            max_eval = max(max_eval, eval)
        virsotne.hfunction = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for child_id in sp.loku_kopa.get(virsotne.id, []):
            child = next(v for v in sp.virsotnu_kopa if v.id == child_id)
            eval = minimax(child, depth - 1, True)
            min_eval = min(min_eval, eval)
        virsotne.hfunction = min_eval
        return min_eval

def generet_virkni(garums):
    return [1, 4, 1, 4, 4]  # testa dati

def virkne_uz_multikopu(virkne):
    multikopa = defaultdict(int)
    for skaitlis in virkne:
        multikopa[skaitlis] += 1
    return multikopa

def gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne):
    global j
    id_new = 'A' + str(j)
    j += 1

    mainita_virkne = pasreizeja_virsotne[1].copy()
    iznemtais_skaitlis = mainita_virkne.pop(gajiena_tips)

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
    start_sequence = sp.virsotnu_kopa[0].virkne

    jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new, pirmais, start_sequence)
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

sp = Speles_koks()
generetas_virsotnes = []

pirmais = int(input("Kurš sāk spēli? (1 - dators, 2 - lietotājs): "))
while pirmais not in [1, 2]:
    pirmais = int(input("Lūdzu ievadiet tikai 1 (dators) vai 2 (lietotājs): "))

garums = int(input("Ievadiet skaitļu virknes garumu (no 15 līdz 25): "))
sakuma_virkne = generet_virkni(garums)
sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, 100, 100, 1, pirmais, sakuma_virkne))
generetas_virsotnes.append(['A1', sakuma_virkne, 100, 100, 1, pirmais])
j = 2

while len(generetas_virsotnes) > 0:
    pasreizeja_virsotne = generetas_virsotnes[0]
    if pasreizeja_virsotne[4] < 4:
        for gajiena_tips in range(len(pasreizeja_virsotne[1])):
            gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne)
    generetas_virsotnes.pop(0)

maximizing_player = True if pirmais == 1 else False
best_value = minimax(sp.virsotnu_kopa[0], depth=3, maximizing_player=maximizing_player)
print("Labākā vērtība:", best_value)

for x in sp.virsotnu_kopa:
    print(x.id, x.virkne, x.p1, x.p2, x.limenis, x.hfunction)
for x, y in sp.loku_kopa.items():
    print(x, y)
