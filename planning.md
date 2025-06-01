# InfluencerFlow AI Platform - MVP Backend API Documentation

## Overview
This document outlines the backend API specification for the InfluencerFlow AI Platform MVP using Python FastAPI. The MVP focuses on core functionality without authentication, using mock data for contracts and payments.

## Tech Stack
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis
- **AI/ML**: OpenAI GPT-4 API
- **File Storage**: Local filesystem (for MVP)
- **Task Queue**: Celery with Redis

## Project Structure
```
influencerflow-backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── redis.py
│   ├── models/
│   │   ├── creator.py
│   │   ├── campaign.py
│   │   ├── contract.py
│   │   └── payment.py
│   ├── schemas/
│   │   ├── creator.py
│   │   ├── campaign.py
│   │   ├── contract.py
│   │   └── payment.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── creators.py
│   │   │   ├── campaigns.py
│   │   │   ├── contracts.py
│   │   │   ├── payments.py
│   │   │   └── analytics.py
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── creator_service.py
│   │   └── payment_service.py
│   └── utils/
│       └── mock_data.py
├── requirements.txt
└── docker-compose.yml
```

## Database Models

## Database Models

### Creator Model
```python
class Creator(Base):
    id: UUID
    name: str
    email: str
    platform: str (instagram, youtube, tiktok, twitter)
    followers_count: str  # Display format like "125K", "1.2M"
    followers_count_numeric: int  # Actual number for calculations
    engagement_rate: float
    niche: str (fitness, technology, beauty, food, travel, fashion)
    language: str
    country: str
    avg_views: int
    collaboration_rate: float
    rating: float
    profile_image: str
    created_at: datetime
    updated_at: datetime
```

### Campaign Model
```python
class Campaign(Base):
    id: UUID
    product_name: str
    brand_name: str
    product_description: str
    target_audience: str
    key_use_cases: str
    campaign_goal: str
    product_niche: str
    total_budget: float
    status: str (active, draft, completed, paused)
    influencer_count: int
    created_at: datetime
    updated_at: datetime
```

### Contract Model
```python
class Contract(Base):
    id: UUID
    campaign_id: UUID
    creator_id: UUID
    terms: JSON
    deliverables: JSON
    payment_amount: float
    payment_schedule: JSON
    status: str (draft, sent, signed, completed)
    signed_at: datetime
    created_at: datetime
    updated_at: datetime
```

### Outreach Model
```python
class OutreachLog(Base):
    id: UUID
    campaign_id: UUID
    influencer_id: UUID
    call_status: str (pending, scheduled, completed, no_answer, cancelled)
    email_status: str (pending, sent, replied, bounced)
    call_recording_url: str
    call_transcript: TEXT
    call_duration_minutes: int
    last_contact_date: datetime
    notes: TEXT
    next_steps: TEXT
    sentiment: str (positive, neutral, negative)
    created_at: datetime
    updated_at: datetime
```

## API Endpoints

### 1. Creator Discovery Engine

#### GET /api/v1/creators
Search and filter creators with match scoring
```json
Query Parameters:
- search: str (optional) - Search by influencer name
- platform: str (optional) - instagram, youtube, tiktok, twitter
- niche: str (optional) - fitness, technology, beauty, food, travel, fashion
- min_followers: int (optional)
- max_followers: int (optional)
- country: str (optional)
- language: str (optional)
- min_engagement: float (optional)
- limit: int (default: 20)
- offset: int (default: 0)

Response:
{
  "creators": [
    {
      "id": "uuid",
      "name": "Sarah Johnson",
      "platform": "instagram",
      "followers_count": "125K",
      "engagement_rate": 4.5,
      "niche": "Fitness",
      "match_percentage": 85,
      "match_status": "high", // high, medium, low
      "profile_image": "https://example.com/profile.jpg"
    },
    {
      "id": "uuid",
      "name": "Tech Mike",
      "platform": "youtube",
      "followers_count": "450K",
      "engagement_rate": 3.8,
      "niche": "Technology",
      "match_percentage": 45,
      "match_status": "low",
      "profile_image": "https://example.com/profile2.jpg"
    },
    {
      "id": "uuid",
      "name": "Beauty by Emma",
      "platform": "tiktok",
      "followers_count": "380K",
      "engagement_rate": 6.1,
      "niche": "Beauty",
      "match_percentage": 70,
      "match_status": "medium",
      "profile_image": "https://example.com/profile3.jpg"
    }
  ],
  "total": 6,
  "filters_applied": {
    "niche": "all",
    "platform": "all",
    "size": "all"
  }
}
```

