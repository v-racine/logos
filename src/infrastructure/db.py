from pgvector.psycopg2 import register_vector
from psycopg2.extras import execute_values
from src.domain.entities import Paper, Chunk, RetrievedChunk
from src.domain.interfaces import PaperRepository, VectorStore


class PostgresPaperRepository(PaperRepository):
    def __init__(self, conn):
        self._conn = conn

    def save_paper(self, paper: Paper) -> int:
        cur = self._conn.cursor()

        try:
            with self._conn:
                cur.execute(
                    """
                    INSERT INTO papers (title, authors, source_url, content, publication_year)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        paper.title,
                        paper.authors,
                        paper.source_url,
                        paper.content,
                        paper.publication_year,
                    ),
                )
                paper_id = cur.fetchone()[0]
                return paper_id
        finally:
            cur.close()

    def get_paper(self, paper_id: int) -> Paper:
        cur = self._conn.cursor()

        try:
            cur.execute(
                "SELECT id, title, authors, source_url, content, publication_year, ingested_at FROM papers WHERE id = %s",
                (paper_id,),
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Paper with id {paper_id} not found")
            return Paper(
                id=row[0],
                title=row[1],
                authors=row[2],
                source_url=row[3],
                content=row[4],
                publication_year=row[5],
                ingested_at=row[6],
            )
        finally:
            cur.close()

    def get_all_papers(self) -> list[Paper]:
        cur = self._conn.cursor()

        try:
            cur.execute(
                "SELECT id, title, authors, source_url, content, publication_year, ingested_at FROM papers ORDER BY id"
            )
            return [
                Paper(
                    id=row[0],
                    title=row[1],
                    authors=row[2],
                    source_url=row[3],
                    content=row[4],
                    publication_year=row[5],
                    ingested_at=row[6],
                )
                for row in cur.fetchall()
            ]
        finally:
            cur.close()


class PostgresVectorStore(VectorStore):
    def __init__(self, conn):
        self._conn = conn
        register_vector(conn)

    def save_chunks(self, chunks: list[Chunk]) -> None:
        cur = self._conn.cursor()

        try:
            values = [
                (chunk.paper_id, chunk.content, chunk.chunk_index, chunk.embedding)
                for chunk in chunks
            ]
            with self._conn:
                execute_values(
                    cur,
                    """
                    INSERT INTO chunks (paper_id, content, chunk_index, embedding)
                    VALUES %s
                    """,
                    values,
                )
        finally:
            cur.close()

    def delete_all_chunks(self) -> None:
        cur = self._conn.cursor()

        try:
            with self._conn:
                cur.execute("DELETE FROM chunks")
        finally:
            cur.close()

    def similarity_search(
        self,
        embedding: list[float],
        limit: int,
    ) -> list[RetrievedChunk]:
        cur = self._conn.cursor()

        try:
            cur.execute(
                """
                SELECT c.id, c.paper_id, c.content,
                c.chunk_index,
                1 - (c.embedding <=> %s::vector) AS similarity_score, p.title, p.authors, p.source_url, p.publication_year
                FROM chunks c
                JOIN papers p ON c.paper_id = p.id
                ORDER BY c.embedding <=> %s::vector
                LIMIT %s
                """,
                (embedding, embedding, limit),
            )
            return [
                RetrievedChunk(
                    chunk_id=row[0],
                    paper_id=row[1],
                    content=row[2],
                    chunk_index=row[3],
                    similarity_score=row[4],
                    paper_title=row[5],
                    authors=row[6],
                    source_url=row[7],
                    publication_year=row[8],
                )
                for row in cur.fetchall()
            ]
        finally:
            cur.close()
