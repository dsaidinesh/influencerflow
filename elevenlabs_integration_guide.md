# ElevenLabs Conversational AI Integration Guide

This guide explains how to use the ElevenLabs Conversational AI integration with the InfluencerFlow platform to automate outreach calls to creators.

## Overview

The ElevenLabs Conversational AI integration allows you to:

1. Initiate automated, personalized outbound calls to creators using natural language AI
2. Store and analyze call transcripts and outcomes
3. Extract key data points such as interest level and collaboration rates
4. Get detailed analysis of conversations to improve outreach strategy

## Prerequisites

Before using the integration, ensure that:

1. Your `.env` file contains the required ElevenLabs configuration:
   ```
   ELEVENLABS_API_KEY=your_api_key
   ELEVENLABS_AGENT_ID=your_agent_id
   ELEVENLABS_PHONE_NUMBER_ID=your_phone_number_id
   ```

2. Your Supabase database has been updated with the required columns. You can run the verification script to check:
   ```bash
   python scripts/apply_elevenlabs_migration.py
   ```

## Usage

### Initiating a Call to a Creator

To initiate an outbound call to a creator:

1. Navigate to the Campaign Manager
2. Select a campaign and creator
3. Click "Initiate Call" button, or
4. Use the API endpoint directly:

```http
POST /api/v1/outreach/call/initiate
Content-Type: application/json

{
  "campaign_id": "campaign-uuid",
  "creator_id": "creator-uuid",
  "phone_number": "+1234567890"
}
```

### Retrieving Call Analysis

After a call is completed, you can retrieve the detailed analysis:

1. Navigate to the Outreach Management dashboard
2. Select the call from the list, or
3. Use the API endpoint:

```http
GET /api/v1/outreach/call/{conversation_id}/analysis
```

The analysis includes:
- Call transcript
- Success assessment
- Interest level evaluation
- Collaboration rate extraction
- Communication quality assessment
- Follow-up recommendations

### Syncing ElevenLabs Conversations

To sync multiple recent conversations from ElevenLabs to your InfluencerFlow database:

```http
POST /api/v1/outreach/sync-conversations
Content-Type: application/json

{
  "limit": 50
}
```

## Workflow Integration

The ElevenLabs integration fits into your campaign workflow as follows:

1. **Campaign Creation**: Define your campaign parameters
2. **Creator Selection**: Use AI matching to find suitable creators
3. **Automated Outreach**: Initiate AI-powered calls to creators
4. **Analysis & Follow-up**: Review call analysis and take follow-up actions
5. **Contract & Payment**: Convert interested creators to signed contracts

## Troubleshooting

If you encounter issues with the integration:

1. Run the verification script to check your configuration:
   ```bash
   python scripts/test_elevenlabs_integration.py
   ```

2. Check that your Supabase database has all required columns:
   ```bash
   python scripts/apply_elevenlabs_migration.py
   ```

3. Ensure all environment variables are set correctly in your `.env` file

4. Verify API connectivity to ElevenLabs services

## Limitations

- Phone calls require a valid phone number for the creator
- The system works best with English-speaking creators
- Call durations are typically limited to 10 minutes
- Currently supports Twilio for phone call handling 