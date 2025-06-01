from fastapi import APIRouter
from app.api.v1 import creators, campaigns, contracts, payments, analytics, outreach, ai

# Create main API router
api_router = APIRouter()

# Include all API endpoint routers
api_router.include_router(creators.router, prefix="/creators", tags=["creators"])
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
api_router.include_router(payments.router, prefix="/payments", tags=["payments"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(outreach.router, prefix="/outreach", tags=["outreach"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
