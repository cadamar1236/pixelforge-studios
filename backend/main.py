import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random
from uuid import uuid4

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "company")
db_engine = None
SessionLocal = None

class Base(DeclarativeBase):
    pass

if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(bind=db_engine)

class User(Base):
    __tablename__ = f"{COMPANY_SLUG}_users"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    plan = Column(String, default="free")

class Subscription(Base):
    __tablename__ = f"{COMPANY_SLUG}_subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False)
    tool_id = Column(String, nullable=False)
    status = Column(String, default="active")
    price = Column(Float, nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)

class Tool(Base):
    __tablename__ = f"{COMPANY_SLUG}_tools"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    name = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)
    price = Column(Float)
    active_users = Column(Integer, default=0)

class AnalyticsEvent(Base):
    __tablename__ = f"{COMPANY_SLUG}_analytics"
    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String)
    event = Column(String)
    tool_id = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(Text)

mock_users = [
    {"id": "1", "name": "Alice Johnson", "email": "alice@example.com", "created_at": "2024-01-15T10:00:00", "plan": "pro"},
    {"id": "2", "name": "Bob Smith", "email": "bob@example.com", "created_at": "2024-02-20T14:30:00", "plan": "business"},
    {"id": "3", "name": "Charlie Brown", "email": "charlie@example.com", "created_at": "2024-03-10T08:00:00", "plan": "free"},
    {"id": "4", "name": "Diana Prince", "email": "diana@example.com", "created_at": "2024-04-05T16:45:00", "plan": "pro"},
    {"id": "5", "name": "Eve Adams", "email": "eve@example.com", "created_at": "2024-05-12T09:15:00", "plan": "free"},
    {"id": "6", "name": "Frank Castle", "email": "frank@example.com", "created_at": "2024-06-01T11:00:00", "plan": "business"},
    {"id": "7", "name": "Grace Hopper", "email": "grace@example.com", "created_at": "2024-06-15T13:20:00", "plan": "pro"},
    {"id": "8", "name": "Henry Ford", "email": "henry@example.com", "created_at": "2024-07-01T07:30:00", "plan": "free"}
]

mock_tools = [
    {"id": "t1", "name": "Invoicely", "description": "Smart invoicing for freelancers", "category": "Finance", "price": 19.0, "active_users": 1240},
    {"id": "t2", "name": "LeadMagnet", "description": "Capture and nurture leads", "category": "Marketing", "price": 29.0, "active_users": 890},
    {"id": "t3", "name": "TimeTracker Pro", "description": "Track hours and productivity", "category": "Productivity", "price": 14.0, "active_users": 2100},
    {"id": "t4", "name": "SocialScheduler", "description": "Schedule social media posts", "category": "Marketing", "price": 9.0, "active_users": 3400},
    {"id": "t5", "name": "ContractLens", "description": "Review contracts with AI", "category": "Legal", "price": 24.0, "active_users": 560},
    {"id": "t6", "name": "PulseAnalytics", "description": "Real-time business metrics dashboard", "category": "Analytics", "price": 19.0, "active_users": 1470},
    {"id": "t7", "name": "MailForge", "description": "Email marketing automation", "category": "Marketing", "price": 14.0, "active_users": 920}
]

mock_subscriptions = [
    {"id": "s1", "user_id": "1", "tool_id": "t1", "status": "active", "price": 19.0, "start_date": "2024-01-20T10:00:00", "end_date": "2025-01-20T10:00:00"},
    {"id": "s2", "user_id": "1", "tool_id": "t3", "status": "active", "price": 14.0, "start_date": "2024-02-01T14:00:00", "end_date": "2025-02-01T14:00:00"},
    {"id": "s3", "user_id": "2", "tool_id": "t2", "status": "active", "price": 29.0, "start_date": "2024-03-15T09:00:00", "end_date": "2025-03-15T09:00:00"},
    {"id": "s4", "user_id": "2", "tool_id": "t4", "status": "active", "price": 9.0, "start_date": "2024-04-01T11:30:00", "end_date": "2025-04-01T11:30:00"},
    {"id": "s5", "user_id": "3", "tool_id": "t6", "status": "active", "price": 19.0, "start_date": "2024-05-10T16:00:00", "end_date": "2025-05-10T16:00:00"},
    {"id": "s6", "user_id": "4", "tool_id": "t5", "status": "active", "price": 24.0, "start_date": "2024-06-05T08:45:00", "end_date": "2025-06-05T08:45:00"},
    {"id": "s7", "user_id": "5", "tool_id": "t7", "status": "active", "price": 14.0, "start_date": "2024-07-01T12:00:00", "end_date": "2025-07-01T12:00:00"},
    {"id": "s8", "user_id": "6", "tool_id": "t1", "status": "active", "price": 19.0, "start_date": "2024-07-15T10:30:00", "end_date": "2025-07-15T10:30:00"},
    {"id": "s9", "user_id": "7", "tool_id": "t3", "status": "active", "price": 14.0, "start_date": "2024-08-01T15:00:00", "end_date": "2025-08-01T15:00:00"},
    {"id": "s10", "user_id": "1", "tool_id": "t4", "status": "active", "price": 9.0, "start_date": "2024-08-10T09:20:00", "end_date": "2025-08-10T09:20:00"}
]

