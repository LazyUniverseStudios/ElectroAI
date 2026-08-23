import db_connection

async def check_parent(user_id):
    connection = db_connection.get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT ParentID FROM Family WHERE UserID = %s", (user_id,))
    result = cursor.fetchone()

    if result:
        parent_id = result[0]
        return [True, parent_id]
    else:
        return [False, None]