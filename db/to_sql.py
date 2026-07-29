import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine


PASTA_PROCESSED = Path("../data/processed")

engine = create_engine("sqlite:///pokemon.db")
arquivos = list(PASTA_PROCESSED.glob("*.csv"))

for arquivo in arquivos:
      
        nome_tabela = arquivo.stem
        df = pd.read_csv(arquivo)
        df.to_sql(nome_tabela, con=engine, if_exists="replace", index=False)