#### POST /api/v1/creators/search
AI-powered creator search
```json
Request Body:
{
  "query": "Find tech YouTubers with 100K+ subscribers who review gadgets",
  "budget_range": [500, 2000],
  "target_audience": "tech enthusiasts aged 18-35"
}

Response:
{
  "creators": [...],
  "search_insights": {
    "query_interpretation": "Looking for technology content creators...",
    "recommended_filters": ["tech", "gadgets", "reviews"],
    "budget_analysis": "Budget range suitable for micro to mid-tier influencers"
  }
}
```

#### GET /api/v1/creators/{creator_id}
Get detailed creator profile with campaign match analysis
```json
Query Parameters:
- campaign_id: UUID (optional) - for match analysis

Response:
{
  "id": "uuid",
  "name": "Sarah Johnson",
  "platform": "Instagram",
  "niche": "Fitness",
  "about": "Certified personal trainer sharing workout routines and healthy lifestyle tips",
  "followers": "125K",
  "followers_numeric": 125000,
  "engagement_rate": 4.2,
  "avg_views": "15K",
  "location": "Los Angeles, CA",
  "audience_type": "Fitness Enthusiasts",
  "languages": ["English"],
  "previous_brands": ["Nike", "Adidas", "Protein World"],
  "profile_image": "https://example.com/profiles/sarah.jpg",
  "campaign_match": {
    "percentage": 85,
    "status": "high",
    "reasons": [
      {
        "factor": "Perfect niche alignment",
        "description": "Creator's fitness niche perfectly matches campaign requirements",
        "impact": "high"
      },
      {
        "factor": "High engagement rate",
        "description": "4.2% engagement rate exceeds industry average of 3.1%",
        "impact": "high"
      },
      {
        "factor": "Target demographic match",
        "description": "Audience demographics align with campaign target audience",
        "impact": "medium"
      }
    ]
  },
  "collaboration_rate": 850.0,
  "rating": 4.8
}
```

## Complete User Flow & Workflow

### 🎯 **End-to-End User Journey**

**1. Campaign Creation** → **2. AI-Powered Creator Discovery** → **3. Match Analysis & Selection** → **4. Outreach Management** → **5. Contract & Payment** → **6. Performance Tracking**

### **Step 1: Campaign Creation**
```
POST /api/v1/campaigns
→ User fills campaign form with product details, target audience, budget
→ System creates campaign with unique ID and status "draft"
```

### **Step 2: AI-Powered Creator Discovery**
```
GET /api/v1/creators?campaign_id={id}
→ AI filters creators based on campaign requirements
→ Returns creators with match percentages and ranking
→ Displays filtered list with match scores (85%, 70%, 45%, etc.)
```

### **Step 3: Match Analysis & Selection**
```
GET /api/v1/creators/{creator_id}?campaign_id={campaign_id}
→ User clicks "View Details" to see why creator matched
→ Shows detailed match breakdown and reasons

POST /api/v1/campaigns/{campaign_id}/ai-match-analysis
→ Provides AI explanation of match scoring

POST /api/v1/campaigns/{campaign_id}/select-influencer
→ User selects creator and moves to outreach phase
```

