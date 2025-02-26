import random
from collections import defaultdict

# Klase, kas atbilst vienai virsotnei spēles kokā
class Virsotne:
    def __init__(self, id, virkne, p1, p2, limenis):
        self.id = id
        self.virkne = virkne
        self.p1 = p1
        self.p2 = p2
        self.limenis = limenis

# Klase, kas atbilst spēles kokam
class Speles_koks:
    def __init__(self):
        self.virsotnu_kopa = []
        self.loku_kopa = dict()
    
    def pievienot_virsotni(self, Virsotne):
        self.virsotnu_kopa.append(Virsotne)
        
    def pievienot_loku(self, sakumvirsotne_id, beiguvirsotne_id):
        self.loku_kopa[sakumvirsotne_id] = self.loku_kopa.get(sakumvirsotne_id, []) + [beiguvirsotne_id]

# Funkcija, kas ģenerē sākuma skaitļu virkni
def generet_virkni(garums):
    return [random.randint(1, 4) for _ in range(garums)]

# Funkcija, kas pārveido virkni par multikopu (vārdnīcu ar skaitļu skaitiem), piemēram virknei [1, 3, 3, 3, 4] multivirkne būtu {1 : 1, 3 : 3, 4 : 1}, jo vienkārši salīdzīnāt masīvus
# nevar, tādēļ kā algoritms domās, ka virknes [1, 3, 3, 3, 4] un [1, 3, 4, 3, 3] nav vienādas, kaut gan spēlēs ietvaros tie ir
def virkne_uz_multikopu(virkne):
    multikopa = defaultdict(int)
    for skaitlis in virkne:
        multikopa[skaitlis] += 1
    return multikopa

# Funkcija, kas veic gājienu un atjauno spēles koku
def gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne):
    global j
    id_new = 'A' + str(j)
    j += 1
    mainita_virkne = pasreizeja_virsotne[1].copy()
    iznemtais_skaitlis = mainita_virkne.pop(gajiena_tips)
    
    # Noteikt, kura spēlētāja kārta ir un pieskaitīt atbilstošus punktus
    if pasreizeja_virsotne[4] % 2 == 1:  # Spēlētājs 1 -> nepāra līmenis
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2] - 2 * iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]
        else:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] + iznemtais_skaitlis
    else:  # # Spēlētājs 2 -> pāra līmenis
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] - 2 * iznemtais_skaitlis
        else:
            p1_new = pasreizeja_virsotne[2] + iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]
    
    limenis_new = pasreizeja_virsotne[4] + 1
    jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new)
    
    # Pārveido pašreizējo un jauno virkni par multikopām
    jauna_multikopa = virkne_uz_multikopu(jauna_virsotne.virkne)
    

    parbaude = False
    i = 0
    while (not parbaude) and (i <= len(sp.virsotnu_kopa) - 1):
        # Salīdzina jauno virsotni ar visām virsotnēm spēlē 9lai nebūtu dublikātu)
        if (virkne_uz_multikopu(sp.virsotnu_kopa[i].virkne) == jauna_multikopa and 
            sp.virsotnu_kopa[i].p1 == jauna_virsotne.p1 and 
            sp.virsotnu_kopa[i].p2 == jauna_virsotne.p2 and 
            sp.virsotnu_kopa[i].limenis == jauna_virsotne.limenis):
            parbaude = True
        else:
            i += 1
    
    if not parbaude: # ja nav dublikātu - pievieno jauno virsotni
        sp.pievienot_virsotni(jauna_virsotne)
        generetas_virsotnes.append([id_new, mainita_virkne, p1_new, p2_new, limenis_new])
        sp.pievienot_loku(pasreizeja_virsotne[0], id_new)
    else: # ja ir dublikāti - norāda jauno loku uz jauno virsotni no pašreizējas virsotnes
        j -= 1
        sp.pievienot_loku(pasreizeja_virsotne[0], sp.virsotnu_kopa[i].id)


# Spēles inicializācija
sp = Speles_koks()
generetas_virsotnes = []
garums = int(input("Ievadiet skaitļu virknes garumu (no 15 līdz 25): "))
sakuma_virkne = generet_virkni(garums)
sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, 100, 100, 1))
generetas_virsotnes.append(['A1', sakuma_virkne, 100, 100, 1])
j = 2

# Spēles izpilde
while len(generetas_virsotnes) > 0:
    pasreizeja_virsotne = generetas_virsotnes[0]
    if pasreizeja_virsotne[4] < 3: # Ierobežojums cik vajag līmeņu
        for gajiena_tips in range(len(pasreizeja_virsotne[1])):
            gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne)
    generetas_virsotnes.pop(0)
# Rezultātu izvade
for x in sp.virsotnu_kopa:
    print(x.id, x.virkne, x.p1, x.p2, x.limenis)
for x, y in sp.loku_kopa.items():
    print(x, y)