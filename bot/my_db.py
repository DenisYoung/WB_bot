from sqlalchemy import create_engine, MetaData, Table, delete, desc

# Создание подключения к базе данных PostgreSQL
engine = create_engine('postgresql://postgres:2131@db:5432/postgres')
metadata = MetaData()
users_subscriptions = Table('users_subscriptions', metadata,  autoload_with=engine)

def add_user_sub(user_id, article):
    
    with engine.connect() as connection:
        exist = connection.execute(users_subscriptions.select().where(users_subscriptions.c.user_id == user_id, users_subscriptions.c.article == article).order_by(desc(users_subscriptions.c.id)).with_only_columns(users_subscriptions.c.sub_status)).fetchone()
        print(exist)
        if exist is not None and exist[0]:
            return 0
        del_user_subs(user_id)
        connection.execute(users_subscriptions.insert().values(user_id=user_id, article=article, sub_status=1))
        connection.commit()
        return 1

def del_user_subs(user_id):
    with engine.connect() as connection:
        connection.execute(users_subscriptions.update().where(users_subscriptions.c.user_id == user_id, users_subscriptions.c.sub_status == True).values(sub_status=0))
        connection.commit()

def get_5last(user_id):
    with engine.connect() as connection:
        result = connection.execute(users_subscriptions.select().where(users_subscriptions.c.user_id == user_id).order_by(desc(users_subscriptions.c.id)).limit(5).with_only_columns(users_subscriptions.c.article, users_subscriptions.c.created_at)).fetchall()
        return result

def get_users_with_subs():
    with engine.connect() as connection:
        result = connection.execute(users_subscriptions.select().where(users_subscriptions.c.sub_status == True).with_only_columns(users_subscriptions.c.user_id, users_subscriptions.c.article)).fetchall()
        return result
    
if __name__ == '__main__':
    print(add_user_sub(1,32233))
    #print(get_5last(1))
    del_user_subs(1)
    #print(get_5last(1))
    #add_user_sub(3,32233)
    #print(get_users_with_subs())
    print(add_user_sub(1,32233))