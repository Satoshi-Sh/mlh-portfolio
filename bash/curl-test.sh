#!/bin/sh

# Create Post test 
CREATED_POST_ID=$(curl -s --request POST http://localhost:5000/api/timeline_post -d 'name=Satoshi&email=test@email.com&content=Testing my endpints with curl.' | jq -r '.id')
LATEST_POST_ID=$(curl -s http://localhost:5000/api/timeline_post | jq -r '.timeline_posts[].id' | head -n 1)

if [ "$CREATED_POST_ID" -eq "$LATEST_POST_ID" ]; then
    echo "New post $CREATED_POST_ID created correctly!!"
    # Delete test post
    curl -s --request DELETE "http://localhost:5000/api/timeline_post/$CREATED_POST_ID" | jq -r '.message' 
    else
    echo "Something went wrong.."
fi



