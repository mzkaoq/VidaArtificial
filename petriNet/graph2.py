import matplotlib.pyplot as plt

# Coordonnées des points pour les itérations avant embouteillage
x = [1, 2, 3]
y_iterations = [24, 109, 420]

# Coordonnées des points pour le nombre de voitures
y_cars = [50, 120, 300]  # Valeurs inventées

# Création du graphique
plt.figure(figsize=(8, 6))

# Courbe pour les itérations avant embouteillage
plt.plot(x, y_iterations, marker='o', linestyle='-', color='blue', label="Iterations before traffic jam")

# Courbe pour le nombre de voitures
plt.plot(x, y_cars, marker='s', linestyle='--', color='green', label="Number of cars")

# Légendes des axes
plt.xlabel("Number of lanes")
plt.ylabel("Values")

# Titre du graphique
plt.title("Traffic Analysis: Iterations vs. Number of Cars")

# Affichage de la légende
plt.legend()

# Affichage du graphique
plt.show()