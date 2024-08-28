# Installs tips
## via requirements.txt (command line)
pip install -r requirements.txt

## Build setup
( the python package build must be installed beforehand)
1) build/Modify the *.toml file
2) run $ py -m build
3) pip install C:\Git\bp-genai-fmk\dist\ragfmk-x.x.x.x-py3-none-any.whl

## Run Chroma DB
$ chroma run --host localhost --port 8000 --path C:\\chromadb

## installs via pip (see the toml file)
pip install pandas==2.2.1
pip install PyMuPDF==1.24.0
pip install langchain==0.1.13
pip install sentence-transformers==2.6.0
pip install faiss-cpu==1.8.0
pip install numpyencoder==0.3.0
pip install langchain-experimental==0.0.55
pip install chromadb-client==0.4.25.dev0
pip install Jinja2==3.1.3
pip install beautifulsoup4==4.12.3
pip install boto3==1.34.119
pip install botocore-1.34.120

# Ideas / improvements
* Need to find a way to leverage the Credential Manager for the Env. variables
* Adding for all the stack AWS services (embeddings, Textract, other LLMs - Mistral,Cohere, titan, llama -, other VDB , etc.)