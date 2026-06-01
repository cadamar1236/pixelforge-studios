import os
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import random

DATABASE_URL = os.environ.get("DATABASE_URL", "")
COMPANY_SLUG = os.environ.get("COMPANY_SLUG", "pixelforge")
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
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    name = Column(String)
    joined_date = Column(DateTime, default=datetime.utcnow)
    plan = Column(String, default="free")

class Subscription(Base):
    __tablename__ = f"{COMPANY_SLUG}_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    tool_id = Column(Integer)
    plan_name = Column(String)
    price = Column(Float)
    start_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")

class Tool(Base):
    __tablename__ = f"{COMPANY_SLUG}_tools"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    monthly_price = Column(Float)
    active_users = Column(Integer, default=0)

class UsageLog(Base):
    __tablename__ = f"{COMPANY_SLUG}_usage_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    tool_id = Column(Integer)
    action = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Payment(Base):
    __tablename__ = f"{COMPANY_SLUG}_payments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    subscription_id = Column(Integer)
    amount = Column(Float)
    currency = Column(String, default="USD")
    status = Column(String, default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

if DATABASE_URL and db_engine:
    Base.metadata.create_all(db_engine)

app = FastAPI(title="MicroToolKit", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MOCK_USERS = [
    {"id": 1, "email": "sarah@buildr.com", "name": "Sarah Chen", "joined_date": "2024-01-15T10:00:00", "plan": "pro"},
    {"id": 2, "email": "marcus@dev.io", "name": "Marcus Johnson", "joined_date": "2024-02-20T14:30:00", "plan": "growth"},
    {"id": 3, "email": "elena@startup.xyz", "name": "Elena Rodriguez", "joined_date": "2024-03-10T08:00:00", "plan": "free"},
    {"id": 4, "email": "james@solocorp.com", "name": "James Wilson", "joined_date": "2024-04-05T16:45:00", "plan": "pro"},
    {"id": 5, "email": "anna@sidehustle.io", "name": "Anna Kim", "joined_date": "2024-05-12T11:20:00", "plan": "growth"},
    {"id": 6, "email": "david@microkit.com", "name": "David Park", "joined_date": "2024-06-01T09:15:00", "plan": "free"},
    {"id": 7, "email": "lisa@indiehack.me", "name": "Lisa Thompson", "joined_date": "2024-06-20T13:40:00", "plan": "pro"},
]

MOCK_TOOLS = [
    {"id": 1, "name": "InvoiceBot", "description": "AI-powered invoice generation and tracking", "category": "finance", "monthly_price": 19.0, "active_users": 234},
    {"id": 2, "name": "ContentScribe", "description": "Blog post generator with SEO optimization", "category": "content", "monthly_price": 14.0, "active_users": 567},
    {"id": 3, "name": "LeadScraper", "description": "Automated lead collection from LinkedIn", "category": "sales", "monthly_price": 29.0, "active_users": 345},
    {"id": 4, "name": "ScheduleGenius", "description": "Smart calendar management and meeting scheduler", "category": "productivity", "monthly_price": 9.0, "active_users": 891},
    {"id": 5, "name": "AnalytixMini", "description": "Lightweight website analytics dashboard", "category": "analytics", "monthly_price": 12.0, "active_users": 678},
    {"id": 6, "name": "SocialPilot", "description": "Social media post scheduler and analyzer", "category": "marketing", "monthly_price": 24.0, "active_users": 423},
]

MOCK_SUBSCRIPTIONS = [
    {"id": 1, "user_id": 1, "tool_id": 1, "plan_name": "pro", "price": 19.0, "start_date": "2024-01-15T10:00:00", "status": "active"},
    {"id": 2, "user_id": 2, "tool_id": 3, "plan_name": "growth", "price": 29.0, "start_date": "2024-02-20T14:30:00", "status": "active"},
    {"id": 3, "user_id": 1, "tool_id": 4, "plan_name": "pro", "price": 9.0, "start_date": "2024-03-01T08:00:00", "status": "active"},
    {"id": 4, "user_id": 3, "tool_id": 2, "plan_name": "free", "price": 0.0, "start_date": "2024-03-10T08:00:00", "status": "trial"},
    {"id": 5, "user_id": 4, "tool_id": 5, "plan_name": "pro", "price": 12.0, "start_date": "2024-04-05T16:45:00", "status": "active"},
    {"id": 6, "user_id": 5, "tool_id": 6, "plan_name": "growth", "price": 24.0, "start_date": "2024-05-12T11:20:00", "status": "active"},
    {"id": 7, "user_id": 2, "tool_id": 2, "plan_name": "growth", "price": 14.0, "start_date": "2024-06-01T09:00:00", "status": "active"},
    {"id": 8, "user_id": 7, "tool_id": 1, "plan_name": "pro", "price": 19.0, "start_date": "2024-06-20T13:40:00", "status": "active"},
]

MOCK_USAGE_LOGS = [
    {"id": 1, "user_id": 1, "tool_id": 1, "action": "invoice_generated", "timestamp": "2024-07-01T10:30:00"},
    {"id": 2, "user_id": 2, "tool_id": 3, "action": "lead_exported", "timestamp": "2024-07-01T11:15:00"},
    {"id": 3, "user_id": 4, "tool_id": 5, "action": "report_viewed", "timestamp": "2024-07-01T14:00:00"},
    {"id": 4, "user_id": 5, "tool_id": 6, "action": "post_scheduled", "timestamp": "2024-07-02T09:45:00"},
    {"id": 5, "user_id": 1, "tool_id": 4, "action": "meeting_created", "timestamp": "2024-07-02T15:20:00"},
    {"id": 6, "user_id": 3, "tool_id": 2, "action": "content_generated", "timestamp": "2024-07-03T08:30:00"},
    {"id": 7, "user_id": 7, "tool_id": 1, "action": "invoice_generated", "timestamp": "2024-07-03T12:00:00"},
    {"id": 8, "user_id": 2, "tool_id": 2, "action": "content_published", "timestamp": "2024-07-03T16:45:00"},
]

MOCK_PAYMENTS = [
    {"id": 1, "user_id": 1, "subscription_id": 1, "amount": 19.0, "currency": "USD", "status": "completed", "created_at": "2024-01-15T10:05:00"},
    {"id": 2, "user_id": 2, "subscription_id": 2, "amount": 29.0, "currency": "USD", "status": "completed", "created_at": "2024-02-20T14:35:00"},
    {"id": 3, "user_id": 1, "subscription_id": 3, "amount": 9.0, "currency": "USD", "status": "completed", "created_at": "2024-03-01T08:05:00"},
    {"id": 4, "user_id": 4, "subscription_id": 5, "amount": 12.0, "currency": "USD", "status": "completed", "created_at": "2024-04-05T16:50:00"},
    {"id": 5, "user_id": 5, "subscription_id": 6, "amount": 24.0, "currency": "USD", "status": "completed", "created_at": "2024-05-12T11:25:00"},
    {"id": 6, "user_id": 2, "subscription_id": 7, "amount": 14.0, "currency": "USD", "status": "completed", "created_at": "2024-06-01T09:05:00"},
    {"id": 7, "user_id": 7, "subscription_id": 8, "amount": 19.0, "currency": "USD", "status": "completed", "created_at": "2024-06-20T13:45:00"},
    {"id": 8, "user_id": 1, "subscription_id": 1, "amount": 19.0, "currency": "USD", "status": "completed", "created_at": "2024-07-15T10:05:00"},
]

@app.get("/health")
async def health():
    return {"status": "ok", "app": "MicroToolKit", "version": "1.0.0"}

@app.get("/api/info")
async def info():
    return {
        "name": "PixelForge Studios",
        "app": "MicroToolKit",
        "tagline": "Empowering solopreneurs with affordable micro-tools",
        "founded": "2023",
        "team_size": 8,
        "headquarters": "Austin, TX",
        "tools_count": 6,
        "active_users": 2345,
        "monthly_revenue": 45800
    }

@app.get("/api/metrics")
async def metrics():
    return {
        "total_users": 2345,
        "active_subscriptions": 1567,
        "mrr": 45800,
        "arpu": 29.20,
        "churn_rate": 3.2,
        "trial_conversion": 18.5,
        "active_tools": 6,
        "total_payments_month": 48900
    }

@app.get("/api/stats")
async def stats():
    return {
        "users_by_plan": {"free": 778, "pro": 892, "growth": 675},
        "revenue_by_tool": [
            {"tool": "InvoiceBot", "revenue": 9876, "subscribers": 234},
            {"tool": "ContentScribe", "revenue": 7938, "subscribers": 567},
            {"tool": "LeadScraper", "revenue": 10005, "subscribers": 345},
            {"tool": "ScheduleGenius", "revenue": 8019, "subscribers": 891},
            {"tool": "AnalytixMini", "revenue": 8136, "subscribers": 678},
            {"tool": "SocialPilot", "revenue": 10152, "subscribers": 423}
        ],
        "daily_active_users": 892,
        "avg_session_minutes": 14.5
    }

@app.get("/api/recent-activity")
async def recent_activity():
    return [
        {"id": 1, "user": "Sarah Chen", "action": "Upgraded to Pro plan", "tool": "InvoiceBot", "timestamp": "2 hours ago"},
        {"id": 2, "user": "Marcus Johnson", "action": "Exported 50 leads", "tool": "LeadScraper", "timestamp": "3 hours ago"},
        {"id": 3, "user": "Elena Rodriguez", "action": "Started free trial", "tool": "ContentScribe", "timestamp": "5 hours ago"},
        {"id": 4, "user": "Lisa Thompson", "action": "Generated invoice", "tool": "InvoiceBot", "timestamp": "6 hours ago"},
        {"id": 5, "user": "David Park", "action": "Scheduled 3 posts", "tool": "SocialPilot", "timestamp": "8 hours ago"},
        {"id": 6, "user": "Anna Kim", "action": "Viewed analytics report", "tool": "AnalytixMini", "timestamp": "12 hours ago"},
        {"id": 7, "user": "James Wilson", "action": "Cancelled subscription", "tool": "ScheduleGenius", "timestamp": "1 day ago"},
        {"id": 8, "user": "Sarah Chen", "action": "Created meeting", "tool": "ScheduleGenius", "timestamp": "1 day ago"}
    ]

@app.get("/api/chart-data")
async def chart_data():
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return {
        "new_users": [45, 52, 48, 63, 55, 38, 41],
        "active_sessions": [230, 280, 310, 290, 350, 220, 195],
        "revenue": [3200, 3800, 4100, 3900, 4500, 2800, 2500],
        "labels": days
    }

@app.get("/api/users")
async def get_users():
    if SessionLocal:
        db = SessionLocal()
        users = db.query(User).all()
        db.close()
        return [{"id": u.id, "email": u.email, "name": u.name, "joined_date": u.joined_date.isoformat(), "plan": u.plan} for u in users]
    return MOCK_USERS

@app.get("/api/tools")
async def get_tools():
    if SessionLocal:
        db = SessionLocal()
        tools = db.query(Tool).all()
        db.close()
        return [{"id": t.id, "name": t.name, "description": t.description, "category": t.category, "monthly_price": t.monthly_price, "active_users": t.active_users} for t in tools]
    return MOCK_TOOLS

@app.get("/api/subscriptions")
async def get_subscriptions():
    if SessionLocal:
        db = SessionLocal()
        subs = db.query(Subscription).all()
        db.close()
        return [{"id": s.id, "user_id": s.user_id, "tool_id": s.tool_id, "plan_name": s.plan_name, "price": s.price, "start_date": s.start_date.isoformat(), "status": s.status} for s in subs]
    return MOCK_SUBSCRIPTIONS

@app.get("/api/payments")
async def get_payments():
    if SessionLocal:
        db = SessionLocal()
        payments = db.query(Payment).all()
        db.close()
        return [{"id": p.id, "user_id": p.user_id, "subscription_id": p.subscription_id, "amount": p.amount, "currency": p.currency, "status": p.status, "created_at": p.created_at.isoformat()} for p in payments]
    return MOCK_PAYMENTS

@app.get("/api/usage-logs")
async def get_usage_logs():
    if SessionLocal:
        db = SessionLocal()
        logs = db.query(UsageLog).all()
        db.close()
        return [{"id": l.id, "user_id": l.user_id, "tool_id": l.tool_id, "action": l.action, "timestamp": l.timestamp.isoformat()} for l in logs]
    return MOCK_USAGE_LOGS

@app.get("/api/tools/{tool_id}")
async def get_tool(tool_id: int):
    if SessionLocal:
        db = SessionLocal()
        tool = db.query(Tool).filter(Tool.id == tool_id).first()
        db.close()
        if not tool:
            raise HTTPException(404, "Tool not found")
        return {"id": tool.id, "name": tool.name, "description": tool.description, "category": tool.category, "monthly_price": tool.monthly_price, "active_users": tool.active_users}
    for t in MOCK_TOOLS:
        if t["id"] == tool_id:
            return t
    raise HTTPException(404, "Tool not found")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    if SessionLocal:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        if not user:
            raise HTTPException(404, "User not found")
        return {"id": user.id, "email": user.email, "name": user.name, "joined_date": user.joined_date.isoformat(), "plan": user.plan}
    for u in MOCK_USERS:
        if u["id"] == user_id:
            return u
    raise HTTPException(404, "User not found")

@app.get("/api/users/{user_id}/subscriptions")
async def get_user_subscriptions(user_id: int):
    if SessionLocal:
        db = SessionLocal()
        subs = db.query(Subscription).filter(Subscription.user_id == user_id).all()
        db.close()
        return [{"id": s.id, "user_id": s.user_id, "tool_id": s.tool_id, "plan_name": s.plan_name, "price": s.price, "start_date": s.start_date.isoformat(), "status": s.status} for s in subs]
    return [s for s in MOCK_SUBSCRIPTIONS if s["user_id"] == user_id]

class UserCreate(BaseModel):
    email: str
    name: str
    plan: str = "free"

@app.post("/api/users")
async def create_user(user: UserCreate):
    if SessionLocal:
        db = SessionLocal()
        db_user = User(email=user.email, name=user.name, plan=user.plan)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        new_user = {"id": db_user.id, "email": db_user.email, "name": db_user.name, "joined_date": db_user.joined_date.isoformat(), "plan": db_user.plan}
        db.close()
        return new_user
    new_id = max(u["id"] for u in MOCK_USERS) + 1
    new_user = {"id": new_id, "email": user.email, "name": user.name, "joined_date": datetime.utcnow().isoformat(), "plan": user.plan}
    MOCK_USERS.append(new_user)
    return new_user

class SubscriptionCreate(BaseModel):
    user_id: int
    tool_id: int
    plan_name: str
    price: float

@app.post("/api/subscriptions")
async def create_subscription(sub: SubscriptionCreate):
    if SessionLocal:
        db = SessionLocal()
        db_sub = Subscription(user_id=sub.user_id, tool_id=sub.tool_id, plan_name=sub.plan_name, price=sub.price)
        db.add(db_sub)
        db.commit()
        db.refresh(db_sub)
        new_sub = {"id": db_sub.id, "user_id": db_sub.user_id, "tool_id": db_sub.tool_id, "plan_name": db_sub.plan_name, "price": db_sub.price, "start_date": db_sub.start_date.isoformat(), "status": db_sub.status}
        db.close()
        return new_sub
    new_id = max(s["id"] for s in MOCK_SUBSCRIPTIONS) + 1
    new_sub = {"id": new_id, "user_id": sub.user_id, "tool_id": sub.tool_id, "plan_name": sub.plan_name, "price": sub.price, "start_date": datetime.utcnow().isoformat(), "status": "active"}
    MOCK_SUBSCRIPTIONS.append(new_sub)
    return new_sub

if __name__ == "__main__":
    PORT = int(os.environ.get("COMPANY_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)