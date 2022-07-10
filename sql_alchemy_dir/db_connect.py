from sqlalchemy import create_engine

# Linux
# def db_con():
#     engine = create_engine(
#         "sqlite:////home/golu/Desktop/Github/coinPrice/Coin_price.db", echo=True
#     )
#     print("DB CREATED")
#     return engine

# Windows
def db_con():
    engine = create_engine(
        "sqlite:///C:\\Github\\coinPrice\\Coin_price.db", echo=True
    )
    print("DB CREATED")
    return engine