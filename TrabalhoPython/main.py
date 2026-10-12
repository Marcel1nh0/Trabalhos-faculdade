import os
import pandas as pd
import matplotlib.pyplot as plt
import banco


def pausar():
    input("Pressione enter para continuar")

def tratarDados():
    dados = pd.read_csv("Atividade2.csv")
    print("=== ANÁLISE INICIAL ===")
    print(f"Quantidade de registros: {dados.shape[0]}")
    print(f"Quantidade de colunas: {dados.shape[1]}")
    print(f"Colunas: {list(dados.columns)}")
    pausar()
    print("\nTipos de dados:")
    print(dados.dtypes)
    pausar()
    print("\nDados ausentes por coluna:")
    print(dados.isnull().sum())
    pausar()
    print("====Importante====")
    print(dados.value_counts())
    print(f"\nTotal de linhas com algum dado ausente: {dados.isnull().any(axis=1).sum()}")
    print("Preparando para tratar os dados incorretos")
    print("Removendo as linhas com dados faltando e truncamento de idades")
    dadosLimpos = dados.dropna()
    dadosLimpos = dadosLimpos[dadosLimpos["smoking_status"] != "Unknown"]


    print("\n=== EVIDÊNCIA DO TRATAMENTO ===")
    print(f"Registros antes: {len(dados)} | depois: {len(dadosLimpos)}")
    print("Dados ausentes após o tratamento:")
    print(dadosLimpos.isnull().sum())
    pausar()
    return dadosLimpos

def analise(dados):

    dadosAVC = dados[dados["stroke"] == 1].copy()
    dadosNAVC = dados[dados["stroke"] == 0].copy()


    resumo = dados.groupby("stroke").agg(
        pacientes=("stroke", "count"),
        idade_media=("age", "mean"),
        idade_mediana=("age", "median"),
        bmi_medio=("bmi", "mean"),
        bmi_mediano=("bmi", "median"),
        glicose_media=("avg_glucose_level", "mean"),
        glicose_mediana=("avg_glucose_level", "median"),
        hipertensao_pct=("hypertension", lambda x: x.mean() * 100),
        cardiaca_pct=("heart_disease", lambda x: x.mean() * 100),
    )


    tabaco = pd.crosstab(dados["stroke"], dados["smoking_status"], normalize="index") * 100

    sem, com = resumo.loc[0], resumo.loc[1]

    def linha(nome, a, b, fmt=".1f", sufixo=""):
        print(f"{nome:<26}{format(a, fmt) + sufixo:>12}{format(b, fmt) + sufixo:>12}")

    print("\n" + "=" * 50)
    print("ANÁLISE EXPLORATÓRIA: AVC vs SEM AVC")
    print("=" * 50)
    print(f"{'':<26}{'COM AVC':>12}{'SEM AVC':>12}")
    linha("Pacientes", com["pacientes"], sem["pacientes"], fmt=".0f")
    pausar()
    print("\n--- Idade (anos) ---")
    linha("Média", com["idade_media"], sem["idade_media"])
    linha("Mediana", com["idade_mediana"], sem["idade_mediana"])
    pausar()
    print("\n--- IMC (BMI) ---")
    linha("Média", com["bmi_medio"], sem["bmi_medio"])
    linha("Mediana", com["bmi_mediano"], sem["bmi_mediano"])
    pausar()
    print("\n--- Glicose média ---")
    linha("Média", com["glicose_media"], sem["glicose_media"])
    linha("Mediana", com["glicose_mediana"], sem["glicose_mediana"])
    pausar()
    print("\n--- Condições (% do grupo) ---")
    linha("Hipertensão", com["hipertensao_pct"], sem["hipertensao_pct"], sufixo="%")
    linha("Doença cardíaca", com["cardiaca_pct"], sem["cardiaca_pct"], sufixo="%")
    pausar()
    print("\n--- Tabagismo (% do grupo) ---")
    print(f"Quantidade total de pacientes sem avc:{len(dadosNAVC)}\nQuantidade total de pacientes com avc:{len(dadosAVC)}")
    for categoria in tabaco.columns:
        linha(categoria, tabaco.loc[1, categoria], tabaco.loc[0, categoria], sufixo="%")
    print("=" * 50)
    pausar()

    return resumo, tabaco

def visualizar(dados):
    #Gráfico 1: distribuição das idades com avc
    dadosAVC = dados[dados["stroke"] == 1]


    faixas = pd.cut(
        dadosAVC["age"],
        bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        labels=["0-9", "10-19", "20-29", "30-39", "40-49",
                "50-59", "60-69", "70-79", "80-89", "90-99"],
        right=False
    )
    idades = faixas.value_counts().sort_index()

    print("\nGerando Gráfico 1: distribuição das idades")
    pausar()
    idades.plot(kind="bar")
    plt.title("Distribuição das Idades dos Pacientes com AVC")
    plt.xlabel("Faixa de Idade (anos)")
    plt.ylabel("Quantidade de Pacientes")
    plt.savefig("grafico1_idades.png")
    plt.show()

    # Gráfico 2: hipertensão com AVC vs sem AVC

    hipertensao = dados.groupby("stroke")["hypertension"].mean() * 100
    hipertensao = hipertensao.rename(index={0: "Sem AVC", 1: "Com AVC"})

    print("\nGerando Gráfico 2: hipertensão")
    pausar()
    hipertensao.plot(kind="bar")
    plt.title("Pacientes com Hipertensão: Com AVC vs Sem AVC")
    plt.xlabel("Grupo")
    plt.ylabel("Pacientes com Hipertensão (%)")
    plt.xticks(rotation=0)
    plt.savefig("grafico2_hipertensao.png")
    plt.show()

    #Gráfico 3: tabagismo com AVC vs sem AVC
    tabagismo = pd.crosstab(dados["smoking_status"], dados["stroke"], normalize="columns") * 100
    tabagismo = tabagismo.rename(columns={0: "Sem AVC", 1: "Com AVC"})

    print("\nGerando Gráfico 3: tabagismo")
    pausar()
    tabagismo.plot(kind="bar")
    plt.title("Situação de Tabagismo: Com AVC vs Sem AVC")
    plt.xlabel("Situação de Tabagismo")
    plt.ylabel("Pacientes do Grupo (%)")
    plt.xticks(rotation=0)
    plt.legend(title="Grupo")
    plt.savefig("grafico3_tabagismo.png")
    plt.show()

def main():
    while True:
        print("\n=== MENU ===")
        print("1 - Tratar dados e executar tudo")
        print("2 - Consultar o banco SQLite")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            print("Iniciando primeira fase(tratamento de dados)")
            pausar()
            dadosLimpos = tratarDados()

            analise(dadosLimpos)
            visualizar(dadosLimpos)
            print("\nSalvando no banco de dados")
            banco.criar_banco()
            banco.inserir_dados(dadosLimpos)
            pausar()
            banco.consultar(pausar)

        elif opcao == "2":
            if os.path.exists(banco.NOME_BANCO):
                banco.consultar(pausar)
            else:
                print("Banco ainda não existe, execute a opção 1 primeiro")

        elif opcao == "0":
            print("Encerrando")
            break

        else:
            print("Opção inválida")


if __name__ == "__main__":
    main()