### **Step 4: Outreach Management (IRM)**
```
GET /api/v1/outreach/dashboard
→ Shows outreach overview and management tools
→ Track calls, emails, recordings, transcripts

POST /api/v1/outreach/call/schedule
→ Schedule calls with selected influencers

POST /api/v1/outreach/call/complete
→ Log call results and upload recordings
```

### **Step 5: Contract & Payment (Mock)**
```
POST /api/v1/contracts
→ Generate mock contracts after successful outreach

POST /api/v1/payments/{payment_id}/process
→ Process mock payments
```

### **Step 6: Performance Tracking**
```
GET /api/v1/analytics/campaigns/{campaign_id}
→ Track campaign performance and ROI
```

### 2. Campaign Management
Create a new campaign
```json
Request Body:
{
  "product_name": "Wireless Earbuds Pro",
  "brand_name": "TechCorp",
  "product_description": "High-quality wireless earbuds with noise cancellation and 24-hour battery life. Perfect for fitness enthusiasts and professionals.",
  "target_audience": "Tech enthusiasts aged 18-35, fitness enthusiasts, professionals who commute",
  "key_use_cases": "Fitness workouts, commuting, professional calls, music listening, noise cancellation for focus",
  "campaign_goal": "Brand awareness, Sales, Engagement",
  "product_niche": "Fitness, Tech, Beauty, Lifestyle",
  "total_budget": 15000.0
}

Response:
{
  "id": "uuid",
  "product_name": "Wireless Earbuds Pro",
  "brand_name": "TechCorp",
  "status": "draft",
  "total_budget": 15000.0,
  "created_at": "2024-06-01T10:00:00Z",
  "campaign_code": "CAMP-001"
}
```

#### GET /api/v1/campaigns
List all campaigns with dashboard summary
```json
Query Parameters:
- status: str (optional)
- limit: int (default: 20)
- offset: int (default: 0)

Response:
{
  "campaigns": [
    {
      "id": "uuid",
      "product_name": "Summer Fitness Collection",
      "brand_name": "FitLife",
      "total_budget": 10000.0,
      "status": "active",
      "influencer_count": 12,
      "campaign_code": "CAMP-001",
      "created_at": "2024-06-01T10:00:00Z"
    },
    {
      "id": "uuid",
      "product_name": "Tech Gadget Launch",
      "brand_name": "TechNova",
      "total_budget": 15000.0,
      "status": "draft",
      "influencer_count": 8,
      "campaign_code": "CAMP-002",
      "created_at": "2024-06-02T10:00:00Z"
    },
    {
      "id": "uuid",
      "product_name": "Eco-Friendly Skincare",
      "brand_name": "GreenGlow",
      "total_budget": 8500.0,
      "status": "completed",
      "influencer_count": 20,
      "campaign_code": "CAMP-003",
      "created_at": "2024-05-15T10:00:00Z"
    }
  ],
  "total": 3,
  "page": 1,
  "total_pages": 1
}
```

#### POST /api/v1/campaigns/{campaign_id}/select-influencer
Select influencer for campaign and move to outreach
```json
Request Body:
{
  "influencer_id": "uuid",
  "notes": "Great fit for our fitness campaign, high engagement with target demographic"
}

Response:
{
  "campaign_id": "uuid",
  "influencer_id": "uuid",
  "status": "selected_for_outreach",
  "outreach_entry_created": true,
  "next_step": "outreach_management",
  "outreach_id": "uuid"
}
```

#### POST /api/v1/campaigns/{campaign_id}/ai-match-analysis
Get AI-powered match analysis for campaign and influencer
```json
Request Body:
{
  "influencer_id": "uuid"
}

Response:
{
  "match_percentage": 85,
  "match_status": "high",
  "detailed_analysis": {
    "niche_alignment": {
      "score": 95,
      "explanation": "Perfect alignment - both campaign and influencer focus on fitness content"
    },
    "audience_match": {
      "score": 80,
      "explanation": "Target demographic overlaps significantly with influencer's audience"
    },
    "engagement_quality": {
      "score": 85,
      "explanation": "Above-average engagement rate indicates strong audience connection"
    },
    "brand_safety": {
      "score": 90,
      "explanation": "Previous collaborations with reputable fitness brands show professionalism"
    }
  },
  "recommendation": "Highly recommended for this campaign",
  "estimated_performance": {
    "expected_reach": "100K-125K",
    "expected_engagement": "4K-5.5K",
    "estimated_roi": "3.2x"
  }
}
```

