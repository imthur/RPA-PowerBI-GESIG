# Visualizador RPA BI

## Visão Geral
Este repositório contém um sistema automatizado de visualização de dashboards construído com Python. A ferramenta RPA (Automação Robótica de Processos) alterna entre múltiplos dashboards de BI (Business Intelligence) usando Selenium e PyAutoGUI para automatizar interações no navegador.

## Funcionalidades
- Login automático em plataformas de BI
- Alternância entre múltiplas URLs de dashboards
- Modo de visualização em tela cheia
- Sistema inteligente de pausa que detecta movimentos do mouse
- Atualização automática das páginas após múltiplos ciclos de visualização
- Sistema abrangente de registro de logs
- Utiliza o navegador Chrome

## Requisitos
- Python 3.x
- Navegador Chrome
- ChromeDriver compatível com sua versão do Chrome
- Bibliotecas Python: selenium, pyautogui, psutil, python-dotenv, webdriver-manager

## Configuração
1. Clone este repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
   ```
   USERNAME=seu_usuario
   PASSWORD=sua_senha
   LINK_1=url_do_primeiro_dashboard
   LINK_2=url_do_segundo_dashboard
   LINK_3=url_do_terceiro_dashboard
   LINK_4=url_do_quarto_dashboard
   ```
4. Certifique-se de que o arquivo `chromedriver.exe` esteja na pasta do projeto

## Como Usar
Execute o script principal:
```
python RPA_BI_V3.py
```

O programa irá:
1. Iniciar o Chrome com as configurações otimizadas
2. Fazer login com as credenciais fornecidas
3. Abrir os dashboards em abas separadas
4. Alternar entre as abas em intervalos regulares
5. Atualizar todas as abas a cada 3 ciclos completos
6. Pausar a contagem quando detectar movimentos do mouse

## Funcionamento
O sistema opera em ciclos, exibindo cada dashboard por aproximadamente 30 segundos antes de alternar para o próximo. Quando detecta movimentos do mouse, o sistema pausa a contagem, permitindo a interação manual com o dashboard atual. A contagem é retomada após 15 segundos de inatividade do mouse.

A cada 3 ciclos completos, todas as abas são atualizadas para garantir que os dados estejam sempre atualizados.

## Solução de Problemas
- Verifique o arquivo `rpa.log` para informações detalhadas sobre erros
- Certifique-se de que o ChromeDriver é compatível com sua versão do Chrome
- Ajuste as coordenadas de clique no script se sua resolução de tela for diferente
- Em caso de falhas no login, verifique se as credenciais no arquivo `.env` estão corretas

## Observações Importantes
- O script utiliza coordenadas absolutas para cliques, que podem precisar de ajustes dependendo da resolução do monitor
- Antes de iniciar, o programa encerra qualquer instância existente do ChromeDriver
- O modo de tela cheia (F11) é ativado automaticamente para melhor visualização
