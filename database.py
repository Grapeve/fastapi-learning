from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from sqlalchemy.ext.declarative import declarative_base

# 数据库连接配置
SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://root:xxxxxx@127.0.0.1:3306/fastapi-study?charset=utf8mb4"
    #                     密码
)

# 创建数据库引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI)
# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
