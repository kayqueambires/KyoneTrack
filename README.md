# KyoneTrack

KyoneTrack é uma aplicação Python que permite rastrear encomendas dos Correios e receber atualizações pelo WhatsApp usando a API Twilio.

## Créditos

- API de rastreamento dos Correios utilizada neste projeto: [chipytux/correiosApi](https://github.com/chipytux/correiosApi)
- Twilio API: [Site Oficial](https://www.twilio.com/)

## Requisitos

Para executar o KyoneTrack, você precisará das seguintes bibliotecas Python:

requests
twilio

Você pode instalá-las usando o `pip`:

pip install requests twilio

## Uso

1. Configure suas credenciais Twilio no código, substituindo `account_sid` e `auth_token` pelo SID e token de autenticação da sua conta Twilio.

2. Execute o script fornecendo o código de rastreamento como argumento:

   ```bash
   python main.py SEU_CODIGO_DE_RASTREAMENTO

Substitua SEU_CODIGO_DE_RASTREAMENTO pelo código da encomenda que deseja rastrear.

    O programa irá rastrear periodicamente a encomenda e enviar atualizações pelo WhatsApp quando houver novos eventos.

    Para encerrar o programa, abra o Gerenciador de Tarefas (Task Manager) no Windows, encontre o processo python.exe ou pythonw.exe associado ao script e termine-o.

## Executando em Segundo Plano

Você pode usar o pythonw.exe para executar o script em segundo plano:

Abra o Prompt de Comando (cmd) e navegue até a pasta do projeto.

Execute o script usando pythonw.exe:

pythonw.exe main.py SEU_CODIGO_DE_RASTREAMENTO

O script será executado em segundo plano e não exibirá uma janela de terminal.

## Suporte e Contribuições

Se encontrar problemas ou tiver sugestões para melhorar o KyoneTrack, sinta-se à vontade para abrir uma issue ou enviar um pull request.

Esperamos que esse projeto seja útil para você! Mantenha-se atualizado com as últimas atualizações dos Correios diretamente no seu WhatsApp.