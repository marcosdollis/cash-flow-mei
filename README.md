# MEI Cash Flow App

This project is a Streamlit application designed to help Microempreendedores Individuais (MEIs) manage their cash flow effectively. It allows users to record transactions, view registered entries, and analyze daily totals.

## Features

- Input form for transactions with fields for:
  - Transaction type (defaulting to "entrada")
  - Today's date
  - Value
  - Description
- Table displaying registered transactions with options to edit values
- Daily totals table to summarize transactions

## Project Structure

```
mei-cashflow-app
├── src
│   ├── app.py                  # Main entry point of the application
│   ├── components
│   │   ├── form.py             # Input form for transactions
│   │   ├── transactions_table.py # Table for registered transactions
│   │   └── daily_totals_table.py # Table for daily totals
│   └── utils
│       └── data_manager.py      # Utility functions for data management
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd mei-cashflow-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   streamlit run src/app.py
   ```

## Usage Guidelines

- Use the input form to add new transactions.
- View and edit existing transactions in the registered entries table.
- Check the daily totals table for a summary of your transactions.

## Contributing
✅ Por que anunciar com você faz sentido (e pode ser melhor que redes sociais em certos casos):
1. Atenção garantida em locais físicos
Em redes sociais, o conteúdo disputa atenção com centenas de outros posts.
Nas TVs em locais de espera, você controla o ambiente e o foco está na tela. Isso é raro e valioso.
2. Menor dispersão e mais retenção
O Instagram tem rolagem infinita e atenção fragmentada.
Em locais como lavanderias e consultórios, o tempo de exposição à mensagem é maior, o que aumenta a retenção.
3. Público local e qualificado
Redes sociais têm alcance amplo, mas muitas vezes disperso.
Você oferece acesso direto a pessoas que estão fisicamente próximas do anunciante, o que é ideal para negócios locais.
4. Custo menor por impacto real
Em redes sociais, o custo por clique ou impressão pode ser alto — e nem sempre gera conversão.
Com você, o anunciante paga por atenção real e recorrente, com menor dispersão e maior chance de retorno.
5. Integração física + digital
Você não está competindo com redes sociais — está complementando.
O ideal é usar ambos os canais, mas você oferece algo que as redes sociais não conseguem: presença física e atenção cativa.
❗ Quando redes sociais podem ser mais vantajosas:
Se o público-alvo é jovem e altamente digital, e o produto é online ou escalável, redes sociais podem ter melhor custo-benefício.
Se a empresa busca alcance nacional ou internacional, o seu canal local pode ser limitado.
🎯 Conclusão lógica
Se eu fosse uma empresa local, com foco em serviços ou produtos físicos, e quisesse atenção real, recorrente e segmentada, eu anunciaria com você. E complementaria com redes sociais para reforçar a marca.

Você oferece atenção qualificada, ambiente controlado, e exclusividade por segmento — três coisas que as redes sociais não garantem.

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.
