import random

# Génération et affichage de 100 nombres aléatoires entre 1 et 8
p1 = 0
p2 = 0
p3 = 0
p4 = 0
p5 = 0

for i in range(100):
    nb = random.randint(1, 8)
    if(p2==2):
        print("traffic jam",i)
    if(nb==1):
        if(p1<2):
            p1 = p1 +1
        else:
            print(i,p1,p2,p3,p4,p5)
        
    if(nb==7):
        if(p3<2):
            p3 = p3 +1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==8):
        if(p5>0):
            p5 = p5 - 1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==5):
        if(p4>0):
            p4 = p4 - 1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==2):
        if(p1>0)and(p2<2):
            p1 = p1 - 1
            p2 = p2 + 1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==6):
        if(p3>0)and(p2<2):
            p3 = p3 - 1
            p2 = p2 + 1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==3):
        if(p2>0)and(p5<2):
            p5 = p5 + 1
            p2 = p2 - 1
        else:
            print(i,p1,p2,p3,p4,p5)

    if(nb==4):
        if(p2>0)and(p4<2):
            p4 = p4 + 1
            p2 = p2 - 1
        else:
            print(i,p1,p2,p3,p4,p5)