### 7. Outreach Management & IRM (Influencer Relationship Management)

#### GET /api/v1/outreach/dashboard
Get outreach management overview
```json
Query Parameters:
- campaign_filter: str (optional) - "All Campaigns" or specific campaign ID

Response:
{
  "summary": {
    "total_contacts": 5,
    "calls_completed": 2,
    "email_replies": 2,
    "recordings": 2
  },
  "outreach_log": [
    {
      "campaign_id": "CAMP-001",
      "influencer_name": "Sarah Johnson",
      "call_status": "completed",
      "email_status": "sent",
      "has_recording": true,
      "has_transcript": true,
      "last_contact": "2024-01-15"
    },
    {
      "campaign_id": "CAMP-001",
      "influencer_name": "Tech Mike",
      "call_status": "scheduled",
      "email_status": "replied",
      "has_recording": false,
      "has_transcript": false,
      "last_contact": "2024-01-14"
    },
    {
      "campaign_id": "CAMP-002",
      "influencer_name": "Beauty by Emma",
      "call_status": "pending",
      "email_status": "sent",
      "has_recording": false,
      "has_transcript": false,
      "last_contact": "2024-01-13"
    },
    {
      "campaign_id": "CAMP-001",
      "influencer_name": "Chef Carlos",
      "call_status": "completed",
      "email_status": "replied",
      "has_recording": true,
      "has_transcript": true,
      "last_contact": "2024-01-12"
    },
    {
      "campaign_id": "CAMP-003",
      "influencer_name": "Travel with Lisa",
      "call_status": "no answer",
      "email_status": "pending",
      "has_recording": false,
      "has_transcript": false,
      "last_contact": "2024-01-11"
    }
  ]
}
```

#### POST /api/v1/outreach/call/schedule
Schedule a call with an influencer
```json
Request Body:
{
  "campaign_id": "CAMP-001",
  "influencer_id": "uuid",
  "scheduled_time": "2024-01-16T14:00:00Z",
  "notes": "Initial discussion about fitness campaign collaboration"
}

Response:
{
  "call_id": "uuid",
  "status": "scheduled",
  "calendar_link": "https://calendar.example.com/meeting/uuid",
  "reminder_sent": true
}
```

#### POST /api/v1/outreach/call/complete
Mark call as completed and upload recording
```json
Request Body:
{
  "call_id": "uuid",
  "status": "completed",
  "duration_minutes": 25,
  "recording_url": "https://storage.example.com/recordings/uuid.mp3",
  "transcript": "Auto-generated transcript text...",
  "notes": "Positive response, interested in collaboration",
  "next_steps": "Send contract for review"
}

Response:
{
  "call_id": "uuid",
  "status": "completed",
  "transcript_generated": true,
  "follow_up_created": true
}
```

#### GET /api/v1/outreach/call/{call_id}/recording
Download call recording
```json
Response: Audio file download (MP3/WAV)
```

#### GET /api/v1/outreach/call/{call_id}/transcript
Get call transcript
```json
Response:
{
  "call_id": "uuid",
  "transcript": "Full conversation transcript...",
  "summary": "Key points discussed during the call",
  "action_items": [
    "Send product samples",
    "Draft contract terms",
    "Schedule follow-up call"
  ],
  "sentiment": "positive"
}
```

### Payment Model
```python
class Payment(Base):
    id: UUID
    contract_id: UUID
    amount: float
    status: str (pending, processing, completed, failed)
    payment_method: str
    transaction_id: str
    due_date: datetime
    paid_at: datetime
    created_at: datetime
    updated_at: datetime
```

