import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler


COLUMNS = [
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

ZERO_AS_MISSING = [
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
]


def load_data(path="data/diabetes.csv"):
    return pd.read_csv(path, names=COLUMNS)


def preprocess_data(df):
    df = df.copy()

    features = df.drop(columns=["Outcome"])
    target = df["Outcome"].copy()

    features[ZERO_AS_MISSING] = features[ZERO_AS_MISSING].replace(0, np.nan)

    imputer = SimpleImputer(strategy="median")
    imputed = imputer.fit_transform(features)

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(imputed)

    processed = pd.DataFrame(
        scaled,
        columns=features.columns
    )

    processed["Outcome"] = target.reset_index(drop=True)

    return processed, imputer, scaler


if __name__ == "__main__":
    df = load_data()

    processed, imputer, scaler = preprocess_data(df)

    print("Shape originale:", df.shape)
    print("Shape preprocessata:", processed.shape)

    print("\nValori nulli dopo preprocessing:")
    print(processed.isnull().sum())

    print("\nRange feature numeriche:")
    print(processed.drop(columns=["Outcome"]).agg(["min", "max"]))

    print("\nPrime 5 righe:")
    print(processed.head())
