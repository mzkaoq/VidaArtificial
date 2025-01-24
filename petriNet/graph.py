import matplotlib.pyplot as plt

# Coordonnées des points
x = [1, 3, 4, 5]
y = [240, 995, 1398, 2147]

# Création du graphique
plt.figure(figsize=(8, 6))
plt.plot(x, y, marker='o', linestyle='-', color='green', label="Points")  # Trace une ligne reliant les points
plt.xlabel("Number of lanes")  # Légende de l'axe des x
plt.ylabel("Traffic capacity")  # Légende de l'axe des y
plt.title("Traffic capacity depending the lane number")
plt.legend()  # Affichage de la légende
plt.show()