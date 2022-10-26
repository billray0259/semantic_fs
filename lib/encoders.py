from sentence_transformers import SentenceTransformer
from transformers import pipeline
import numpy as np
from .util import ndarray_from_json


class TextEncoderPipeline:
    # TODO move model name into config
    def __init__(
        self,
        model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1",
        chunk_size=128,
    ):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = chunk_size

    # TODO use dataloader
    def __call__(self, text):
        # TODO use a better tokenizer
        tokens = self.model.tokenizer.tokenize(
            text
        )  # List[str] "hello world!" -> ["hel", "##lo", "world", "##!"] -> "hello world !"
        chunks = [
            tokens[i : i + self.chunk_size]
            for i in range(0, len(tokens), self.chunk_size)
        ]

        # TODO make this configurable (if we want to encode overlapping chunks)
        # chunks.extend([
        #     tokens[i:i+self.chunk_size]
        #     for i in range(self.chunk_size//2, len(tokens), self.chunk_size)
        # ])

        # convert the chunks of tokens back to text
        text_chunks = [
            self.model.tokenizer.convert_tokens_to_string(chunk) for chunk in chunks
        ]

        embeddings = self.model.encode(text_chunks)  # List[str] -> np.ndarray

        # return both the embeddings and the text chunks
        return text_chunks, embeddings


class QueryPipeline:
    def __init__(self, model_name="sentence-transformers/multi-qa-mpnet-base-dot-v1"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, query):
        return self.model.encode(query)

    # TODO We dont seem to use this
    def query_embeddings_dict(self, query, embeddings_dict, top_k=10):
        query_embedding = self(query)
        results = []
        for key, value in embeddings_dict.items():
            embedding = ndarray_from_json(value["embedding"])
            results.append(
                (
                    key,
                    value["filename"],
                    value["text"],
                    np.dot(query_embedding, embedding),
                )
            )
        return sorted(results, key=lambda x: x[3], reverse=True)[:top_k]


class ExtractiveQAPipeline:
    def __init__(self, model_name="deepset/roberta-base-squad2"):
        self.pipe = pipeline("question-answering", model=model_name)

    def __call__(self, query, text):
        return self.pipe(question=query, context=text)
