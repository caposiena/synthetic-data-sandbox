from src.preprocessing import load_data, preprocess_data


def test_preprocessing_output():
    df = load_data()

    processed, imputer, scaler = preprocess_data(df)

    assert processed.shape == df.shape
    assert processed.isnull().sum().sum() == 0

    features = processed.drop(columns=["Outcome"])

    tolerance = 1e-9

    assert features.min().min() >= -tolerance
    assert features.max().max() <= 1 + tolerance

    assert set(processed["Outcome"].unique()).issubset({0, 1})
