"""Pinned real database adapters; no embedding downloads or LLM calls."""
import hashlib
import json
import re
import sqlite3
import uuid

def vector(key):
    # Deterministic token hashes isolate state-mutation behavior from model quality.
    values=[0.0]*32
    for token in re.findall(r"\w+",key.lower()):values[int.from_bytes(hashlib.sha256(token.encode()).digest()[:2],"big")%32]+=1
    return values

def payload(doc):return {"id":doc["id"],"tenant":doc["tenant"],"key":doc["key"],"value":doc["value"],"revision":doc["revision"]}

class SQLiteAdapter:
    version=sqlite3.sqlite_version
    def __init__(self):
        self.db=sqlite3.connect(":memory:");self.db.execute("CREATE VIRTUAL TABLE memories USING fts5(id UNINDEXED, tenant UNINDEXED, key, body UNINDEXED)")
    def upsert(self,doc):
        self.delete(doc["id"]);self.db.execute("INSERT INTO memories VALUES(?,?,?,?)",(doc["id"],doc["tenant"],doc["key"],json.dumps(payload(doc))))
    def delete(self,id):self.db.execute("DELETE FROM memories WHERE id=?",(id,))
    def retrieve(self,query,scope=True):
        expression='"'+query['key'].replace('"','""')+'"'
        sql="SELECT body FROM memories WHERE memories MATCH ?";params=[expression]
        if scope:sql+=" AND tenant=?";params.append(query["tenant"])
        return [json.loads(row[0]) for row in self.db.execute(sql,params) if json.loads(row[0])["key"]==query["key"]]
    def close(self):self.db.close()

class ChromaAdapter:
    def __init__(self):
        import chromadb
        from chromadb.config import Settings
        self.version=chromadb.__version__;self.client=chromadb.EphemeralClient(Settings(anonymized_telemetry=False));self.name="bb-"+uuid.uuid4().hex
        self.collection=self.client.create_collection(self.name,embedding_function=None)
    def upsert(self,doc):self.collection.upsert(ids=[doc["id"]],embeddings=[vector(doc["key"])],documents=[doc["value"]],metadatas=[payload(doc)])
    def delete(self,id):self.collection.delete(ids=[id])
    def retrieve(self,query,scope=True):
        where={"$and":[{"key":query["key"]},{"tenant":query["tenant"]}]} if scope else {"key":query["key"]}
        count=self.collection.count()
        if not count:return []
        result=self.collection.query(query_embeddings=[vector(query["key"])],n_results=min(32,count),where=where,include=["metadatas"])
        return result["metadatas"][0]
    def close(self):self.client.delete_collection(self.name)

class QdrantAdapter:
    def __init__(self):
        import importlib.metadata
        from qdrant_client import QdrantClient,models
        self.models=models;self.version=importlib.metadata.version("qdrant-client");self.client=QdrantClient(":memory:")
        self.client.create_collection("memories",vectors_config=models.VectorParams(size=32,distance=models.Distance.COSINE))
    def point_id(self,id):return str(uuid.uuid5(uuid.NAMESPACE_URL,id))
    def upsert(self,doc):self.client.upsert("memories",points=[self.models.PointStruct(id=self.point_id(doc["id"]),vector=vector(doc["key"]),payload=payload(doc))],wait=True)
    def delete(self,id):self.client.delete("memories",points_selector=self.models.PointIdsList(points=[self.point_id(id)]),wait=True)
    def retrieve(self,query,scope=True):
        must=[self.models.FieldCondition(key="key",match=self.models.MatchValue(value=query["key"]))]
        if scope:must.append(self.models.FieldCondition(key="tenant",match=self.models.MatchValue(value=query["tenant"])))
        return [point.payload for point in self.client.query_points("memories",query=vector(query["key"]),query_filter=self.models.Filter(must=must),limit=32,with_payload=True).points]
    def close(self):self.client.close()

ADAPTERS={"sqlite_fts5":SQLiteAdapter,"chroma":ChromaAdapter,"qdrant_local":QdrantAdapter}
