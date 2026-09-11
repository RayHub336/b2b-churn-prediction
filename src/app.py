from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

# Inicializar la aplicación
app = FastAPI(title="B2B Churn Prediction API", version="1.0")

# 1. Cargar los activos matemáticos en memoria al iniciar el servidor
preprocessor = joblib.load('src/preprocessor.joblib')
model = joblib.load('src/lgbm_model.joblib')
OPTIMIZED_THRESHOLD = 0.60

# 2. Definir el esquema de datos (Contrato B2B de entrada)
class CustomerData(BaseModel):
    gender: str = "Female"
    SeniorCitizen: int = 0
    Partner: str = "Yes"
    Dependents: str = "No"
    Type: str = "Month-to-month"
    PaperlessBilling: str = "Yes"
    PaymentMethod: str = "Electronic check"
    MonthlyCharges: float = 29.85
    TotalCharges: float = 29.85
    MultipleLines: str = "No Phone"
    InternetService: str = "DSL"
    OnlineSecurity: str = "No"
    OnlineBackup: str = "Yes"
    DeviceProtection: str = "No"
    TechSupport: str = "No"
    StreamingTV: str = "No"
    StreamingMovies: str = "No"
    tenure_days: int = 30

# 3. Endpoint de consumo B2B
@app.post("/predict")
def predict_churn(customer: CustomerData):
    # Convertir JSON a DataFrame de una fila
    df_input = pd.DataFrame([customer.model_dump()])
    
    # Preprocesamiento (Escalado y OneHotEncoding)
    X_processed = preprocessor.transform(df_input)
    
    # Predicción de probabilidad
    probabilidad = model.predict_proba(X_processed)[0][1]
    
    # Toma de decisión operativa
    is_churn = bool(probabilidad >= OPTIMIZED_THRESHOLD)
    nivel_riesgo = "Alto - Riesgo de Fuga" if is_churn else "Bajo - Retenido"
    
    return {
        "probabilidad_churn": round(probabilidad, 4),
        "alerta_operativa": nivel_riesgo,
        "accion_sugerida": "Desplegar campaña de retención" if is_churn else "Mantener monitoreo"
    }