"""PATHFINDER FastAPI application.  Run:  uvicorn main:app --reload"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import RouteRequest, RouteResponse
from services.graph_service import CampusGraph
from services.route_service import find_route

graph: CampusGraph | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global graph
    graph = CampusGraph()
    yield


app = FastAPI(title="PATHFINDER API", version="1.0.0",
              description="Campus navigation powered by a from-scratch A* search engine.", lifespan=lifespan)

# Comma-separated list of allowed frontend origins, e.g. "https://my-app.vercel.app"
_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173")
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in _origins.split(",") if o.strip()],
                   allow_methods=["*"], allow_headers=["*"])


def _graph() -> CampusGraph:
    return graph if graph is not None else CampusGraph()


@app.get("/")
def root():
    return {"name": "PATHFINDER API", "docs": "/docs", "health": "/api/health"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/map")
def get_map():
    return _graph().raw


@app.get("/api/locations")
def get_locations():
    return _graph().raw["locations"]


@app.post("/api/find-route", response_model=RouteResponse)
def post_find_route(req: RouteRequest):
    try:
        return find_route(_graph(), req.source, req.destination)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=f"Unknown location: {exc.args[0]}")


@app.post("/api/reset")
def post_reset():
    # The API is stateless (every search is independent); this endpoint exists so clients
    # can signal a reset and get a consistent acknowledgement.
    return {"status": "ok", "message": "Search state cleared."}
