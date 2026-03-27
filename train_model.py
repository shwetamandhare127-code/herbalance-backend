import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Load dataset
data = pd.read_excel("PCOS_data.xlsx")

data.columns = data.columns.str.strip()

# Target
y = data['PCOS (Y/N)']

# Features
X = data[['Age (yrs)', 'Weight (Kg)', 'BMI',
          'Cycle length(days)',
          'hair growth(Y/N)', 'Skin darkening (Y/N)',
          'Pimples(Y/N)', 'Weight gain(Y/N)',
          'Fast food (Y/N)', 'Reg.Exercise(Y/N)']]

# Clean data
X = X.dropna()
y = y.loc[X.index]

print("Remaining rows:", len(X))  #  debug line

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
print("Model Accuracy:", accuracy_score(y_test, y_pred))

# Save
with open("pcos_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved successfully!")