import pytest
from datetime import date, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from app.database import Base
from app.models.user import User
from app.models.task import Task, Priority, TaskStatus

# Use a separate test database on Postgres (same Docker instance)
TEST_DB_URL = "postgresql://planner:planner@localhost:5432/planner_test"
ADMIN_DB_URL = "postgresql://planner:planner@localhost:5432/planner"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _pg_is_available() -> bool:
    """Check if Postgres is reachable."""
    try:
        engine = create_engine(ADMIN_DB_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        engine.dispose()
        return True
    except Exception:
        return False


requires_postgres = pytest.mark.skipif(
    not _pg_is_available(),
    reason="PostgreSQL not available (run `docker compose up -d` first)",
)


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """Create the test database once per session."""
    if not _pg_is_available():
        yield
        return
    admin_engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS planner_test"))
        conn.execute(text("CREATE DATABASE planner_test"))
    admin_engine.dispose()
    yield
    # Cleanup after all tests
    admin_engine = create_engine(ADMIN_DB_URL, isolation_level="AUTOCOMMIT")
    with admin_engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS planner_test"))
    admin_engine.dispose()


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test, drop after."""
    if not _pg_is_available():
        pytest.skip("PostgreSQL not available")
    engine = create_engine(TEST_DB_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def db(setup_db):
    Session = sessionmaker(bind=setup_db)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def user(db):
    u = User(
        name="Test User",
        email="test@example.com",
        hashed_password=pwd_context.hash("test123"),
        timezone="Asia/Kolkata",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u
