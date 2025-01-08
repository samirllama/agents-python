# ingest.py
import os
from dotenv import load_dotenv
import pandas as pd
from upstash_vector import Index
from halo import Halo  # Python equivalent of ora for spinners
import sys
from pathlib import Path
from openai import AsyncOpenAI
from utils.db import MetadataDB

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Initialize Upstash Vector client
index = Index(
    url=os.getenv("UPSTASH_VECTOR_REST_URL") or "",
    token=os.getenv("UPSTASH_VECTOR_REST_TOKEN") or ""
)

async def get_embedding(text: str):
    """Get embedding for text using OpenAI API"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

async def index_movie_data():
    # Initialize spinner and database
    spinner = Halo(text='Reading movie data...', spinner='dots')
    spinner.start()
    db = MetadataDB()

    try:
        # Read and parse CSV file
        csv_path = Path(__file__).parent / 'data' / 'imdb_movie_dataset.csv'
        df = pd.read_csv(csv_path)

        spinner.text = 'Starting movie indexing...'

        # Prepare batch of vectors
        vectors = []
        # Index each movie
        for _, movie in df.iterrows():
            spinner.text = f"Indexing movie: {movie['Title']}"

            # Create text representation
            text = f"{movie['Title']}. {movie['Genre']}. {movie['Description']}"

            try:
                # Get embedding for the text
                embedding = await get_embedding(text)
                vectors.append({
                           "id": movie['Title'],
                           "vector": embedding
                       })

            except Exception as error:
                spinner.fail(f"Error indexing movie {movie['Title']}")
                print(f"Error: {str(error)}", file=sys.stderr)
                continue

        # Batch upsert
        if vectors:
            spinner.text = "Upserting vectors to database..."
            index.upsert(vectors=vectors)

        spinner.succeed('Finished indexing movie data')

    except Exception as e:
        spinner.fail(f"Failed to process movie data: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(index_movie_data())
