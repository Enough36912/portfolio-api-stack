import os
import psycopg
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

app = FastAPI(title="Isaac Sterling | Portfolio API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

def get_conn():
    # autocommit for simple demo
    return psycopg.connect(DATABASE_URL, autocommit=True)

@app.get("/health")
def health():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
        return {"ok": True, "db": "up"}
    except Exception as e:
        return {"ok": False, "db": "down", "error": str(e)}

@app.get("/visits")
def get_visits():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT count FROM visits WHERE pk = 'resume';")
            row = cur.fetchone()
            return {"count": int(row[0]) if row else 0}

@app.post("/visits/increment")
def increment_visits():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO visits(pk, count)
                VALUES ('resume', 1)
                ON CONFLICT (pk)
                DO UPDATE SET count = visits.count + 1
                RETURNING count;
            """)
            new_count = cur.fetchone()[0]
            return {"count": int(new_count)}

@app.get("/")
def root():
    return {
        "service": "portfolio-api-stack",
        "endpoints": ["/health", "/visits", "/visits/increment (POST)"],
        "hint": "Run: curl http://localhost:8080/health"
    }
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

REQUESTS = Counter("api_requests_total", "Total API requests", ["path", "method"])

@app.middleware("http")
async def metrics_mw(request, call_next):
    resp = await call_next(request)
    REQUESTS.labels(path=request.url.path, method=request.method).inc()
    return resp

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
