# InfluencerFlow Database Structure

This document outlines the database structure for the InfluencerFlow application, which is designed to manage influencer marketing campaigns. The database contains tables for creators (influencers), campaigns, contracts, outreach logs, and payments.

## Database Tables

### creators

Stores information about influencers/creators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each creator |
| name | text | NOT NULL | Creator's full name |
| email | text | UNIQUE, NOT NULL | Creator's email address |
| platform | enum | NOT NULL | Social media platform (instagram, youtube, tiktok, twitter) |
| followers_count | text | NOT NULL | Formatted follower count (e.g., "125K", "1.2M") |
| followers_count_numeric | integer | NOT NULL | Actual follower count as a number |
| engagement_rate | float | NOT NULL | Creator's engagement rate percentage |
| niche | enum | NOT NULL | Content category (fitness, technology, beauty, food, travel, fashion) |
| language | text | NOT NULL | Creator's primary language |
| country | text | NOT NULL | Creator's country |
| about | text | | Creator's bio or description |
| channel_name | text | | Name of the creator's channel or account |
| avg_views | integer | | Average number of views per post |
| collaboration_rate | float | | Creator's standard rate for collaborations |
| rating | float | | Rating based on past collaborations |
| profile_image | text | | URL to creator's profile image |
| embedding_vector | vector(1536) | | AI embedding vector for similarity matching |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

### campaigns

Stores information about marketing campaigns.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each campaign |
| product_name | text | NOT NULL | Name of the product being promoted |
| brand_name | text | NOT NULL | Name of the brand running the campaign |
| product_description | text | | Description of the product |
| target_audience | text | | Description of the target audience |
| key_use_cases | text | | Key use cases for the product |
| campaign_goal | text | | Goal or objective of the campaign |
| product_niche | text | | Product category or niche |
| total_budget | float | NOT NULL | Total budget allocated for the campaign |
| status | enum | NOT NULL, DEFAULT 'draft' | Campaign status (active, draft, completed, paused) |
| influencer_count | integer | NOT NULL, DEFAULT 0 | Number of influencers in the campaign |
| campaign_code | text | UNIQUE | Unique code for the campaign |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

### contracts

Manages agreements between campaigns and creators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each contract |
| campaign_id | uuid | FOREIGN KEY | Reference to the campaign |
| creator_id | uuid | FOREIGN KEY | Reference to the creator |
| terms | jsonb | | Contract terms and conditions |
| deliverables | jsonb | | Deliverables expected from the creator |
| payment_amount | float | NOT NULL | Amount to be paid to the creator |
| payment_schedule | jsonb | | Schedule of payments |
| status | enum | NOT NULL, DEFAULT 'draft' | Contract status (draft, sent, signed, completed) |
| signed_at | timestamp | | When the contract was signed |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

### outreach_logs

Tracks communication with creators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each log entry |
| campaign_id | uuid | FOREIGN KEY | Reference to the campaign |
| creator_id | uuid | FOREIGN KEY | Reference to the creator |
| channel | text | NOT NULL | Communication channel (call, email, message) |
| message_type | text | NOT NULL | Type of message (outreach, follow_up, reply) |
| status | text | NOT NULL | Status of the outreach |
| conversation_id | text | UNIQUE | ElevenLabs conversation ID |
| twilio_call_sid | text | | Twilio call SID |
| call_duration_seconds | integer | | Duration of the call in seconds |
| call_successful | text | | Success status of the call (success, failure, unknown) |
| transcript_summary | text | | Summary of the call transcript |
| full_transcript | jsonb | | Full transcript of the call |
| interest_assessment_result | text | | Assessment of creator's interest |
| interest_assessment_rationale | text | | Explanation of interest assessment |
| communication_quality_result | text | | Assessment of communication quality |
| communication_quality_rationale | text | | Explanation of communication quality |
| interest_level | text | | Creator's interest level (very_interested, interested, neutral, not_interested) |
| collaboration_rate | text | | Creator's collaboration rate from call |
| preferred_content_types | text | | Creator's preferred content types |
| timeline_availability | text | | Creator's timeline availability |
| contact_preferences | text | | Creator's contact preferences |
| audience_demographics | text | | Creator's audience demographics |
| brand_restrictions | text | | Creator's brand restrictions |
| follow_up_actions | text | | Recommended follow-up actions |
| content | jsonb | | Content of the outreach |
| email_status | text | | Status of the email |
| last_contact_date | timestamp | | Date of the last contact |
| notes | text | | Notes about the outreach |
| sentiment | text | | Creator's sentiment (positive, neutral, negative) |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

### payments

Tracks payments to creators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each payment |
| contract_id | uuid | FOREIGN KEY | Reference to the contract |
| amount | float | NOT NULL | Payment amount |
| status | enum | NOT NULL, DEFAULT 'pending' | Payment status (pending, processing, completed, failed) |
| payment_method | text | | Method of payment |
| transaction_id | text | | External transaction identifier |
| due_date | timestamp | | When the payment is due |
| paid_at | timestamp | | When the payment was completed |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

### match_scores

Stores AI-generated match scores between campaigns and creators.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | uuid | PRIMARY KEY | Unique identifier for each match score |
| campaign_id | uuid | FOREIGN KEY | Reference to the campaign |
| creator_id | uuid | FOREIGN KEY | Reference to the creator |
| match_score | float | NOT NULL | Overall match score percentage |
| niche_match | float | NOT NULL | Niche compatibility score |
| audience_match | float | NOT NULL | Audience compatibility score |
| engagement_score | float | NOT NULL | Engagement quality score |
| budget_fit | float | NOT NULL | Budget compatibility score |
| created_at | timestamp | | Timestamp when the record was created |
| updated_at | timestamp | | Timestamp when the record was last updated |

## Relationships

1. A **Campaign** can have multiple **Contracts** (one-to-many)
2. A **Creator** can have multiple **Contracts** (one-to-many)
3. A **Contract** can have multiple **Payments** (one-to-many)
4. A **Campaign** can have multiple **OutreachLogs** (one-to-many)
5. A **Creator** can have multiple **OutreachLogs** (one-to-many)
6. A **Campaign** can have multiple **MatchScores** (one-to-many)
7. A **Creator** can have multiple **MatchScores** (one-to-many)

## Enum Types

1. **platform_types**: instagram, youtube, tiktok, twitter
2. **niche_types**: fitness, technology, beauty, food, travel, fashion
3. **campaign_status**: active, draft, completed, paused
4. **contract_status**: draft, sent, signed, completed
5. **payment_status_types**: pending, processing, completed, failed

## Text-based Enum Values

These fields use text values instead of database enum types for flexibility:

1. **channel**: call, email, message
2. **message_type**: outreach, follow_up, reply
3. **status**: initiated, in-progress, completed, failed, no_answer
4. **call_successful**: success, failure, unknown
5. **interest_level**: very_interested, interested, neutral, not_interested
6. **sentiment**: positive, neutral_positive, neutral, neutral_negative, negative

## Migration to Supabase

When migrating this database structure to Supabase:

1. Create the enum types first
2. Create the tables in the order: creators, campaigns, contracts, outreach_logs, payments, match_scores (to respect foreign key constraints)
3. Set up RLS (Row Level Security) policies as needed
4. Create indexes for frequently queried columns
5. Set up any necessary triggers for `created_at` and `updated_at` timestamps
6. Enable pgvector extension for vector similarity search
7. Create a GIN index on the `embedding_vector` column for faster similarity searches 