mock_analytics = [
    {"id": "a1", "user_id": "1", "event": "login", "tool_id": "t1", "timestamp": "2024-08-01T08:00:00", "metadata": "{\"browser\": \"Chrome\"}"},
    {"id": "a2", "user_id": "2", "event": "purchase", "tool_id": "t2", "timestamp": "2024-08-01T09:30:00", "metadata": "{\"amount\": 29.0}"},
    {"id": "a3", "user_id": "3", "event": "feature_use", "tool_id": "t6", "timestamp": "2024-08-01T10:15:00", "metadata": "{\"feature\": \"report_generation\"}"},
    {"id": "a4", "user_id": "4", "event": "signup", "tool_id": "t5", "timestamp": "2024-08-01T11:00:00", "metadata": "{\"source\": \"referral\"}"},
    {"id": "a5", "user_id": "5", "event": "cancellation", "tool_id": "t7", "timestamp": "2024-08-01T12:45:00", "metadata": "{\"reason\": \"too_expensive\"}"},
    {"id": "a6", "user_id": "6", "event": "login", "tool_id": "t1", "timestamp": "2024-08-02T07:30:00", "metadata": "{\"browser\": \"Firefox\"}"},
    {"id": "a7", "user_id": "7", "event": "feature_use", "tool_id": "t3", "timestamp": "2024-08-02T08:45:00", "metadata": "{\"feature\": \"time_tracking\"}"},
    {"id": "a8", "user_id": "1", "event": "purchase", "tool_id": "t4", "timestamp": "2024-08-02T09:00:00", "metadata": "{\"amount\": 9.0}"}
]

