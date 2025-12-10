from core.db import Base, engine

def init():
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

if __name__ == "__main__":
    init()
