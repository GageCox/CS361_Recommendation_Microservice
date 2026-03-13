import mysql.connector
import zmq
import json

def get_connection():
    conn = mysql.connector.connect(
        host='', # add host
        user='', # add username
        password='', # add password
        database='' # add database name
    )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def recommendation(req):
    rec_table = req["recommendation_table"]
    user_table = req["user_table"]
    conn, cursor = get_connection()

    query = f"""
        SELECT r.title, r.genre
        FROM {rec_table} r
        LEFT JOIN {user_table} u
        ON r.title = u.title
        WHERE u.title IS NULL
        ORDER BY RAND()
        LIMIT 3
    """

    cursor.execute(query)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def genre_recommendation(req):
    rec_table = req["recommendation_table"]
    user_table = req["user_table"]
    genre = req["genre"]
    conn, cursor = get_connection()

    query = f"""
        SELECT r.title, r.genre
        FROM {rec_table} r
        LEFT JOIN {user_table} u
        ON r.title = u.title
        WHERE u.title IS NULL
        AND r.genre = %s
        ORDER BY RAND()
        LIMIT 3
    """

    cursor.execute(query, (genre,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def route_handler(req):
    action = req.get("action")

    if action == "recommendation":
        return recommendation(req)
    
    elif action == "genre_recommendation":
        return genre_recommendation(req)
    
    else:
        raise ValueError("Invalid Request")

def runServer():
    global context, socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5556")

    print("Service running on port 5556...")

    while True:
        message = socket.recv()

        try:
            request = json.loads(message.decode("utf-8"))
            result = route_handler(request)
            response = {
                "status": "success",
                "data": result
            }

        except Exception as e:
            response = {
                "status": "error",
                "message": str(e)
            }

        socket.send(json.dumps(response).encode("utf-8"))

if __name__ == "__main__":
    runServer()