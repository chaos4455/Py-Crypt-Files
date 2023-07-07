# py-crypt-files

O projeto py-crypt-files é uma interface GUI para criptografia de arquivos. Esta versão atual é 0.9 e pode não estar 100% funcional.

## Descrição do Projeto

O py-crypt-files é um aplicativo desenvolvido em Python com o uso da biblioteca PyQt5 para fornecer uma interface gráfica simples e intuitiva para criptografar e descriptografar arquivos. Ele permite que os usuários selecionem um arquivo local, forneçam uma senha ou gerem uma senha aleatória e realizem a criptografia ou descriptografia do arquivo selecionado.

## Funcionalidades

- Permite selecionar um arquivo para criptografar ou descriptografar.
- Gera uma senha aleatória ou permite que o usuário insira uma senha.
- Criptografa o conteúdo do arquivo selecionado usando uma chave simétrica.
- Criptografa a chave simétrica usando uma chave pública RSA.
- Salva o arquivo criptografado com a extensão .cryptfile.
- Descriptografa arquivos criptografados com a extensão .cryptfile.

Pré-requisitos
Antes de executar o projeto py-crypt-files, verifique se você possui os seguintes pré-requisitos instalados:

Python 3.x
PyQt5
cryptography
Instalação
Certifique-se de ter o Python 3.x instalado.
Instale as dependências executando o seguinte comando:
Copy code
pip install PyQt5 cryptography
Baixe ou clone este repositório para o seu ambiente local.
Uso
Abra um terminal e navegue até o diretório onde o projeto está localizado.
Execute o seguinte comando para iniciar o aplicativo:
css
Copy code
python main.py
A interface gráfica do py-crypt-files será aberta.
Clique no botão "Selecionar Arquivo" para escolher o arquivo que você deseja criptografar ou descriptografar.
Insira uma senha no campo "Senha" ou clique em "Gerar Senha" para gerar uma senha aleatória.
Clique no botão "Criptografar" para criptografar o arquivo selecionado.
Clique no botão "Descriptografar" para descriptografar um arquivo criptografado.
Contribuição
O projeto py-crypt-files é um trabalho em andamento e as contribuições são bem-vindas. Se você deseja contribuir, siga estas etapas:

Fork este repositório.
Crie um branch para sua nova feature (git checkout -b feature/nova-feature).
Faça as alterações necessárias e adicione os commits (git commit -am 'Adicione uma nova feature').
Envie as alterações para o seu repositório fork (git push origin feature/nova-feature).
Abra uma solicitação de pull para este repositório.
Licença
Este projeto está licenciado sob a MIT License.

bash
Copy code

Certifique-se de adaptar quaisquer informações adicionais, como pré-requisitos, instruções de