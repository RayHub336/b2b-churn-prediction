# Motor Predictivo de Churn para Retención B2B (FastAPI / Docker)

## 1. Desafío de Negocio (Define)
La pérdida de clientes (*Churn*) representa una fuga de capital directo y un incremento en el Costo de Adquisición de Clientes (CAC). El objetivo de este proyecto es transicionar de una retención reactiva a una **retención proactiva**, desarrollando un modelo predictivo capaz de identificar anticipadamente a los usuarios en riesgo de abandono.

**KPI Objetivo:** Maximizar el *F1-Score* (> 0.80) para equilibrar la precisión en la detección y minimizar el costo de falsos positivos en campañas de retención.

## 2. Análisis de Causa Raíz (Analyze)
Antes del modelado predictivo, el análisis de datos reveló los principales cuellos de botella en la retención de la base instalada:

### Riesgo Operativo por Tipo de Contrato
Se identificó que el modelo de negocio es altamente vulnerable en los esquemas de corto plazo. La inmensa mayoría de la fuga de clientes se concentra en los contratos "Mes a Mes" (*Month-to-month*), indicando una falta de "candados" de fidelidad o problemas de satisfacción temprana.

![Fuga por Contrato](images/fuga.png)

### Perfil de Riesgo: Cargos vs. Antigüedad
Al evaluar la dispersión operativa, detectamos que el abandono está correlacionado con dos variables críticas:
1. **Facturación:** Los clientes que abandonan tienen una mediana de cargos mensuales significativamente más alta (~$80 USD).
2. **Ciclo de Vida:** La ventana de mayor riesgo (cuello de botella de retención) ocurre en los primeros 500 días de antigüedad.

![Distribución Cargos y Antigüedad](images/cargos.png)

## 3. Solución Técnica y Modelado (Improve & Control)
Para automatizar la detección de estos perfiles de riesgo, se construyó un *pipeline* de Machine Learning:

*   **Preprocesamiento:** Escalado estándar para variables numéricas y codificación OHE para variables categóricas, evitando *Data Leakage*.
*   **Modelo Final:** Ensamble de Gradient Boosting (`LightGBM`) ajustado para manejar desbalanceo de clases.
*   **Resultados de Producción:** 
    *   **ROC-AUC:** 0.8930 (Excelente capacidad de separación de clases).
    *   **F1-Score:** 0.6944 (Alcanzado mediante optimización de umbral de decisión a 0.60 para balancear Precisión y Recall).
 
### 📊 Technical Note on Model Performance & Trade-offs
El objetivo inicial planteaba un F1-Score > 0.80, alcanzando en esta versión un 0.6944. En el contexto de retención B2B, existe un trade-off de negocio crítico: los Falsos Negativos (no detectar a un cliente que se va a ir) son financieramente mucho más costosos que los Falsos Positivos (ofrecer una campaña de retención a un cliente leal). Por lo tanto, el umbral de decisión se ajustó para priorizar el Recall (capturar la mayor cantidad de deserciones reales) sobre la precisión pura del F1-Score. Aceptar esta métrica permite proteger el MRR (Monthly Recurring Revenue) de forma inmediata.

## 4. Stack Tecnológico
*   **Lenguaje:** Python 3
*   **Manipulación de Datos:** Pandas, NumPy
*   **Machine Learning:** Scikit-learn, LightGBM

## 5. Arquitectura de Despliegue (AWS EC2)
El modelo está industrializado mediante **FastAPI** y empaquetado en un contenedor de **Docker**. El archivo `deploy_ec2.sh` contiene la automatización de infraestructura (*Infrastructure as Code*) diseñada para levantar el microservicio de manera instantánea en instancias **AWS EC2**, permitiendo que los sistemas corporativos (CRM/ERP) consuman las predicciones en tiempo real vía HTTP.

### 🚀 API Endpoint Demo (No installation required)

Para facilitar la validación técnica del microservicio desplegado en AWS EC2, a continuación se muestra la estructura de interacción con la API de FastAPI. Los sistemas ERP/CRM pueden consumir el modelo enviando un payload en formato JSON.

**Sample Request (cURL):**
```bash
curl -X 'POST' \
  'http://<AWS_EC2_IP>:8000/predict_churn' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "client_id": "C-98342",
  "contract_type": "Month-to-month",
  "tenure_months": 12,
  "monthly_charges": 89.50,
  "tech_support_calls": 3
}'

{
  "client_id": "C-98342",
  "churn_prediction": 1,
  "churn_probability": 0.84,
  "risk_level": "Critical",
  "business_action": "Trigger automated retention campaign (Discount Tier 1)"
}

### 💼 Business Impact & What I Would Do Next

Business Impact: Permite a los equipos de ventas y Customer Success identificar proactivamente cuentas B2B en riesgo antes de que cancelen el servicio, protegiendo el flujo de ingresos.

Next Steps for Iteration: (1) Implementar SMOTE para manejar el desbalanceo severo de clases. (2) Transicionar a un modelo basado en árboles (XGBoost) para capturar relaciones no lineales más complejas y subir el F1-Score por encima de 0.80.
