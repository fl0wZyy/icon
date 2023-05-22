from pretty_html_table import build_table
import tabula
import pandas as pd

def locale(value):
    value = value.replace(".","")
    return value.replace(",",".")

def extract_df(filepath):
    df = tabula.read_pdf(filepath, pages="all", silent=True)
    df_tables = []
    for table in df:
        if not table.empty:
            table_clean = table.dropna(axis=1, how='all')
            table_clean.columns = ["Šifra", "Artikl", "Količina", "Cijena", "Ukupno"]
            df_tables.append(table_clean)
    df_all = pd.concat(df_tables)
    df_all.columns = ["Šifra", "Artikl", "Količina", "Cijena", "Ukupno"]
    df_amt = df_all.drop(["Artikl","Cijena", "Ukupno"],axis=1)
    df_full = df_amt.dropna(axis=0)
    df_full = df_full.loc[df_full["Šifra"] != "VIPTABL\rE"]
    df_full= df_full.astype({"Šifra":int})
    df_full= df_full.astype({"Šifra":str})
    df_clean = df_full[df_full["Šifra"].str.isdigit()].copy()
    df_clean["Količina"] = df_clean["Količina"].apply(locale)
    return df_clean

def print_to_pdf(df, filename):
    html_table = build_table(df, 'blue_light', font_family='Open Sans, sans-serif')
    with open(f'./2.ISPIS/{filename}.html', 'w', encoding="utf-8") as f:
        f.write(html_table)