#### POST /api/v1/contracts
Create a new contract
```json
Request Body:
{
  "campaign_id": "uuid",
  "creator_id": "uuid",
  "terms": {
    "deliverables": [
      {
        "type": "youtube_video",
        "deadline": "2024-07-10T00:00:00Z",
        "requirements": ["5-8 minutes", "honest review", "CTA included"]
      }
    ],
    "usage_rights": "6 months",
    "exclusivity": "tech category for 30 days"
  },
  "payment_amount": 1200.0,
  "payment_schedule": [
    {
      "milestone": "contract_signing",
      "amount": 400.0,
      "percentage": 33
    },
    {
      "milestone": "content_delivery",
      "amount": 800.0,
      "percentage": 67
    }
  ]
}

Response:
{
  "id": "uuid",
  "status": "draft",
  "contract_url": "/api/v1/contracts/uuid/pdf",
  "created_at": "2024-06-01T15:00:00Z"
}
```

#### GET /api/v1/contracts
List contracts
```json
Query Parameters:
- campaign_id: UUID (optional)
- creator_id: UUID (optional)
- status: str (optional)
- limit: int (default: 20)
- offset: int (default: 0)

Response:
{
  "contracts": [
    {
      "id": "uuid",
      "campaign_title": "Summer Tech Product Launch",
      "creator_name": "TechReviewer123",
      "payment_amount": 1200.0,
      "status": "signed",
      "signed_at": "2024-06-02T10:30:00Z"
    }
  ],
  "total": 5,
  "page": 1,
  "total_pages": 1
}
```

#### GET /api/v1/contracts/{contract_id}
Get contract details
```json
Response:
{
  "id": "uuid",
  "campaign": {
    "id": "uuid",
    "title": "Summer Tech Product Launch"
  },
  "creator": {
    "id": "uuid",
    "name": "TechReviewer123"
  },
  "terms": {...},
  "payment_amount": 1200.0,
  "payment_schedule": [...],
  "status": "signed",
  "signed_at": "2024-06-02T10:30:00Z",
  "deliverables_status": [
    {
      "type": "youtube_video",
      "status": "pending",
      "deadline": "2024-07-10T00:00:00Z"
    }
  ]
}
```

#### GET /api/v1/contracts/{contract_id}/pdf
Generate contract PDF
```json
Response: PDF file download
```

### 5. Payment Management

#### GET /api/v1/payments
List payments
```json
Query Parameters:
- contract_id: UUID (optional)
- status: str (optional)
- limit: int (default: 20)
- offset: int (default: 0)

Response:
{
  "payments": [
    {
      "id": "uuid",
      "contract_id": "uuid",
      "amount": 400.0,
      "status": "completed",
      "payment_method": "stripe",
      "due_date": "2024-06-02T00:00:00Z",
      "paid_at": "2024-06-02T14:20:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "total_pages": 1
}
```

#### POST /api/v1/payments/{payment_id}/process
Process payment (Mock implementation)
```json
Request Body:
{
  "payment_method": "stripe",
  "payment_details": {
    "card_token": "mock_token_123"
  }
}

Response:
{
  "payment_id": "uuid",
  "status": "processing",
  "transaction_id": "txn_mock_123456",
  "estimated_completion": "2024-06-01T16:00:00Z"
}
```

#### GET /api/v1/payments/dashboard
Payment dashboard summary
```json
Response:
{
  "total_payments": {
    "amount": 25000.0,
    "count": 15
  },
  "pending_payments": {
    "amount": 3200.0,
    "count": 3
  },
  "completed_payments": {
    "amount": 21800.0,
    "count": 12
  },
  "recent_payments": [
    {
      "id": "uuid",
      "creator_name": "TechReviewer123",
      "amount": 800.0,
      "status": "completed",
      "paid_at": "2024-06-01T14:20:00Z"
    }
  ]
}
```

