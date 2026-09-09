import pandas as pd

def prep_data():
    # 1. Carga de datos (asumiendo que corres el script desde la raíz)
    df_personal = pd.read_csv('data/personal.csv')
    df_contract = pd.read_csv('data/contract.csv')
    df_phone = pd.read_csv('data/phone.csv')
    df_internet = pd.read_csv('data/internet.csv')

    # 2. Consolidación
    df = df_personal.merge(df_contract, on='customerID', how='left')
    df = df.merge(df_phone, on='customerID', how='left')
    df = df.merge(df_internet, on='customerID', how='left')

    # 3. Imputación de nulos
    cols_internet = ['InternetService', 'OnlineSecurity', 'OnlineBackup', 
                     'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    df[cols_internet] = df[cols_internet].fillna('No Internet')
    df['MultipleLines'] = df['MultipleLines'].fillna('No Phone')

    # 4. Corrección de tipos
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    df['Churn'] = (df['EndDate'] != 'No').astype(int)

    # 5. Ingeniería de características (Antigüedad)
    df['BeginDate'] = pd.to_datetime(df['BeginDate'], format='mixed')
    df['EndDate_temp'] = df['EndDate'].replace('No', '2020-02-01')
    df['EndDate_temp'] = pd.to_datetime(df['EndDate_temp'], format='mixed')
    df['tenure_days'] = (df['EndDate_temp'] - df['BeginDate']).dt.days

    # 6. Prevención de fuga de datos
    df = df.drop(['customerID', 'BeginDate', 'EndDate', 'EndDate_temp'], axis=1)
    
    return df