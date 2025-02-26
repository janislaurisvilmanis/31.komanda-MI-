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
# nevar, tādēļ kā algoritms domās, ka virknes [1, 3, 3, 3, 4] un [1, 3, 4, 3, 3] nav vienādas, kaut gan spēlēs ietvaros tie ir, tāpēc medz veidoties dublikāti spēles virsotņu kopā
def virkne_uz_multikopu(virkne):
    # Izmanto defaultdict, jo tā nevajag veikt pārbaudi pai 'skaitlis' (key) jau ir vārdnīcā, defaultdict to izdara automātiski un, nepieciešamības gadījumā, pats to pievieno
    multikopa = defaultdict(int) 
    for skaitlis in virkne:
        multikopa[skaitlis] += 1
    return multikopa

# Funkcija, kas veic gājienu un atjauno spēles koku
def gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne):
    global j
    # Izveido jaunu virsotnes ID, piemēram, 'A2', 'A3', utt.
    id_new = 'A' + str(j)  
    j += 1

    # Izveido kopiju no pašreizējās virsotnes virknes, lai to modificētu, neietekmējot oriģinālo
    mainita_virkne = pasreizeja_virsotne[1].copy()
    
    # Izņem skaitli no virknes atbilstoši gājiena tipam (indeksam)
    iznemtais_skaitlis = mainita_virkne.pop(gajiena_tips)
    
    # Noteikt, kura spēlētāja kārta ir un pieskaitīt/atņemt atbilstošus punktus
    # Spēlētājs 1 -> nepāra līmenis
    if pasreizeja_virsotne[4] % 2 == 1:  
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2] - 2 * iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]  
        else:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] + iznemtais_skaitlis
    # Spēlētājs 2 -> pāra līmenis
    else:  
        if iznemtais_skaitlis % 2 == 0:
            p1_new = pasreizeja_virsotne[2]
            p2_new = pasreizeja_virsotne[3] - 2 * iznemtais_skaitlis
        else:
            p1_new = pasreizeja_virsotne[2] + iznemtais_skaitlis
            p2_new = pasreizeja_virsotne[3]
            
    # Palielina līmeni par 1, jo pārejam uz nākamo spēles stāvokli
    limenis_new = pasreizeja_virsotne[4] + 1
    
    # Izveido jaunu virsotni ar atjaunināto virkni, punktiem un līmeni
    jauna_virsotne = Virsotne(id_new, mainita_virkne, p1_new, p2_new, limenis_new)
    
    # Pārveido jauno virkni par multikopu (vārdnīcu ar skaitļu skaitiem)
    jauna_multikopa = virkne_uz_multikopu(jauna_virsotne.virkne)
    
    # Pārbauda, vai jaunā virsotne jau eksistē spēles kokā (lai izvairītos no dublikātiem)
    parbaude = False
    # Sāk meklēt no pirmās virsotnes spēles kokā
    i = 0  
    while (not parbaude) and (i <= len(sp.virsotnu_kopa) - 1):
        # Salīdzina jauno virsotni ar esošajām virsotnēm
        if (virkne_uz_multikopu(sp.virsotnu_kopa[i].virkne) == jauna_multikopa and
            sp.virsotnu_kopa[i].p1 == jauna_virsotne.p1 and
            sp.virsotnu_kopa[i].p2 == jauna_virsotne.p2 and
            sp.virsotnu_kopa[i].limenis == jauna_virsotne.limenis):
            # Ja visi nosacījumi ir izpildīti, virsotne ir dublikāts
            parbaude = True  
        else:
            # Pāriet uz nākamo virsotni kokā
            i += 1  
    # Ja nav dublikātu
    if not parbaude: 
        # Pievieno jauno virsotni spēles kokam
        sp.pievienot_virsotni(jauna_virsotne)
        generetas_virsotnes.append([id_new, mainita_virkne, p1_new, p2_new, limenis_new])
        # Pievieno loku no pašreizējās virsotnes uz jauno virsotni
        sp.pievienot_loku(pasreizeja_virsotne[0], id_new)
    # Ja ir dublikāts
    else: 
        # Atceļ j palielināšanu, jo virsotne netika pievienota
        j -= 1  
        # Pievieno loku no pašreizējās virsotnes uz esošo virsotni (dublikātu)
        sp.pievienot_loku(pasreizeja_virsotne[0], sp.virsotnu_kopa[i].id)


# Spēles inicializācija
sp = Speles_koks()
generetas_virsotnes = []
# Lietotājs ievada virknes sākuma garumu
garums = int(input("Ievadiet skaitļu virknes garumu (no 15 līdz 25): "))
# Funkcija saģenerē nejaušo ciparu virkni
sakuma_virkne = generet_virkni(garums) 
# Spēles kokam tiek pievienota sākuma virsotne
sp.pievienot_virsotni(Virsotne('A1', sakuma_virkne, 100, 100, 1))
# Sākuma virsotne tiek pievienota izvēršamo virsotņu sarakstam
generetas_virsotnes.append(['A1', sakuma_virkne, 100, 100, 1]) 
j = 2

# Spēles izpilde
while len(generetas_virsotnes) > 0:
    # Tiem paņemta virsotne no izvēršamo virsotņu saraksta
    pasreizeja_virsotne = generetas_virsotnes[0]
    # Ierobežojums cik vajag līmeņu
    if pasreizeja_virsotne[4] < 3:
        # Cikls, kurš iet cauri visiem iespējamiem variantiem, kuru ciparu var izņemt no pašreizējas virsotnes ciparu virknes
        for gajiena_tips in range(len(pasreizeja_virsotne[1])): 
            gajiena_parbaude(gajiena_tips, generetas_virsotnes, pasreizeja_virsotne)
    # Virsotne ir izvērsta -> izdzēsta no izvēršamo virsotņu sarkasta
    generetas_virsotnes.pop(0) 
# Rezultātu izvade
for x in sp.virsotnu_kopa:
    print(x.id, x.virkne, x.p1, x.p2, x.limenis)
for x, y in sp.loku_kopa.items():
    print(x, y)
