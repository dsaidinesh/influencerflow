# InfluencerFlow AI Platform API Documentation

This document outlines the API endpoints available in the InfluencerFlow AI Platform, which helps manage influencer marketing campaigns.

## Base URL

All API endpoints are relative to your base URL (e.g., `https://api.influencerflow.com`).

## Authentication

Authentication details are required for accessing these endpoints. Please contact the API administrator for credentials.

## Resource Groups

The API is organized into the following resource groups:

- Creators
- Campaigns
- Contracts
- Payments
- Outreach
- Analytics
- AI Matching

## Endpoints

### Creators

#### List Creators

```
GET /api/v1/creators/
```

Search and filter creators with match scoring.

**Query Parameters:**
- `search` (string, optional): Search term
- `platform` (string, optional): Filter by platform
- `niche` (string, optional): Filter by niche
- `min_followers` (integer, optional): Minimum follower count
- `max_followers` (integer, optional): Maximum follower count
- `country` (string, optional): Filter by country
- `language` (string, optional): Filter by language
- `min_engagement` (number, optional): Minimum engagement rate
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset

**Response:** 200 OK - List of creators

#### Create Creator

```
POST /api/v1/creators/
```

Create a new creator.

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "platform": "instagram|youtube|tiktok|twitter",
  "followers_count": "string",
  "followers_count_numeric": "integer",
  "engagement_rate": "number",
  "niche": "fitness|technology|beauty|food|travel|fashion",
  "language": "string",
  "country": "string",
  "about": "string",
  "channel_name": "string",
  "avg_views": "integer",
  "collaboration_rate": "number",
  "profile_image": "string"
}
```

**Response:** 200 OK - Created creator details

#### AI-Powered Creator Search

```
POST /api/v1/creators/search
```

AI-powered creator search.

**Request Body:**
```json
{
  "query": "object"
}
```

**Response:** 200 OK - Search results

#### Get Creator by ID

```
GET /api/v1/creators/{creator_id}
```

Get detailed creator profile with campaign match analysis.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator to get

**Query Parameters:**
- `campaign_id` (string, optional): Campaign ID for match analysis

**Response:** 200 OK - Creator details

#### Update Creator

```
PUT /api/v1/creators/{creator_id}
```

Update an existing creator.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator to update

**Request Body:**
```json
{
  "name": "string",
  "email": "string",
  "platform": "instagram|youtube|tiktok|twitter",
  "followers_count": "string",
  "followers_count_numeric": "integer",
  "engagement_rate": "number",
  "niche": "fitness|technology|beauty|food|travel|fashion",
  "language": "string",
  "country": "string",
  "about": "string",
  "channel_name": "string",
  "avg_views": "integer",
  "collaboration_rate": "number",
  "rating": "number",
  "profile_image": "string"
}
```

**Response:** 200 OK - Updated creator details

#### Delete Creator

```
DELETE /api/v1/creators/{creator_id}
```

Delete a creator.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator to delete

**Response:** 200 OK - Deletion confirmation

### Campaigns

#### List Campaigns

```
GET /api/v1/campaigns/
```

List all campaigns.

**Query Parameters:**
- `status` (string, optional): Filter by status
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset

**Response:** 200 OK - List of campaigns

#### Create Campaign

```
POST /api/v1/campaigns/
```

Create a new campaign.

**Request Body:**
```json
{
  "product_name": "string",
  "brand_name": "string",
  "product_description": "string",
  "target_audience": "string",
  "key_use_cases": "string",
  "campaign_goal": "string",
  "product_niche": "string",
  "total_budget": "number"
}
```

**Response:** 200 OK - Created campaign details

#### Get Campaign by ID

```
GET /api/v1/campaigns/{campaign_id}
```

Get campaign by ID.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign to get

**Response:** 200 OK - Campaign details

#### Update Campaign

```
PUT /api/v1/campaigns/{campaign_id}
```

Update an existing campaign.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign to update

**Request Body:**
```json
{
  "product_name": "string",
  "brand_name": "string",
  "product_description": "string",
  "target_audience": "string",
  "key_use_cases": "string",
  "campaign_goal": "string",
  "product_niche": "string",
  "total_budget": "number",
  "status": "active|draft|completed|paused"
}
```

**Response:** 200 OK - Updated campaign details

#### Delete Campaign

```
DELETE /api/v1/campaigns/{campaign_id}
```

Delete a campaign.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign to delete

**Response:** 200 OK - Deletion confirmation

#### Get Campaigns by Brand

```
GET /api/v1/campaigns/brand/{brand_name}
```

Get campaigns for a specific brand.

**Path Parameters:**
- `brand_name` (string, required): The brand name to filter campaigns by

**Response:** 200 OK - List of campaigns for the brand

#### Select Influencer for Campaign

```
POST /api/v1/campaigns/{campaign_id}/select-influencer
```

Select influencer for campaign and move to outreach.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign

**Request Body:**
```json
{
  "influencer_id": "string",
  "notes": "string"
}
```

**Response:** 200 OK - Selection confirmation

#### Analyze Campaign-Influencer Match

```
POST /api/v1/campaigns/{campaign_id}/ai-match-analysis
```

Get AI-powered match analysis for campaign and influencer.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign

**Request Body:**
```json
{
  "influencer_id": "string"
}
```

**Response:** 200 OK - Match analysis results

### Contracts

#### List Contracts

```
GET /api/v1/contracts/
```

List all contracts.

**Query Parameters:**
- `campaign_id` (string, optional): Filter by campaign
- `creator_id` (string, optional): Filter by creator
- `status` (string, optional): Filter by status
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset

**Response:** 200 OK - List of contracts

#### Create Contract

```
POST /api/v1/contracts/
```

Create a new contract.

**Request Body:**
```json
{
  "campaign_id": "string",
  "creator_id": "string",
  "terms": "object",
  "payment_amount": "number",
  "payment_schedule": "array"
}
```

**Response:** 200 OK - Created contract details

#### Get Contract by ID

```
GET /api/v1/contracts/{contract_id}
```

Get contract by ID.

**Path Parameters:**
- `contract_id` (string, required): The ID of the contract to get

**Response:** 200 OK - Contract details

#### Update Contract

```
PUT /api/v1/contracts/{contract_id}
```

Update an existing contract.

**Path Parameters:**
- `contract_id` (string, required): The ID of the contract to update

**Request Body:**
```json
{
  "terms": "object",
  "payment_amount": "number",
  "payment_schedule": "array",
  "status": "draft|sent|signed|completed"
}
```

**Response:** 200 OK - Updated contract details

#### Sign Contract

```
POST /api/v1/contracts/{contract_id}/sign
```

Sign a contract.

**Path Parameters:**
- `contract_id` (string, required): The ID of the contract to sign

**Response:** 200 OK - Signing confirmation

#### Generate Contract Document

```
GET /api/v1/contracts/{contract_id}/pdf
```

Generate contract document.

**Path Parameters:**
- `contract_id` (string, required): The ID of the contract to generate PDF for

**Response:** 200 OK - Document URL or content

#### Get Contracts by Campaign

```
GET /api/v1/contracts/campaign/{campaign_id}
```

Get all contracts for a campaign.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign

**Response:** 200 OK - List of contracts for the campaign

#### Get Contracts by Creator

```
GET /api/v1/contracts/creator/{creator_id}
```

Get all contracts for a creator.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator

**Response:** 200 OK - List of contracts for the creator

### Payments

#### List Payments

```
GET /api/v1/payments/
```

List all payments.

**Query Parameters:**
- `contract_id` (string, optional): Filter by contract
- `status` (string, optional): Filter by status
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset

**Response:** 200 OK - List of payments

#### Create Payment

```
POST /api/v1/payments/
```

Create a new payment.

**Request Body:**
```json
{
  "contract_id": "string",
  "amount": "number",
  "due_date": "string (date-time)"
}
```

**Response:** 200 OK - Created payment details

#### Get Payment by ID

```
GET /api/v1/payments/{payment_id}
```

Get payment by ID.

**Path Parameters:**
- `payment_id` (string, required): The ID of the payment to get

**Response:** 200 OK - Payment details

#### Update Payment

```
PUT /api/v1/payments/{payment_id}
```

Update an existing payment.

**Path Parameters:**
- `payment_id` (string, required): The ID of the payment to update

**Request Body:**
```json
{
  "amount": "number",
  "status": "pending|processing|completed|failed",
  "payment_method": "string",
  "transaction_id": "string",
  "due_date": "string (date-time)",
  "paid_at": "string (date-time)"
}
```

**Response:** 200 OK - Updated payment details

#### Process Payment

```
POST /api/v1/payments/{payment_id}/process
```

Process a payment.

**Path Parameters:**
- `payment_id` (string, required): The ID of the payment to process

**Request Body:**
```json
{
  "payment_method": "string"
}
```

**Response:** 200 OK - Processing confirmation

#### Get Payments by Contract

```
GET /api/v1/payments/contract/{contract_id}
```

Get all payments for a contract.

**Path Parameters:**
- `contract_id` (string, required): The ID of the contract

**Response:** 200 OK - List of payments for the contract

#### Get Payment Summary

```
GET /api/v1/payments/summary
```

Get payment summary statistics.

**Response:** 200 OK - Payment summary statistics

### Outreach

#### List Outreach Logs

```
GET /api/v1/outreach/
```

List all outreach logs.

**Query Parameters:**
- `campaign_id` (string, optional): Filter by campaign
- `creator_id` (string, optional): Filter by creator
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset

**Response:** 200 OK - List of outreach logs

#### Create Outreach Log

```
POST /api/v1/outreach/
```

Create a new outreach log.

**Request Body:**
```json
{
  "campaign_id": "string",
  "creator_id": "string",
  "channel": "string",
  "message_type": "string",
  "content": "object",
  "status": "string"
}
```

**Response:** 200 OK - Created outreach log details

#### Get Outreach Log by ID

```
GET /api/v1/outreach/{log_id}
```

Get outreach log by ID.

**Path Parameters:**
- `log_id` (string, required): The ID of the outreach log to get

**Response:** 200 OK - Outreach log details

#### Update Outreach Log

```
PUT /api/v1/outreach/{log_id}
```

Update an existing outreach log.

**Path Parameters:**
- `log_id` (string, required): The ID of the outreach log to update

**Request Body:**
```json
{
  "channel": "string",
  "message_type": "string",
  "content": "object",
  "status": "string"
}
```

**Response:** 200 OK - Updated outreach log details

#### Send Outreach Email

```
POST /api/v1/outreach/email
```

Send outreach email to creator.

**Request Body:**
```json
{
  "campaign_id": "string",
  "creator_id": "string",
  "subject": "string",
  "message": "string"
}
```

**Response:** 200 OK - Email sending confirmation

#### Initiate Outbound Call to Creator (ElevenLabs)

```
POST /api/v1/outreach/call/initiate
```

Initiate an outbound call to a creator using ElevenLabs Conversational AI.

**Request Body:**
```json
{
  "campaign_id": "string",
  "creator_id": "string",
  "phone_number": "string"
}
```

**Response:**
```json
{
  "success": true,
  "conversation_id": "string",
  "outreach_id": "string",
  "call_status": "initiated",
  "message": "Call initiated successfully"
}
```

#### Get Call Analysis (ElevenLabs)

```
GET /api/v1/outreach/call/{conversation_id}/analysis
```

Get detailed call analysis from ElevenLabs for a specific conversation.

**Path Parameters:**
- `conversation_id` (string, required): The ID of the ElevenLabs conversation

**Response:**
```json
{
  "conversation_id": "string",
  "status": "string",
  "duration_seconds": "integer",
  "call_successful": "string",
  "summary": "string",
  "evaluation_results": {
    "interest_assessment": "object",
    "communication_quality": "object",
    "information_gathering": "object",
    "next_steps": "object"
  },
  "extracted_data": {
    "interest_level": "string",
    "collaboration_rate": "string",
    "content_preferences": "string",
    "timeline": "string",
    "contact_info": "string",
    "follow_up_actions": "string"
  },
  "transcript": "array"
}
```

#### Sync ElevenLabs Conversations

```
POST /api/v1/outreach/sync-conversations
```

Sync recent conversations from ElevenLabs and update outreach logs.

**Request Body:**
```json
{
  "from_date": "string (date-time, optional)",
  "limit": "integer (optional, default: 30)"
}
```

**Response:**
```json
{
  "success": true,
  "updated_conversations": "integer",
  "message": "string"
}
```

#### Get Outreach by Campaign

```
GET /api/v1/outreach/campaign/{campaign_id}
```

Get all outreach logs for a campaign.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign

**Response:** 200 OK - List of outreach logs for the campaign

#### Get Outreach by Creator

```
GET /api/v1/outreach/creator/{creator_id}
```

Get all outreach logs for a creator.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator

**Response:** 200 OK - List of outreach logs for the creator

### Analytics

#### Get Campaign Analytics

```
GET /api/v1/analytics/campaigns/{campaign_id}
```

Campaign performance analytics.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign to analyze

**Response:** 200 OK - Campaign analytics data

#### Get Analytics Dashboard

```
GET /api/v1/analytics/dashboard
```

Overall platform analytics.

**Response:** 200 OK - Platform analytics data

### AI Matching

#### AI-Powered Influencer Matching

```
POST /api/ai/similaritysearch
```

Compute AI-based similarity matching between campaign details and stored influencer embeddings.

**Request Body:**
```json
{
  "product_name": "string",
  "brand_name": "string",
  "product_description": "string",
  "target_audience": "string",
  "key_use_cases": ["string"],
  "campaign_goal": "string",
  "product_niche": "string",
  "total_budget": "number",
  "min_followers": "number",
  "max_followers": "number",
  "min_engagement": "number",
  "limit": "number"
}
```

**Response:**
```json
{
  "matches": [
    {
      "id": "string", 
      "influencer_name": "string",
      "profile_image": "string",
      "platform": "string",
      "match_score": "string",
      "niche": "string",
      "followers": "string",
      "followers_count_numeric": "number",
      "engagement": "string",
      "collaboration_rate": "string",
      "detailed_scores": {
        "niche_match": "string",
        "audience_match": "string",
        "engagement_score": "string",
        "budget_fit": "string"
      }
    }
  ],
  "total": "number",
  "page": "number",
  "pages": "number"
}
```

#### Get Saved Match Scores

```
GET /api/ai/matches/{campaign_id}
```

Retrieve previously computed match scores for a specific campaign.

**Path Parameters:**
- `campaign_id` (string, required): The ID of the campaign

**Query Parameters:**
- `limit` (integer, default: 20, max: 100): Number of results per page
- `offset` (integer, default: 0): Pagination offset
- `min_score` (number, optional): Minimum match score threshold

**Response:**
```json
{
  "matches": [
    {
      "id": "string",
      "creator_id": "string",
      "campaign_id": "string",
      "influencer_name": "string",
      "match_score": "string",
      "niche_match": "string",
      "audience_match": "string",
      "engagement_score": "string",
      "budget_fit": "string",
      "created_at": "string"
    }
  ],
  "total": "number"
}
```

#### Save Match Score

```
POST /api/ai/matches
```

Save a computed match score between a campaign and creator.

**Request Body:**
```json
{
  "campaign_id": "string",
  "creator_id": "string",
  "match_score": "number",
  "niche_match": "number",
  "audience_match": "number",
  "engagement_score": "number",
  "budget_fit": "number"
}
```

**Response:**
```json
{
  "id": "string",
  "campaign_id": "string",
  "creator_id": "string",
  "match_score": "number",
  "niche_match": "number",
  "audience_match": "number",
  "engagement_score": "number",
  "budget_fit": "number",
  "created_at": "string"
}
```

#### Generate Creator Embedding

```
POST /api/ai/embeddings/creator/{creator_id}
```

Generate or update the embedding vector for a specific creator.

**Path Parameters:**
- `creator_id` (string, required): The ID of the creator

**Response:**
```json
{
  "creator_id": "string",
  "embedding_updated": true,
  "embedding_dimensions": 1536
}
```

#### Batch Generate Creator Embeddings

```
POST /api/ai/embeddings/batch
```

Generate embeddings for multiple creators in a batch operation.

**Request Body:**
```json
{
  "creator_ids": ["string"],
  "force_update": false
}
```

**Response:**
```json
{
  "processed": "number",
  "successful": "number",
  "failed": "number",
  "details": [
    {
      "creator_id": "string",
      "status": "success|failed",
      "message": "string"
    }
  ]
}
```

## AI-Powered Influencer Matching Endpoints

### Similarity Search (Detailed)

**Endpoint:** `POST /api/v1/ai/similaritysearch`

Performs AI-powered similarity search to find the best influencer matches for a campaign.

**Request Body:**
```json
{
  "product_name": "FitBand Pro",
  "brand": "TechFit",
  "product_description": "A smart fitness band that tracks activities and provides health insights",
  "target_audience": "Health-conscious individuals aged 25-45 who are interested in tracking their fitness",
  "key_usecases": ["Activity tracking", "Heart rate monitoring", "Sleep analysis"],
  "campaign_goal": "Increase brand awareness and drive sales for the new FitBand Pro",
  "product_niche": "Fitness Technology",
  "total_budget": 25000
}
```

**Response:**
```json
{
  "matches": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "influencer_name": "Mia Martinez (@mia_martinez838)",
      "match_score": "78.31%",
      "niche": "Fitness",
      "followers": "374K",
      "engagement": "5.9%",
      "collaboration_rate": "$3769",
      "detailed_scores": {
        "niche_match": "91.60%",
        "audience_match": "43.00%",
        "engagement_score": "82.00%",
        "budget_fit": "100.00%"
      }
    },
    // Additional matches...
  ],
  "total_matches": 10,
  "search_parameters": {
    // Original request parameters
  }
}
```

### Simplified Campaign-Based Similarity Search

**Endpoint:** `POST /api/v1/ai/campaign-similarity`

Performs AI-powered similarity search using an existing campaign's details. This simplified endpoint requires only the campaign ID.

**Request Body:**
```json
{
  "campaign_id": "550e8400-e29b-41d4-a716-446655440000",
  "match_threshold": 0.5,
  "match_count": 10
}
```

**Response:**
Same structure as the detailed similarity search endpoint.

### Get Campaign Matches (GET Method)

**Endpoint:** `GET /api/v1/ai/campaign/{campaign_id}/matches`

Retrieves AI-powered influencer matches for an existing campaign. This is a convenience GET method alternative to the POST campaign-similarity endpoint.

**Path Parameters:**
- `campaign_id`: The ID of the campaign to use for matching

**Query Parameters:**
- `match_threshold`: Minimum similarity score (0-1) to include in results (default: 0.5)
- `match_count`: Maximum number of results to return (default: 10)

**Response:**
Same structure as the detailed similarity search endpoint.

### Generate Creator Embedding

**Endpoint:** `POST /api/v1/ai/creator/{creator_id}/generate-embedding`

Generates and stores an embedding vector for a creator's profile. This is necessary for the creator to appear in similarity search results.

**Path Parameters:**
- `creator_id`: The ID of the creator

**Response:**
```json
{
  "status": "success",
  "message": "Creator embedding generated successfully"
}
```

## Data Models

### Creator

```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "platform": "instagram|youtube|tiktok|twitter",
  "followers_count": "string",
  "followers_count_numeric": "integer",
  "engagement_rate": "number",
  "niche": "fitness|technology|beauty|food|travel|fashion",
  "language": "string",
  "country": "string",
  "about": "string",
  "channel_name": "string",
  "avg_views": "integer",
  "collaboration_rate": "number",
  "rating": "number",
  "profile_image": "string",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### Campaign

