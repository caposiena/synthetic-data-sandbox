import pandas as pd

columns = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
    "Outcome",
]

df = pd.read_csv("data/diabetes.csv", names=columns)

print("Shape:", df.shape)

print("\nPrime 5 righe:")
print(df.head())

print("\nTipi di dato:")
print(df.dtypes)

print("\nValori nulli:")
print(df.isnull().sum())

print("\nStatistiche descrittive:")
print(df.describe())

print("\nDistribuzione Outcome:")
print(df["Outcome"].value_counts())
