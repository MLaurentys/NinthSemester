import pandas as pd

def map_values(x):
    x = x.upper()
    if x == "NÃO DETECTADO" or x == "NÃO DETECTADO (NEGATIVO)" or\
       x == "NÃO REAGENTE" or x == "NEGATIVA":
        return '0'
    elif x == "DETECTADO" or x == "DETECTADO (POSITIVO)" or\
         x == "REAGENTE"  or x == "POSITIVA":
        return '1'
    return x

def is_real(x):
    try:
        a = float(x)
    except:
        return False
    return True

# Load csv files
df_exame_raw = pd.read_csv("dados/raw/added/fleury/dataset_exames.csv", '|',\
                encoding='latin-1')
df_paciente_raw = pd.read_csv("dados/raw/added/fleury/dataset_pacientes.csv",\
                '|', encoding='latin-1')

for df in [df_exame_raw, df_paciente_raw]:
    df.drop_duplicates(inplace=True)

# Maps some results to 0/1
df_exame_raw.DE_RESULTADO = df_exame_raw.DE_RESULTADO.apply(lambda x: map_values(x))

# Drops column I considered useless
del df_paciente_raw['CD_PAIS']
del df_paciente_raw['CD_UF']
del df_paciente_raw['CD_MUNICIPIO']
del df_paciente_raw['CD_CEP']
del df_exame_raw['DE_ORIGEM']

# Used to simplify conversion
df_exame_raw.DE_RESULTADO = df_exame_raw.DE_RESULTADO.str.replace(",", ".")

# Remove rows whose exam's result is not numerical
df_exame_raw = df_exame_raw[df_exame_raw['DE_RESULTADO'].apply(lambda x: is_real(x))]

# Removes exams that very few people made
LIMIAR = 0.98
amt_people = df_paciente_raw.shape[0]
df_exame_aux = df_exame_raw\
                .groupby(['DE_EXAME','DE_ANALITO'])\
                .filter(lambda x : len(x)>((1-LIMIAR)*amt_people))

# Generates CSV
exam_count = df_exame_aux.copy()
exam_count = exam_count\
                .groupby(['DE_EXAME','DE_ANALITO', 'DE_RESULTADO'])\
                .size()\
                .reset_index(name="COUNT")
exam_count = exam_count.sort_values(by="COUNT")
exam_count.reset_index()[['DE_EXAME','DE_ANALITO', 'DE_RESULTADO', 'COUNT']]\
            .to_csv('teste.csv')

# Joins the two tables
df = df_paciente_raw.merge(df_exame_aux, on='ID_PACIENTE', how='inner')