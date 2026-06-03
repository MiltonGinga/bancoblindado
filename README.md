# bancoblindado
Este projeto detalha a implementação do projeto prático “Operação Banco Blindado”, proposto pela Universidade de Luanda no âmbito da disciplina de Administração de Banco de Dados. O objetivo principal é reestruturar um ambiente de banco de dados para uma startup de e-commerce, focando em infraestrutura, segurança e continuidade de negócio.

## Requisitos e Dependências
Para executar os scripts de migração e automação, instale as dependências necessárias:
```bash
pip install pandas bcrypt
```

## Melhorias de "Blindagem Profissional"
Recentemente o projeto foi atualizado para padrões de produção:
*   **Segurança:** Substituição de SHA256 por **BCrypt** (Hashing com Salt).
*   **Resiliência:** Script de backup com política de retenção (7 dias) e simulação de upload para nuvem (AWS S3).
*   **Auditoria:** Logs detalhados de todas as operações de automação.