### 6. Analytics & Reporting

#### GET /api/v1/analytics/campaigns/{campaign_id}
Campaign performance analytics
```json
Response:
{
  "campaign_id": "uuid",
  "performance": {
    "total_reach": 450000,
    "total_engagement": 25000,
    "total_views": 380000,
    "average_engagement_rate": 6.5,
    "roi": 3.2
  },
  "creator_performance": [
    {
      "creator_id": "uuid",
      "creator_name": "TechReviewer123",
      "content_views": 125000,
      "engagement": 8500,
      "engagement_rate": 6.8,
      "delivery_status": "completed"
    }
  ],
  "timeline": [
    {
      "date": "2024-06-01",
      "views": 15000,
      "engagement": 950
    }
  ]
}
```

#### GET /api/v1/analytics/dashboard
Overall platform analytics
```json
Response:
{
  "overview": {
    "total_campaigns": 12,
    "active_campaigns": 3,
    "total_creators": 145,
    "total_contracts": 28,
    "total_budget_managed": 125000.0
  },
  "performance_metrics": {
    "average_campaign_roi": 2.8,
    "average_engagement_rate": 5.2,
    "creator_satisfaction_score": 4.6,
    "contract_completion_rate": 89.3
  },
  "recent_activity": [
    {
      "type": "contract_signed",
      "description": "Contract signed with TechReviewer123",
      "timestamp": "2024-06-01T10:30:00Z"
    }
  ]
}
```

## Mock Data Service

### Mock Data Service

### Creator Mock Data
```python
# Generate 50+ mock creators across different platforms
MOCK_CREATORS = [
    {
        "name": "Sarah Johnson",
        "platform": "instagram",
        "followers_count": "125K",
        "followers_count_numeric": 125000,
        "niche": "Fitness",
        "engagement_rate": 4.5,
        "country": "US",
        "match_percentage": 85,
        "profile_image": "https://example.com/profiles/sarah.jpg"
    },
    {
        "name": "Tech Mike",
        "platform": "youtube",
        "followers_count": "450K",
        "followers_count_numeric": 450000,
        "niche": "Technology",
        "engagement_rate": 3.8,
        "country": "US",
        "match_percentage": 45,
        "profile_image": "https://example.com/profiles/tech_mike.jpg"
    },
    {
        "name": "Beauty by Emma",
        "platform": "tiktok",
        "followers_count": "380K",
        "followers_count_numeric": 380000,
        "niche": "Beauty",
        "engagement_rate": 6.1,
        "country": "UK",
        "match_percentage": 70,
        "profile_image": "https://example.com/profiles/emma.jpg"
    },
    {
        "name": "Chef Carlos",
        "platform": "instagram",
        "followers_count": "220K",
        "followers_count_numeric": 220000,
        "niche": "Food",
        "engagement_rate": 5.3,
        "country": "Spain",
        "match_percentage": 60,
        "profile_image": "https://example.com/profiles/carlos.jpg"
    },
    {
        "name": "Travel with Lisa",
        "platform": "youtube",
        "followers_count": "95K",
        "followers_count_numeric": 95000,
        "niche": "Travel",
        "engagement_rate": 4.7,
        "country": "Australia",
        "match_percentage": 40,
        "profile_image": "https://example.com/profiles/lisa.jpg"
    },
    {
        "name": "Style Maven",
        "platform": "instagram",
        "followers_count": "310K",
        "followers_count_numeric": 310000,
        "niche": "Fashion",
        "engagement_rate": 4.9,
        "country": "France",
        "match_percentage": 75,
        "profile_image": "https://example.com/profiles/style_maven.jpg"
    }
    # ... more creators
]
```

