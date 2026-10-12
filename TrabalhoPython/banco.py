import sqlite3
from contextlib import closing

NOME_BANCO = "avc.db"

COLUNAS = ["id", "gender", "age", "hypertension", "heart_disease", "ever_married",
           "work_type", "Residence_type", "avg_glucose_level", "bmi",
           "smoking_status", "stroke"]


def criar_banco():
    with closing(sqlite3.connect(NOME_BANCO)) as conn:
        conn.execute("DROP TABLE IF EXISTS pacientes")  # evita duplicar se rodar duas vezes
        conn.execute("""
            CREATE TABLE pacientes (
                id                INTEGER PRIMARY KEY,
                gender            TEXT,
                age               REAL,
                hypertension      INTEGER,
                heart_disease     INTEGER,
                ever_married      TEXT,
                work_type         TEXT,
                Residence_type    TEXT,
                avg_glucose_level REAL,
                bmi               REAL,
                smoking_status    TEXT,
                stroke            INTEGER
            )
        """)
        conn.commit()
    print(f"Banco '{NOME_BANCO}' e tabela 'pacientes' criados")


def inserir_dados(dados):
    registros = list(dados[COLUNAS].itertuples(index=False, name=None))
    marcadores = ",".join("?" * len(COLUNAS))
    with closing(sqlite3.connect(NOME_BANCO)) as conn:
        conn.executemany(f"INSERT INTO pacientes VALUES ({marcadores})", registros)
        conn.commit()
    print(f"{len(registros)} registros inseridos")


def consultar(pausar):
    with closing(sqlite3.connect(NOME_BANCO)) as conn:
        # Consulta 1: total de registros
        total = conn.execute("SELECT COUNT(*) FROM pacientes").fetchone()[0]
        print(f"\n[1] Total de registros armazenados: {total}")
        pausar()

        # Consulta 2: pacientes com AVC
        qtd_avc = conn.execute("SELECT COUNT(*) FROM pacientes WHERE stroke = 1").fetchone()[0]
        print(f"\n[2] Pacientes com registro de AVC: {qtd_avc}")
        print("Primeiros 10:")
        for linha in conn.execute(
            "SELECT id, gender, age, hypertension, smoking_status "
            "FROM pacientes WHERE stroke = 1 LIMIT 10"
        ):
            print(linha)
        pausar()

        # Consulta 3: taxa de AVC por situação de tabagismo
        print("\n[3] Taxa de AVC por situação de tabagismo:")
        print(f"{'tabagismo':<18}{'pacientes':>10}{'com AVC':>10}{'taxa %':>9}")
        for fumo, n, avc, taxa in conn.execute("""
            SELECT smoking_status,
                   COUNT(*),
                   SUM(stroke),
                   ROUND(100.0 * SUM(stroke) / COUNT(*), 2)
            FROM pacientes
            GROUP BY smoking_status
            ORDER BY 4 DESC
        """):
            print(f"{fumo:<18}{n:>10}{avc:>10}{taxa:>9}")
        pausar()