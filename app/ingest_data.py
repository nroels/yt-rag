import os, psycopg2

con = psycopg2.connect(
    dbname=os.environ["POSTGRES_DB"],
    user=os.environ["POSTGRES_USER"],
    password=os.environ["POSTGRES_PASSWORD"],
    host=os.environ.get("POSTGRES_HOST", "localhost"),
    port=os.environ.get("POSTGRES_PORT", "5432"),
)

curs_obj = con.cursor()

curs_obj.execute("INSERT INTO videos(emp_name, emp_age) VALUES('Joseph', 26), ('Joe', 29);")
print("Data Inserted")

con.commit()

curs_obj.execute("SELECT * FROM emp_data")
result = curs_obj.fetchall()
print("Table's Data:", "\n", result)