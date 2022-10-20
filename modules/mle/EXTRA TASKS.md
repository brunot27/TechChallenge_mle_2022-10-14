## DE's tasks

create a new database user, called `analyst`, with READ and WRITE access to the public schema of the database. This user should be created when starting the database for the first time.

added to `/de/db_admin/setup_users.sql`

```
CREATE USER analyst PASSWORD 'analyst';
GRANT CREATE, USAGE ON SCHEMA public TO analyst;
```

## DS's Tasks

Add a new function to the `data_science` package to fetch the data from the sales table.

added to `ds/ds_package/src/data_science/fetch_data.py`

```
def get_sales():
    """Fetches the sales from the database
    """
    sales = pd.read_sql(
        "select * from sales",
        get_conn_string()
    )
    return sales
```