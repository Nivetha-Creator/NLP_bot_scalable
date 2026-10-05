from nlp_bot_scalable.config.database import engine
from nlp_bot_scalable.database.models import Base


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()