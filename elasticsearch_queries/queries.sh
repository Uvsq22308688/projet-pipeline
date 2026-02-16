# 1️⃣ Recherche description rain
curl -s -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search?pretty" \
-d '{"query":{"match":{"description":"rain"}}}'

# 2️⃣ Agrégation température moyenne par ville
curl -s -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search?pretty" \
-d '{
  "size": 0,
  "aggs": {
    "par_ville": {
      "terms": { "field": "city", "size": 10 },
      "aggs": {
        "temp_moy": { "avg": { "field": "temp" } }
      }
    }
  }
}'

# 3️⃣ Recherche partielle avec ngram
curl -s -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search?pretty" \
-d '{"query":{"match":{"city.ngram":"Pa"}}}'

# 4️⃣ Recherche fuzzy
curl -s -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search?pretty" \
-d '{"query":{"fuzzy":{"city":{"value":"Pariss","fuzziness":"AUTO"}}}}'

# 5️⃣ Histogramme par heure
curl -s -H "Content-Type: application/json" \
-X GET "http://localhost:9200/api-events-*/_search?pretty" \
-d '{
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
}'
