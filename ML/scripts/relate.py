from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def find_related_concepts(concepts, threshold=0.70):
    if len(concepts) < 2:
        return []

    embeddings = model.encode(concepts, convert_to_tensor=True)

    related = []
    for i in range(len(concepts)):
        for j in range(i+1, len(concepts)):
            score = util.cos_sim(embeddings[i], embeddings[j]).item()
            if score >= threshold:
                related.append((concepts[i], concepts[j], round(score, 3)))

    return related
