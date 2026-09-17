"""The JSON API, mounted under /api."""
import logging
from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException, Query, status

from askops import sources
from askops.deps import get_store
from askops.errors import RunbookNotFound
from askops.schemas import AskOut, HitOut, IncidentIn, IncidentOut, RunbookOut
from askops.store import Store

logger = logging.getLogger(__name__)
router = APIRouter()


def _runbook_out(rb) -> RunbookOut:
    return RunbookOut(id=rb.id, title=rb.title, service=rb.service, tags=sorted(rb.tags), steps=list(rb.steps))


def _incident_out(incident) -> IncidentOut:
    return IncidentOut(**asdict(incident))


@router.get("/health")
def health(store: Store = Depends(get_store)) -> dict:
    return {"status": "ok", "runbooks": len(store.runbooks())}


@router.get("/runbooks", response_model=list[RunbookOut])
def list_runbooks(service: str | None = None, store: Store = Depends(get_store)):
    return [_runbook_out(rb) for rb in store.runbooks(service)]


@router.get("/runbooks/{runbook_id}", response_model=RunbookOut)
def get_runbook(runbook_id: str, store: Store = Depends(get_store)):
    try:
        return _runbook_out(store.get_runbook(runbook_id))
    except RunbookNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/incidents", response_model=list[IncidentOut])
def list_incidents(store: Store = Depends(get_store)):
    return [_incident_out(i) for i in store.incidents()]


@router.post("/incidents", response_model=IncidentOut, status_code=status.HTTP_201_CREATED)
def create_incident(body: IncidentIn, store: Store = Depends(get_store)):
    try:
        return _incident_out(store.add_incident(body.title, body.severity, body.service, body.runbook_id))
    except RunbookNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/ask", response_model=AskOut)
async def ask(
    q: str = Query(min_length=3),
    limit: int = Query(5, ge=1),
    store: Store = Depends(get_store),
):
    if not any(len(w) >= 3 for w in q.split()):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="query needs a word of 3+ characters")
    # Await the sources one at a time: easier to read and to step through in a debugger.
    # If a source is down, degrade gracefully instead of failing the whole request.
    try:
        runbook_hits = await sources.runbook_hits(store, q, limit)
        incident_hits = await sources.incident_hits(store, q)
    except Exception:
        logger.warning("ask degraded for q=%r", q)
        runbook_hits, incident_hits = [], []
    return AskOut(
        query=q,
        runbooks=[HitOut(**asdict(h)) for h in runbook_hits],
        incidents=[_incident_out(i) for i in incident_hits],
    )
