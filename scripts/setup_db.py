import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

try:
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    print("✓ pgvector extension enabled")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            id          SERIAL PRIMARY KEY,
            title       TEXT NOT NULL,
            authors     TEXT,
            source_url  TEXT NOT NULL,
            content     TEXT NOT NULL,
            ingested_at TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    print("✓ papers table created")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id          SERIAL PRIMARY KEY,
            paper_id    INTEGER NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
            content     TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            embedding   vector(1536),
            created_at  TIMESTAMPTZ DEFAULT NOW()
        );
    """)
    print("✓ chunks table created")

    cur.execute("""
          CREATE INDEX IF NOT EXISTS chunks_embedding_idx
          ON chunks
          USING hnsw (embedding vector_cosine_ops);
      """)
    print("✓ vector similarity index created")

    conn.commit()
    print("\n✓ Database setup complete!")

except Exception as e:
    print("Error during setup:", e)
    conn.rollback()

finally:
    cur.close()
    conn.close()
