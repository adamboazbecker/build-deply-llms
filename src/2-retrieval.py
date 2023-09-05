import os
import pathlib
from typing import List
import openai
import tiktoken
from getpass import getpass

import langchain
from langchain.docstore.document import Document
from langchain import document_loaders
from langchain.embeddings import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

QUERY = "Hi there!"


def read_openai_api_key():
  api_key = os.environ.get("OPENAI_API_KEY", None)
  if api_key is None:
    api_key = getpass("Paste your OpenAI key from: https://platform.openai.com/account/api-keys\n")

  assert api_key.startswith("sk-"), "This doesn't look like a valid OpenAI API key"
  openai.api_key = api_key



# def play_with_embeddings():
#   enc = tiktoken.encoding_for_model("NYC is the place to be")
#   print(enc)
#   print(tiktoken.encoding.decode(enc))
#
#   # we can decode the tokens one by one
#   for token_id in enc:
#     print(f"{token_id}\t{tiktoken.encoding.decode([token_id])}")
#

def load_documents(data_dir: str) -> List[Document]:
  """Load documents from a directory of markdown files

  Args:
      data_dir (str): The directory containing the markdown files

  Returns:
      List[Document]: A list of documents
  """
  md_files = list(map(str, pathlib.Path(data_dir).glob("*.md")))
  documents = [
    # Clue! Load using the UnstructuredMarkdownLoader imported above
    # [Enter the loading function]
    for file_path in md_files
  ]

  """
  Each call to `load` return the following response:
  [
    Document(page_content='the text in the document', metadata={'source': 'the/file/path.md'})
  ]
  """
  return documents


def chunk_documents():
  pass


def create_vector_store(
  documents,
  vector_store_path: str = "./vector_store",
) -> langchain.vectorstores.Chroma:
  """Create a ChromaDB vector store from a list of documents

  Args:
      documents (_type_): A list of documents to add to the vector store
      vector_store_path (str, optional): The path to the vector store. Defaults to "./vector_store".

  Returns:
      Chroma: A ChromaDB vector store containing the documents.
  """

  #
  # Clue! You should be using the OpenAI Embeddings that we imported above
  #
  vector_store = langchain.vectorstores.Chroma.from_documents(
    documents=documents,
    persist_directory=vector_store_path,
  )
  vector_store.persist()
  return vector_store


def get_relevant_documents(query, vector_store):
  docs = vector_store.get_relevant_documents(query)
  # Let's see the results
  for doc in docs:
    print(doc.metadata["source"])


def main():
  read_openai_api_key()
  # play_with_embeddings()
  documents = load_documents("./docs_sample")
  vector_store = create_vector_store(documents, vector_store_path="./vector_store")
  get_relevant_documents(QUERY, vector_store)

if __name__ == "__main__":
  main()