### Campaign Mock Data
```python
MOCK_CAMPAIGNS = [
    {
        "product_name": "Summer Fitness Collection",
        "brand_name": "FitLife",
        "total_budget": 10000.0,
        "status": "active",
        "influencer_count": 12,
        "campaign_code": "CAMP-001"
    },
    {
        "product_name": "Tech Gadget Launch",
        "brand_name": "TechNova",
        "total_budget": 15000.0,
        "status": "draft",
        "influencer_count": 8,
        "campaign_code": "CAMP-002"
    },
    {
        "product_name": "Eco-Friendly Skincare",
        "brand_name": "GreenGlow",
        "total_budget": 8500.0,
        "status": "completed",
        "influencer_count": 20,
        "campaign_code": "CAMP-003"
    }
    # ... more campaigns
]
```

### Outreach Mock Data
```python
MOCK_OUTREACH_LOG = [
    {
        "campaign_id": "CAMP-001",
        "influencer_name": "Sarah Johnson",
        "call_status": "completed",
        "email_status": "sent",
        "has_recording": True,
        "has_transcript": True,
        "last_contact": "2024-01-15",
        "duration_minutes": 25,
        "sentiment": "positive"
    },
    {
        "campaign_id": "CAMP-001",
        "influencer_name": "Tech Mike",
        "call_status": "scheduled",
        "email_status": "replied",
        "has_recording": False,
        "has_transcript": False,
        "last_contact": "2024-01-14"
    }
    # ... more outreach logs
]
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    },
    "timestamp": "2024-06-01T10:00:00Z"
  }
}
```

### HTTP Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 422: Validation Error
- 500: Internal Server Error

## Environment Configuration

### Required Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/influencerflow

# Redis
REDIS_URL=redis://localhost:6379

# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Mock Payment Gateway
STRIPE_SECRET_KEY=mock_stripe_key
STRIPE_WEBHOOK_SECRET=mock_webhook_secret

# App Settings
DEBUG=True
LOG_LEVEL=INFO
```

## Development Setup

### Installation
```bash
pip install -r requirements.txt
```

### Database Migration
```bash
alembic upgrade head
```

### Run Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Run with Docker
```bash
docker-compose up -d
```

## API Testing

### Swagger UI
Available at: `http://localhost:8000/docs`

### ReDoc
Available at: `http://localhost:8000/redoc`

### Sample cURL Commands
```bash
# Get campaign dashboard
curl -X GET "http://localhost:8000/api/v1/campaigns"

# Create campaign
curl -X POST "http://localhost:8000/api/v1/campaigns" \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "Wireless Earbuds Pro",
    "brand_name": "TechCorp",
    "product_description": "High-quality wireless earbuds with noise cancellation",
    "target_audience": "Tech enthusiasts aged 18-35",
    "key_use_cases": "Fitness workouts, commuting, professional calls",
    "campaign_goal": "Brand awareness, Sales",
    "product_niche": "Fitness, Tech",
    "total_budget": 15000.0
  }'

# Search creators with filters
curl -X GET "http://localhost:8000/api/v1/creators?platform=instagram&niche=fitness&min_followers=100000"

# Get outreach dashboard
curl -X GET "http://localhost:8000/api/v1/outreach/dashboard?campaign_filter=All%20Campaigns"

# Schedule a call
curl -X POST "http://localhost:8000/api/v1/outreach/call/schedule" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "CAMP-001",
    "influencer_id": "uuid",
    "scheduled_time": "2024-01-16T14:00:00Z",
    "notes": "Initial discussion about collaboration"
  }'
```

## Performance Considerations

### Caching Strategy
- Creator search results cached for 1 hour
- Campaign data cached for 30 minutes
- Analytics data cached for 15 minutes

### Database Indexing
- Creators: platform, niche, followers_count, country
- Campaigns: status, created_at
- Contracts: campaign_id, creator_id, status
- Payments: contract_id, status, due_date

### Rate Limiting
- AI API calls: 100 requests per minute
- General API endpoints: 1000 requests per minute per IP

This MVP backend provides a solid foundation for the InfluencerFlow AI Platform with all core functionalities while maintaining simplicity and scalability for future enhancements.