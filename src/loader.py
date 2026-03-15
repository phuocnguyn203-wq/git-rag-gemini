import git
import os
from git.exc import GitCommandError

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language
def clone_repo(repo_url, local_dir="../data/repo"):
    try:
        if not os.path.exists(local_dir):
            os.makedirs(local_dir)
            print(f"Created {local_dir}")
        print(f"Cloning {repo_url} to {local_dir}")
        repo = git.Repo.clone_from(repo_url, local_dir)
        print("Cloned successfully")
        return repo
    except GitCommandError as e:
        print(f"An error occurred during cloning: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def load_repo():
    loader = GenericLoader.from_filesystem(
        "../data/repo",
        glob="**/*.py",
        suffixes=[".py"],
        parser=LanguageParser(language=Language.PYTHON, parser_threshold=500) #type: ignore
    )
    docs = loader.load()
    print(f"Loaded {len(docs)} code snippets.")
    return docs

if __name__ == "__main__":
    repo = clone_repo("https://github.com/pallets/flask.git")
    print(repo)
        