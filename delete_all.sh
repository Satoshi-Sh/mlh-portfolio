# can be done in oneline with xargs
# curl -s http://localhost:5000/api/timeline_post | jq -r '.timeline_posts[].id'| xargs -L 1 curl -s --request DELETE "http://localhost:5000/api/timeline_post/{}"


ids=$(curl -s http://localhost:5000/api/timeline_post | jq -r '.timeline_posts[].id' )

for id in $ids
do 
  curl -s --request DELETE "http://localhost:5000/api/timeline_post/$id"
done