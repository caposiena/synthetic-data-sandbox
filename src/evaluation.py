import pandas as pd

from src.preprocessing import load_data, preprocess_data


def compare_datasets():
    real_df = load_data()

    processed, imputer, scaler = preprocess_data(real_df)

    feature_columns = [
        column
        for column in processed.columns
        if column != "Outcome"
    ]

    real_features_original_scale = scaler.inverse_transform(
        processed[feature_columns]
    )

    clean_real_df = pd.DataFrame(
        real_features_original_scale,
        columns=feature_columns
    )

    clean_real_df["Outcome"] = real_df["Outcome"].values

    synthetic_df = pd.read_csv(
        "output/synthetic_diabetes.csv"
    )

    rows = []

    for column in feature_columns:
        rows.append(
            {
                "Feature": column,
                "Real mean": clean_real_df[column].mean(),
                "Synthetic mean": synthetic_df[column].mean(),
                "Real std": clean_real_df[column].std(),
                "Synthetic std": synthetic_df[column].std(),
            }
        )

    comparison = pd.DataFrame(rows)

    print("\nConfronto media e deviazione standard:")
    print(
        comparison.round(3).to_string(index=False)
    )

    print("\nOutcome reale:")
    print(
        clean_real_df["Outcome"]
        .value_counts(normalize=True)
        .sort_index()
        .round(3)
    )

    print("\nOutcome sintetico:")
    print(
        synthetic_df["Outcome"]
        .value_counts(normalize=True)
        .sort_index()
        .round(3)
    )


if __name__ == "__main__":
    compare_datasets()
