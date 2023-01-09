# QA Gerdau Rolling

Este documento apresenta um tutorial sobre como instalar e configurar o ambiente pela primeira vez, instalar a atualizar as dependências, bem como rodar os testes e scripts.

---

***Aviso 1***: Este tutorial foi criado e testado no Ubuntu. Se você não está usando uma distribuição Linux, alguns passos poderão ser diferentes e não estão cobertos neste documento.

***Aviso 2***: Este repositório usa Git LFS, portanto, deve ser clonado apenas usando HTTP. Porém, as dependências utilizando SSH, então é necessário que exista uma chave SSH válida e habilitada (***trusted***) cadastrada no Azure Devops para a correta instalação. Se você clonou usando SSH, provavelmente ocorreram erros, e de qualquer forma, recomenda-se apagar a versão clonada e repetir a operação usando HTTP.

## Importante

Este repositório é feito para testar o repositório [science_gerdau_rolling](https://dev.azure.com/azure0511/ENACOM/_git/science_gerdau_rolling). Portanto, é necessário que os usuários desse repositório tenham familiaridade com o mesmo e possam debugar e identificar possíveis erros que ocorram no repositório que será testado, bem como os erros que ocorram nesse resultado, de modo que ambos estejam funcionando corretamente e estejam coerentes para que os testes sejam feitos adequadamente.

## Pré-requisitos

* Python 3.10+
* Pip 3.10+
* Poetry
* Git LFS
* Poedit

# Configuração do Ambiente

## Instalando o python3.10+

Este rápido tutorial irá mostrar-lhe como instalar a versão mais recente
Python 3.10+ no Ubuntu.

* Abra o terminal via Ctrl+Alt+T ou procurando por “Terminal” em lançador de aplicativos. Quando ele abrir, execute os comandos:

### Instalando o Python 3.10 no Ubuntu 20.04|18.04 usando o Apt Repo

```shell
$ sudo apt-get install software-properties-common -y
$ sudo add-apt-repository ppa:deadsnakes/ppa
$ sudo apt-get install python3.10 -y
```

Agora você tem pelo menos uma versão do Python 3.10 instalada, use o comando ***python*** para a versão 2.x (se ainda estiver instalada),
***python3*** para a versão principal usada no sistema operacional e ***python3.10*** para a versão 3.10.x. Talvez seja necessário tornar a versão ***3.10*** como a principal, o que pode ser feito seguindo os passos neste [tutorial](https://www.folkstalk.com/tech/set-python-3-as-default-ubuntu-with-code-examples/).

Para verificar se funcionou digite:

```shell
python3.10 --version
```

A saída no terminal deve ser algo do tipo:

Python 3.10.7

## Instalando pip

Pip é um sistema de gerenciamento de pacotes usado para instalar e gerenciar pacotes de software escritos em Python.

Recomenda-se instalar a versão mais recente do pip3.10:

```shell
$ sudo curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```

e teste o resultado da instalação:

```shell
$ python3.10 -m pip --version
```

e após isso, dê um upgrade na versão do pip instalada

```shell
$ python3.10 -m pip install --upgrade pip
```

## Instalando o Poetry

Para instalar o Poetry, gerenciador de dependências utilizado neste repositório, basta executar o comando após a instalação do Python3.10 e pip:

```shell
$ sudo curl -sSL https://install.python-poetry.org | python3 -
```

## Instalando o Git LFS

O Git LFS substitui arquivos grandes com ponteiros para esses arquivos, armazenando seus conteúdos em um servidor remoto, evitando operações Git demoradas e ineficientes. 

Para instalar o Git LFS, execute os seguintes comandos:

```shell
$ curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

```

```shell
$ sudo apt-get install git-lfs -y
```

```shell
$ git lfs install
```

Caso você tenha clonado este repositório usando HTTP, instalado o Git LFS, e ao abrir arquivos do tipo *json* ou planilhas, apenas um pequeno texto relacionado ao Git LFS esteja aparecendo no lugar do conteúdo, é necessário carregar os arquivos novamente. Para isso, basta clonar o repositório novamente, ou apenas apagar todo seu conteúdo e digitar o seguinte comando:

```shell
$ git reset --hard
```

## Instalando o Poedit

Poedit é um *shareware* e editor de catálogo *gettext* multiplataforma para auxiliar no processo de localização de idiomas.

Para instalar o Poedit, execute o seguinte comando:


```shell
$ sudo apt-get install poedit -y
```

## Versionamento de Dependências e Instalação

Todas as dependências utilizadas são versionadas no arquivo 'pyproject.toml', na raiz da pasta do projeto.

Normalmente, os comandos são feitos utilizando o Poetry, porém, esse projeto requer algumas mudanças na instalação, portanto, as instruções serão rodadas atraveś de um arquivo Makefile.

Para instalar o projeto com a última versão do repositório de teste, habilite o ambiente virtual:

```shell
$ poetry shell
```

e execute o comando:

```shell
$ make build
```

## Execução dos Testes

Para executar os testes, basta utilizar alguma ferramenta de testes da IDE que esteja utilizando, ou rodar os seguintes comandos:

Caso o ambiente virtual esteja desabilitado:

```shell
$ poetry shell
```

Executando os testes:

```shell
$ make test
```

Os resultados dos testes são salvos nas seguintes pastas:

* Arquivos json

    *qa_gerdau_rolling/data/json_files/output_json_files*

* Planilhas

    *qa_gerdau_rolling/data/sheet_files/output_sheet_files*


# Testando uma branch

Para testar uma branch do repositório [science_gerdau_rolling](https://dev.azure.com/azure0511/ENACOM/_git/science_gerdau_rolling), é preciso que a dependência no arquivo ***pyproject.toml*** esteja apontando para a branch. Abaixo, está a dependência padrão, apontando para develop.

```toml
science_gerdau_rolling = { git = "git@ssh.dev.azure.com:v3/azure0511/ENACOM/science_gerdau_rolling", rev = "develop" }
```

Para apontar para a branch a ser testada, mude o valor de ***rev*** para o nome da branch. Para testar uma branch *feature/test_new_method*, ficaria assim:

```toml
science_gerdau_rolling = { git = "git@ssh.dev.azure.com:v3/azure0511/ENACOM/science_gerdau_rolling", rev = "feature/test_new_method" }
```

Após isso, basta instalar o projeto:

```shell
make build
```

e rodar os testes:

```shell
make test
```

# Autores

* **Matheus Anjos** - [matheus.anjos@enacom.com.br](mailto:matheus.anjos@enacom.com.br)
