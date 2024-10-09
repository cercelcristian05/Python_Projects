from sklearn.svm import OneClassSVM
import joblib
import numpy as np

# Load embeddings and labels (you only have "trusted" embeddings)
X = np.load('face_embeddings.npy')

# Train a One-Class SVM classifier
clf = OneClassSVM(kernel='rbf', gamma='auto').fit(X)

# Save the trained model
joblib.dump(clf, 'one_class_face_recognition_model.pkl')
print("One-Class SVM model saved to one_class_face_recognition_model.pkl")