app = FastAPI(title="SoloSuite", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    name: str
    email: str
    plan: str = "free"

class SubscriptionCreate(BaseModel):
    user_id: str
    tool_id: str
    price: float

class AnalyticsEventModel(BaseModel):
    user_id: str
    event: str
    tool_id: str
    metadata: str = "{}"

@app.on_event("startup")
async def startup():
    if db_engine:
        Base.metadata.create_all(db_engine)

@app.get("/health")
async def health():
    return {"status": "ok", "app": "SoloSuite", "version": "1.0.0"}

@app.get("/api/info")
async def info():
    return {
        "name": "PixelForge Studios",
        "app": "SoloSuite",
        "tagline": "Empowering solopreneurs with powerful micro-tools",
        "founded": "2023",
        "team_size": 8,
        "headquarters": "Austin, TX",
        "mission": "A digital product studio that builds and sells SaaS micro-tools for solopreneurs",
        "pricing_range": "$9-$29/month",
        "total_users": len(mock_users),
        "total_tools": len(mock_tools)
    }

@app.get("/api/metrics")
async def metrics():
    total_revenue = sum(s["price"] for s in mock_subscriptions if s["status"] == "active")
    active_subs = len([s for s in mock_subscriptions if s["status"] == "active"])
    churned = len([s for s in mock_subscriptions if s["status"] != "active"])
    return {
        "mrr": round(total_revenue, 2),
        "active_subscriptions": active_subs,
        "total_users": len(mock_users),
        "churn_rate": round(churned / max(len(mock_subscriptions), 1) * 100, 2),
        "average_revenue_per_user": round(total_revenue / max(len(mock_users), 1), 2),
        "tool_usage_count": sum(s["active_users"] for s in mock_tools),
        "last_updated": datetime.utcnow().isoformat()
    }

@app.get("/api/users")
async def get_users():
    return mock_users

@app.post("/api/users")
async def create_user(user: UserCreate):
    new_user = {
        "id": str(uuid4()),
        "name": user.name,
        "email": user.email,
        "created_at": datetime.utcnow().isoformat(),
        "plan": user.plan
    }
    mock_users.append(new_user)
    return new_user

@app.get("/api/tools")
async def get_tools():
    return mock_tools

@app.get("/api/subscriptions")
async def get_subscriptions():
    return mock_subscriptions

@app.post("/api/subscriptions")
async def create_subscription(sub: SubscriptionCreate):
    new_sub = {
        "id": str(uuid4()),
        "user_id": sub.user_id,
        "tool_id": sub.tool_id,
        "status": "active",
        "price": sub.price,
        "start_date": datetime.utcnow().isoformat(),
        "end_date": (datetime.utcnow() + timedelta(days=365)).isoformat()
    }
    mock_subscriptions.append(new_sub)
    return new_sub

@app.get("/api/analytics")
async def get_analytics():
    return mock_analytics

@app.post("/api/analytics")
async def create_analytics(event: AnalyticsEventModel):
    new_event = {
        "id": str(uuid4()),
        "user_id": event.user_id,
        "event": event.event,
        "tool_id": event.tool_id,
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": event.metadata
    }
    mock_analytics.append(new_event)
    return new_event

@app.get("/api/stats")
async def stats():
    plan_distribution = {}
    for u in mock_users:
        plan = u["plan"]
        plan_distribution[plan] = plan_distribution.get(plan, 0) + 1
    
    tool_popularity = sorted(mock_tools, key=lambda x: x["active_users"], reverse=True)
    
    return {
        "plan_distribution": plan_distribution,
        "total_users": len(mock_users),
        "total_subscriptions": len(mock_subscriptions),
        "active_subscriptions": len([s for s in mock_subscriptions if s["status"] == "active"]),
        "popular_tools": [{"name": t["name"], "active_users": t["active_users"]} for t in tool_popularity[:3]],
        "average_tool_price": round(sum(t["price"] for t in mock_tools) / len(mock_tools), 2)
    }

@app.get("/api/recent-activity")
async def recent_activity():
    recent = sorted(mock_analytics, key=lambda x: x["timestamp"], reverse=True)[:8]
    enriched = []
    for e in recent:
        user = next((u for u in mock_users if u["id"] == e["user_id"]), None)
        tool = next((t for t in mock_tools if t["id"] == e["tool_id"]), None)
        enriched.append({
            "event": e["event"],
            "user_name": user["name"] if user else "Unknown",
            "tool_name": tool["name"] if tool else "Unknown",
            "timestamp": e["timestamp"],
            "metadata": e["metadata"]
        })
    return enriched

@app.get("/api/chart-data")
async def chart_data():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug"]
    revenue_chart = [random.uniform(5000, 15000) for _ in range(8)]
    user_growth = [100, 150, 200, 280, 350, 420, 500, 580]
    churn_chart = [random.uniform(1, 8) for _ in range(8)]
    return {
        "revenue_by_month": [{"month": m, "revenue": round(r, 2)} for m, r in zip(months, revenue_chart)],
        "user_growth": [{"month": m, "users": u} for m, u in zip(months, user_growth)],
        "monthly_churn_rate": [{"month": m, "churn": round(c, 2)} for m, c in zip(months, churn_chart)]
    }

@app.get("/api/dashboard")
async def dashboard():
    return {
        "total_users": len(mock_users),
        "active_subscriptions": len([s for s in mock_subscriptions if s["status"] == "active"]),
        "monthly_revenue": round(sum(s["price"] for s in mock_subscriptions if s["status"] == "active"), 2),
        "popular_tool": max(mock_tools, key=lambda x: x["active_users"])["name"],
        "recent_signups": sorted(mock_users, key=lambda x: x["created_at"], reverse=True)[:5],
        "tools_summary": [
            {"name": t["name"], "category": t["category"], "price": t["price"], "active_users": t["active_users"]}
            for t in mock_tools[:5]
        ]
    }

PORT = int(os.environ.get("COMPANY_PORT", 8000))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)