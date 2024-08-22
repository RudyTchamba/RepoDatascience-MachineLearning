import numpy as np
import matplotlib.pyplot as plt

# Fonction d'activation sigmoïde
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Fonction de perte (entropie croisée binaire)
def binary_cross_entropy(y_true, y_pred):
    epsilon = 1e-15  # Pour éviter les log(0)
    y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(y_pred))

# Données d'entraînement
X = np.array([
    [0, 0, 0, 0],  # 0
    [0, 0, 0, 1],  # 1
    [0, 0, 1, 0],  # 2
    [0, 0, 1, 1],  # 3
    [0, 1, 0, 0],  # 4
    [0, 1, 0, 1],  # 5
    [0, 1, 1, 0],  # 6
    [0, 1, 1, 1],  # 7
    [1, 0, 0, 0],  # 8
    [1, 0, 0, 1],  # 9
])

# Labels (1 pour pair, 0 pour impair)
y = np.array([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

# Initialisation des poids et biais
np.random.seed(42)  # Pour des résultats reproductibles
weights = np.random.randn(4)
bias = np.random.randn()

# Paramètres de l'entraînement
learning_rate = 0.1
epochs = 10000

# Historique de l'erreur
loss_history = []

# Entraînement du perceptron
for epoch in range(epochs):
    # Calcul des prédictions
    linear_output = np.dot(X, weights) + bias
    y_pred = sigmoid(linear_output)
    
    # Calcul de la perte
    loss = binary_cross_entropy(y, y_pred)
    loss_history.append(loss)
    
    # Calcul des gradients
    error = y_pred - y
    d_weights = np.dot(X.T, error) / len(X)
    d_bias = np.mean(error)
    
    # Mise à jour des poids et biais
    weights -= learning_rate * d_weights
    bias -= learning_rate * d_bias
    
    # Affichage de la perte tous les 1000 epochs
    if epoch % 1000 == 0:
        print(f'Epoch {epoch}, Loss: {loss}')

# Prédiction après entraînement
def predict(x):
    linear_output = np.dot(x, weights) + bias
    y_pred = sigmoid(linear_output)
    return 1 if y_pred >= 0.5 else 0

# Test des prédictions
for i in range(10):
    print(f'Chiffre: {i}, Binaire: {X[i]}, Prédit: {"Pair" if predict(X[i]) else "Impair"}')

# Test des prédictions
y_pred = [predict(x) for x in X]
accuracy = np.mean(y == y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Tracé de l'évolution de l'erreur
plt.figure(figsize=(10, 6))
plt.plot(loss_history)
plt.title('Évolution de l\'erreur au cours de l\'entraînement')
plt.xlabel('Epochs')
plt.ylabel('Erreur (Entropie croisée binaire)')
plt.show()