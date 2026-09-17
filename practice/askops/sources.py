"""Two slow sources that /ask consults. Complete - nothing to do here.

In production these would be network calls: the runbook wiki and the ticketing system, each
taking a couple of hundred milliseconds. Here `asyncio.sleep` stands in for that I/O, so the
difference between awaiting them one after another and awaiting them together is measurable.
"""
import asyncio

from askops.models import Incident
from askops.search import Hit, search
from askops.store import Store

LATENCY_SECONDS = 0.2


async def runbook_hits(store: Store, query: str, limit: int = 5) -> list[Hit]:
    await asyncio.sleep(LATENCY_SECONDS)      # the wiki round trip
    return search(store, query, limit)


async def incident_hits(store: Store, query: str) -> list[Incident]:
    await asyncio.sleep(LATENCY_SECONDS)      # the ticketing-system round trip
    words = [w for w in query.lower().split() if len(w) >= 3]
    return [i for i in store.incidents() if any(w in i.title.lower() for w in words)]
