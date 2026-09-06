import os
import pytest
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from app.core.config import settings


def test_alembic_config_loading():
    """Verify Alembic configuration file exists and script directory loads."""
    ini_path = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
    assert os.path.exists(ini_path), f"alembic.ini not found at {ini_path}"

    alembic_cfg = Config(ini_path)
    script_dir = ScriptDirectory.from_config(alembic_cfg)
    assert script_dir is not None

    revisions = list(script_dir.walk_revisions())
    assert len(revisions) > 0, "No Alembic migration revisions found"
    assert revisions[-1].revision == "001_initial_schema"


@pytest.mark.asyncio
async def test_alembic_upgrade_downgrade_cycle_if_postgres_available():
    """
    If PostgreSQL is reachable, test full Alembic upgrade -> downgrade -> upgrade cycle.
    Otherwise, gracefully report DB unreachable for unit test scope.
    """
    from alembic import command
    from app.database.connection import check_db_health

    is_db_ready = await check_db_health()
    if not is_db_ready:
        pytest.skip("PostgreSQL service is not reachable, skipping live migration test")

    ini_path = os.path.join(os.path.dirname(__file__), "..", "alembic.ini")
    alembic_cfg = Config(ini_path)

    # 1. Upgrade head
    command.upgrade(alembic_cfg, "head")

    # 2. Downgrade base
    command.downgrade(alembic_cfg, "base")

    # 3. Upgrade head again
    command.upgrade(alembic_cfg, "head")
