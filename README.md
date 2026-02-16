# 📊 Projet Big Data – Pipeline Kafka → Logstash → Elasticsearch → Kibana

## 🎯 Objectif

Mettre en place un pipeline temps réel permettant :

1. 📡 Collecte de données météo via API (Open-Meteo)
2. 🚀 Envoi des données vers Kafka
3. 🔄 Traitement avec Logstash
4. 📦 Stockage dans Elasticsearch
5. 📈 Analyse et visualisation dans Kibana
6. 🔎 Exécution de requêtes Elasticsearch avancées

---

# 🏗️ Architecture

```
API Open-Meteo
        ↓
   Python Producer
        ↓
      Kafka
        ↓
     Logstash
        ↓
  Elasticsearch
        ↓
      Kibana
```

---

# 🐳 Lancement du projet

```bash
docker compose up -d
```

Vérifier les services :

```bash
docker compose ps
```

Ports utilisés :

| Service       | Port |
| ------------- | ---- |
| Elasticsearch | 9200 |
| Kibana        | 5601 |
| Kafka         | 9092 |

---

# 📂 Structure du projet

```
collector/
    producer.py

logstash/
    pipeline.conf

elasticsearch_queries/
    1_match.json
    2_aggregation.json
    3_ngram.json
    4_fuzzy.json
    5_timeseries.json

Results/
    1_match_result.json
    2_aggregation_result.json
    3_ngram_result.json
    4_fuzzy_result.json
    5_timeseries_result.json

template.json
docker-compose.yml
```

---

# 🔎 Requêtes Elasticsearch

---

## 1️⃣ Requête Textuelle (Match)

Fichier : `1_match.json`

```json
{
  "query": {
    "match": {
      "description": "live_weather"
    }
  }
}
```

✔ Résultat : retourne tous les événements météo.

---

## 2️⃣ Agrégation – Température moyenne par ville

Fichier : `2_aggregation.json`

```json
{
  "size": 0,
  "aggs": {
    "par_ville": {
      "terms": { "field": "city.keyword", "size": 10 },
      "aggs": {
        "temp_moy": { "avg": { "field": "temp" } }
      }
    }
  }
}
```

✔ Résultat : moyenne des températures pour chaque ville.

---

## 3️⃣ Recherche N-gram (Auto-complétion)

Fichier : `3_ngram.json`

```json
{
  "query": {
    "match": {
      "city.ngram": "Pa"
    }
  }
}
```

✔ Permet de rechercher "Pa" → trouve "Paris"

---

## 4️⃣ Recherche Fuzzy (tolérance aux fautes)

Fichier : `4_fuzzy.json`

```json
{
  "query": {
    "fuzzy": {
      "city": {
        "value": "Pari",
        "fuzziness": "AUTO"
      }
    }
  }
}
```

✔ Fonctionne même avec faute d’orthographe.

---

## 5️⃣ Série Temporelle (Histogramme horaire)

Fichier : `5_timeseries.json`

```json
{
  "size": 0,
  "aggs": {
    "par_heure": {
      "date_histogram": {
        "field": "timestamp",
        "calendar_interval": "1h"
      },
      "aggs": {
        "temp_moy": { "avg": { "field": "temp" } }
      }
    }
  }
}
```

✔ Permet d’analyser l’évolution horaire de la température.

---

# 🧠 Points techniques avancés

* Template Elasticsearch avec `edge_ngram`
* Mapping personnalisé pour `city.ngram`
* Agrégations (`terms`, `avg`)
* Date histogram
* Fuzzy search
* Architecture microservices Docker

---

# 🚀 Commandes utiles

Exécuter une requête :

```bash
curl -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search" \
-d @elasticsearch_queries/1_match.json
```

---

# 📌 Conclusion

Ce projet met en œuvre :

* Pipeline temps réel
* Traitement Big Data
* Recherche full-text
* Agrégations analytiques
* Auto-complétion via N-gram
* Architecture distribuée