```json
{
  "id": "string",
  "product_name": "string",
  "brand_name": "string",
  "product_description": "string",
  "target_audience": "string",
  "key_use_cases": "string",
  "campaign_goal": "string",
  "product_niche": "string",
  "total_budget": "number",
  "status": "active|draft|completed|paused",
  "influencer_count": "integer",
  "campaign_code": "string",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### Contract

```json
{
  "id": "string",
  "campaign_id": "string",
  "creator_id": "string",
  "terms": "object",
  "deliverables": "object",
  "payment_amount": "number",
  "payment_schedule": "array",
  "status": "draft|sent|signed|completed",
  "signed_at": "string (date-time)",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### Payment

```json
{
  "id": "string",
  "contract_id": "string",
  "amount": "number",
  "status": "pending|processing|completed|failed",
  "payment_method": "string",
  "transaction_id": "string",
  "due_date": "string (date-time)",
  "paid_at": "string (date-time)",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### OutreachLog

```json
{
  "id": "string",
  "campaign_id": "string",
  "creator_id": "string",
  "channel": "call|email|message",
  "message_type": "outreach|follow_up|reply",
  "status": "initiated|in-progress|completed|failed|no_answer",
  "conversation_id": "string",
  "twilio_call_sid": "string",
  "call_duration_seconds": "integer",
  "call_successful": "success|failure|unknown",
  "transcript_summary": "string",
  "full_transcript": "array",
  "interest_assessment_result": "string",
  "interest_assessment_rationale": "string",
  "communication_quality_result": "string",
  "communication_quality_rationale": "string",
  "interest_level": "very_interested|interested|neutral|not_interested",
  "collaboration_rate": "string",
  "preferred_content_types": "string",
  "timeline_availability": "string",
  "contact_preferences": "string",
  "audience_demographics": "string",
  "brand_restrictions": "string",
  "follow_up_actions": "string",
  "content": "object",
  "email_status": "string",
  "last_contact_date": "string (date-time)",
  "notes": "string",
  "sentiment": "positive|neutral_positive|neutral|neutral_negative|negative",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### MatchScore

```json
{
  "id": "string",
  "campaign_id": "string",
  "creator_id": "string",
  "match_score": "number",
  "niche_match": "number",
  "audience_match": "number",
  "engagement_score": "number",
  "budget_fit": "number",
  "created_at": "string (date-time)",
  "updated_at": "string (date-time)"
}
```

### DetailedMatchResult

```json
{
  "id": "string",
  "influencer_name": "string",
  "profile_image": "string",
  "platform": "string",
  "match_score": "string",
  "niche": "string",
  "followers": "string",
  "followers_count_numeric": "number",
  "engagement": "string",
  "collaboration_rate": "string",
  "detailed_scores": {
    "niche_match": "string",
    "audience_match": "string",
    "engagement_score": "string",
    "budget_fit": "string"
  }
}
```

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Validation Error`: Request validation failed
- `500 Internal Server Error`: Server-side error

Validation errors will include details about the specific validation issues:

```json
{
  "detail": [
    {
      "loc": ["path", "to", "field"],
      "msg": "error message",
      "type": "error type"
    }
  ]
}
``` 