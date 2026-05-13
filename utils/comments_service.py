from database.database import get_connection


def structure_comments(comments: list) -> list:
    for comment in comments:
        comment["replies"] = []

    comment_map = {}
    for comment in comments:
        comment_map[comment["id"]] = comment

    root_comments = []

    for comment in comments:
        parent_id = comment["parent_id"]

        if parent_id in comment_map:
            comment_map[parent_id]["replies"].append(comment)
        else:
            root_comments.append(comment)

    return root_comments

def get_comments_for_post(post_id: int) -> list:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        WITH RECURSIVE comment_tree AS (
            SELECT 
                message.id,
                message.creator_id,
                message.creation_date,
                message.content,
                message.image,
                response.parent_id
            FROM response
            JOIN message ON message.id = response.message_id
            WHERE response.parent_id = ?

            UNION ALL

            SELECT 
                message.id,
                message.creator_id,
                message.creation_date,
                message.content,
                message.image,
                response.parent_id
            FROM response
            JOIN message ON message.id = response.message_id
            JOIN comment_tree ON response.parent_id = comment_tree.id
        )
        SELECT * FROM comment_tree
        ORDER BY creation_date
    """, (post_id,))

    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return structure_comments(comments)