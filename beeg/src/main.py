import psycopg


async def copy_from_csv_async(path: str, part_number):
    create_sql = f"CREATE TABLE stage_reviews_{part_number} (LIKE reviews);"
    sql = f"""COPY stage_reviews_{part_number} 
    (review_id, user_id, restaurant_id, rating, review_text, created_at) 
    FROM STDIN WITH CSV HEADER"""

    print(f"starting copy for table: {part_number}")
    async with await psycopg.AsyncConnection.connect(
        "dbname=beeg"
    ) as conn:
        async with conn.cursor() as cur:
            
            await cur.execute(create_sql)

            async with cur.copy(sql) as copy:
                with open(path, "r") as f:
                    while chunk := f.read(8192):
                        await copy.write(chunk)
    

def main():
    return

if __name__ == "__main__":
    main()