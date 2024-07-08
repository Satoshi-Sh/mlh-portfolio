ids=$(curl -s http://localhost:5000/api/timeline_post | jq -r '.timeline_posts[].id' )

for id in $ids
do 
  curl -s --request DELETE "http://localhost:5000/api/timeline_post/$id"
done