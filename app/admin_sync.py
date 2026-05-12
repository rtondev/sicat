"""Tarefa periódica (estilo cron) que garante admin para matrículas em ADMIN_MATRICULAS."""

import asyncio
import logging
from contextlib import suppress
from datetime import datetime

from app.database import SessionLocal, matriculas_admin_configuradas, settings
from app.models import TipoUsuario, Usuario

logger = logging.getLogger(__name__)


def promote_admin_matriculas() -> int:
    """Atualiza no BD os utilizadores listados em ADMIN_MATRICULAS para tipo admin."""
    mats = matriculas_admin_configuradas()
    if not mats:
        return 0
    db = SessionLocal()
    try:
        changed = 0
        users = db.query(Usuario).filter(Usuario.matricula.in_(tuple(mats))).all()
        for u in users:
            if u.tipo != TipoUsuario.admin:
                u.tipo = TipoUsuario.admin
                u.data_edicao = datetime.utcnow()
                changed += 1
        if changed:
            db.commit()
            logger.info("admin_sync: %s utilizador(es) promovido(s) a admin", changed)
        return changed
    except Exception:
        db.rollback()
        logger.exception("admin_sync: falha ao promover admins")
        raise
    finally:
        db.close()


async def admin_sync_loop(stop: asyncio.Event) -> None:
    while not stop.is_set():
        interval = max(30, settings.admin_sync_interval_seconds)
        try:
            await asyncio.to_thread(promote_admin_matriculas)
        except Exception:
            pass
        try:
            await asyncio.wait_for(stop.wait(), timeout=interval)
        except asyncio.TimeoutError:
            continue
