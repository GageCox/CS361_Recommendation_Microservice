# CS361_Recommendation_Microservice
Recommendation Microservice for CS361 Project. This service compares two tables in a database, one with user stored movies and another already populated with movies.
The service uses SQL to compare the titles of movies in both tables and returns movies that are not in the user table, optionally filtered by genre.

This micorservice uses ZeroMQ as it's communication pipeline.

# Request
1. Create a REQ socket
2. Connect to a port
3. Send a JSON request
4. Wait for a JSON response

Sample requests to service:
```
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5556")

// recommendations
request = {
    "action": "recommendation",
    "recommendation_table": "moviereccs",
    "user_table": "movies"
}
socket.send(json.dumps(request).encode("utf-8))

// genre_recommendation
request = {
    "action": "genre_recommendation",
    "recommendation_table": "moviereccs",
    "user_table": "movies",
    "genre": "Drama"
}
socket.send(json.dumps(request).encode("utf-8))
```

**Action:**\
recommendation: Returns 3 random movies from the movie recommendations table\
genre_recommendation: Returns 3 random movies from the movie recommendations table that match the genre specified in the request\
**recommendation_table:** The table populated with movies to compare the users table against\
**user_table:** The table with user data\
**genre:** The genre of movie that you want recommendations for

# Recieve
1. Store response from socket
2. Decode JSON response

Sample code for recieving:
```
response_bytes = socket.recv()
response = json.loads(response_bytes.decode("utf-8"))
```