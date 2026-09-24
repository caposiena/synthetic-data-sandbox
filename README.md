# Synthetic Data Sandbox

Project developed for Module 6.

The application generates synthetic tabular data using a Variational Autoencoder implemented in PyTorch.

The example dataset is the Pima Indians Diabetes dataset.

The main workflow is:

    dataset
    preprocessing
    VAE training
    synthetic data generation
    statistical comparison

The project also includes a FastAPI backend, a Streamlit interface and an optional natural language analysis feature.

## Data preparation

Some medical variables in the dataset contain zero values that are treated as missing values.

These values are replaced with the median.

The numerical features are then scaled between 0 and 1 with MinMaxScaler.

The Outcome column is kept separate from the VAE training.

## VAE model

The encoder reduces the input features to a latent representation.

Two vectors are produced:

    mean
    log variance

Sampling is performed with the reparameterization trick.

The decoder reconstructs the original numerical features.

The loss combines reconstruction error and KL divergence.

A small beta value is used to reduce the tendency of the generated samples to concentrate too strongly around the average values.

Outcome is generated separately using the proportion observed in the original dataset.

## Running the project

Install the dependencies:

    pip install -r requirements.txt

Train the model:

    python -m src.train

Generate synthetic data:

    python -m src.generate

Compare real and synthetic statistics:

    python -m src.evaluation

Start the API:

    uvicorn api.main:app --reload

Start the Streamlit interface:

    streamlit run app.py

## API endpoints

    GET /status
    POST /train
    POST /generate
    GET /statistics

## Natural language analysis

The Streamlit interface includes an optional section for asking questions about the synthetic dataset.

To enable it, set the OPENAI_API_KEY environment variable before starting the application.

The API key is not stored in the repository.

## Tests

Run:

    pytest -v

## Notes

The model reproduces the average values of the original dataset reasonably well.

The generated distributions are generally less variable than the original ones. This is a limitation of the small VAE used in this project.

Synthetic data generation should not be considered a formal guarantee of anonymization.
