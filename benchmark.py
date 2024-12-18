import os
import time
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Database setup
DATABASE_URL = os.getenv(
    "SQLALCHEMY_DATABASE_URI", "postgresql://postgres:password@db/flaskapi_db")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Models


class Store(Base):
    __tablename__ = 'stores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    items = relationship("Item", back_populates="store",
                         cascade="all, delete-orphan")


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    price = Column(Float, nullable=False)
    store_id = Column(Integer, ForeignKey('stores.id'), nullable=False)
    store = relationship("Store", back_populates="items")

# Context manager for sessions


@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Error occurred: {e}")
        raise
    finally:
        session.close()

# Utility function to measure time


def measure_time(func, *args, **kwargs):
    start_time = time.time()
    func(*args, **kwargs)
    return time.time() - start_time

# Seed the database with data in smaller chunks


def seed_data_in_chunks(session, total_records, chunk_size=1000):
    session.query(Item).delete()
    session.query(Store).delete()

    store = Store(name="Test Store")
    session.add(store)
    session.commit()

    for i in range(0, total_records, chunk_size):
        chunk = [
            Item(name=f"Item {j}", price=j * 0.1, store_id=store.id)
            for j in range(i, min(i + chunk_size, total_records))
        ]
        session.bulk_save_objects(chunk)
        session.commit()
        logger.info(f"Inserted {len(chunk)} records (total: {i + len(chunk)})")

# Benchmark SELECT query


def select_items():
    with get_session() as session:
        session.query(Item).all()
        logger.info("SELECT query executed.")

# Benchmark INSERT query


def insert_items_in_chunks(session, total_records, chunk_size=1000):
    store_id = session.query(Store).first().id
    for i in range(0, total_records, chunk_size):
        chunk = [
            Item(name=f"New Item {j}", price=j * 0.1, store_id=store_id)
            for j in range(i, min(i + chunk_size, total_records))
        ]
        session.bulk_save_objects(chunk)
        session.commit()
        logger.info(f"Inserted {len(chunk)} records (total: {i + len(chunk)})")

# Benchmark UPDATE query


def update_items_in_chunks(session, total_records, chunk_size=1000):
    for offset in range(0, total_records, chunk_size):
        items = session.query(Item).limit(chunk_size).offset(offset).all()
        for item in items:
            item.price += 1.0
        session.commit()
        logger.info(
            f"Updated {len(items)} records starting at offset {offset}")

# Benchmark DELETE query


def delete_items_in_chunks(session, total_records, chunk_size=1000):
    for offset in range(0, total_records, chunk_size):
        items = session.query(Item).limit(chunk_size).offset(offset).all()
        for item in items:
            session.delete(item)
        session.commit()
        logger.info(
            f"Deleted {len(items)} records starting at offset {offset}")

# Save results to a file


def save_results_to_file(results, filename="benchmark_results.txt"):
    with open(filename, "w") as file:
        file.write(
            "| Batch Size | SELECT Time | INSERT Time | UPDATE Time | DELETE Time |\n")
        for batch_size, times in results:
            file.write(
                f"| {batch_size:<10} | {times['SELECT']:.3f}s     | {
                    times['INSERT']:.3f}s     | "
                f"{times['UPDATE']:.3f}s     | {times['DELETE']:.3f}s     |\n"
            )
    logger.info(f"Benchmark results saved to {filename}")

# Main benchmark function


def run_benchmark():
    batch_sizes = [1000, 10000, 100000]
    results = []

    for batch_size in batch_sizes:
        logger.info(f"Running benchmark for {batch_size} records...")
        with get_session() as session:
            seed_data_in_chunks(session, total_records=batch_size)

            times = {
                "SELECT": measure_time(select_items),
                "INSERT": measure_time(insert_items_in_chunks, session, batch_size),
                "UPDATE": measure_time(update_items_in_chunks, session, batch_size),
                "DELETE": measure_time(delete_items_in_chunks, session, batch_size)
            }
            results.append((batch_size, times))

    # Display results
    logger.info("Benchmark Results:")
    logger.info(
        "| Batch Size | SELECT Time | INSERT Time | UPDATE Time | DELETE Time |")
    for batch_size, times in results:
        logger.info(
            f"| {batch_size:<10} | {times['SELECT']:.3f}s     | {
                times['INSERT']:.3f}s     | "
            f"{times['UPDATE']:.3f}s     | {times['DELETE']:.3f}s     |"
        )

    # Save results to a file
    save_results_to_file(results)


if __name__ == "__main__":
    # Reset the database schema
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Database schema reset.")

    # Run the benchmark
    try:
        run_benchmark()
        logger.info("Benchmark script completed successfully.")
    except Exception as e:
        logger.error(f"Benchmark failed: {e}")
