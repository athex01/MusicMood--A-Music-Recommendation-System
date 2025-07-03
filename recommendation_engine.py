import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder

# Load the datasets
data_df = pd.read_csv("Data.csv")  # Replace with the correct path to Data.csv
target_df = pd.read_csv("Target.csv")  # Replace with the correct path to Target.csv

# Combine datasets
data_df['Song'] = target_df['Song']

# Encode categorical features
label_encoders = {}
for column in ['Genre', 'Mood', 'Language', 'Age']:
    le = LabelEncoder()
    data_df[column] = le.fit_transform(data_df[column])
    label_encoders[column] = le

# Prepare features (X) and target (y)
X = data_df[['Genre', 'Mood', 'Language', 'Age']]
y = data_df['Song']

# Train the Nearest Neighbors model
nn = NearestNeighbors(n_neighbors=5, metric='euclidean')
nn.fit(X)


def recommend_songs(genre, mood, language, age):
    """Get top 3 song recommendations."""
    try:
        encoded_inputs = [
            label_encoders['Genre'].transform([genre])[0],
            label_encoders['Mood'].transform([mood])[0],
            label_encoders['Language'].transform([language])[0],
            label_encoders['Age'].transform([age])[0],
        ]
        input_df = pd.DataFrame([encoded_inputs], columns=['Genre', 'Mood', 'Language', 'Age'])
        distances, indices = nn.kneighbors(input_df)
        recommendations = y.iloc[indices[0]].tolist()
        return recommendations[:3]
    except KeyError as e:
        return f"Invalid input: {e}. Please check your values."
    except ValueError as e:
        return f"Invalid input: {e}. Ensure values match the dataset categories."

# Export variables for import
__all__ = ['recommend_songs', 'label_encoders']
