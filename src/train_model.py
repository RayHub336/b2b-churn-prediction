import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import f1_score, roc_auc_score
from lightgbm import LGBMClassifier
from data_prep import prep_data

def train_and_evaluate():
    # 1. Obtener datos limpios
    df = prep_data()

    X = df.drop('Churn', axis=1)
    y = df['Churn']

    # 2. Split Estratificado
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X_train.select_dtypes(include=['object']).columns.tolist()

    # 3. Pipeline de Preprocesamiento
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_cols),
            ('cat', OneHotEncoder(drop='first', handle_unknown='error'), categorical_cols)
        ])

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    # 4. Entrenamiento del modelo (Gradient Boosting)
    print("Entrenando modelo LightGBM para predicción de Churn...")
    lgbm = LGBMClassifier(
        random_state=42, 
        class_weight='balanced',
        n_estimators=200,
        learning_rate=0.05,
        max_depth=5
    )
    lgbm.fit(X_train_processed, y_train)

    # 5. Evaluación y Optimización de Umbral
    y_probs_lgbm = lgbm.predict_proba(X_test_processed)[:, 1]
    roc_auc = roc_auc_score(y_test, y_probs_lgbm)

    best_f1 = 0
    best_thresh = 0.5
    for thresh in np.arange(0.1, 0.9, 0.05):
        preds_adjusted = (y_probs_lgbm >= thresh).astype(int)
        current_f1 = f1_score(y_test, preds_adjusted)
        if current_f1 > best_f1:
            best_f1 = current_f1
            best_thresh = thresh

    print(f"ROC-AUC Score: {roc_auc:.4f}")
    print(f"F1-Score Máximo: {best_f1:.4f} (Usando umbral optimizado de {best_thresh:.2f})")

if __name__ == "__main__":
    train_and_evaluate()