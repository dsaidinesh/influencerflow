# ElevenLabs Conversational AI Integration

This document provides instructions for integrating ElevenLabs Conversational AI with your InfluencerFlow platform, enabling automated outbound calling to influencers via Twilio.

## Setup Instructions

### 1. Update Environment Variables

Add the following variables to your `.env` file:

```
# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_AGENT_ID=your_agent_id_here
ELEVENLABS_PHONE_NUMBER_ID=your_phone_number_id_here
```

### 2. Run Database Migration

The integration requires new fields in the `outreach_logs` table. Run the migration script:

#### On Windows (PowerShell):

```powershell
.\scripts\run_elevenlabs_migration.ps1
```

#### On Unix/macOS (Bash):

```bash
bash scripts/run_elevenlabs_migration.sh
```

### 3. Verify the Integration

Run the test script to verify your ElevenLabs configuration:

```
python scripts/test_elevenlabs_integration.py
```

## Usage

### Initiating Outbound Calls

To initiate an outbound call to an influencer:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/outreach/call/initiate",
    json={
        "campaign_id": "your_campaign_id",
        "influencer_id": "influencer_id",
        "phone_number": "+11234567890"  # Influencer's phone number
    }
)

# The response contains the conversation ID and outreach log ID
print(response.json())
```

### Retrieving Call Analysis

To get the analysis of a completed call:

```python
import requests

response = requests.get(
    f"http://localhost:8000/api/v1/outreach/call/{conversation_id}/analysis"
)

# The response contains the full analysis including transcript and extracted data
analysis = response.json()
print(f"Call status: {analysis['status']}")
print(f"Summary: {analysis['summary']}")
print(f"Collaboration rate: {analysis['extracted_data']['collaboration_rate']}")
```

### Syncing Recent Conversations

To sync recent conversations and update outreach logs:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/outreach/sync-conversations",
    json={
        "limit": 50  # Optional: number of recent conversations to sync
    }
)

print(f"Synced {response.json()['updated_conversations']} conversations")
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/outreach/call/initiate` | POST | Initiate outbound call to influencer |
| `/api/v1/outreach/call/{conversation_id}/analysis` | GET | Get detailed call analysis |
| `/api/v1/outreach/sync-conversations` | POST | Sync recent conversations |

## Testing with Sample Data

You can use our sample campaign and creator data to test the integration:

```python
# Example: Initiate call to a sample creator for a campaign
import requests

response = requests.post(
    "http://localhost:8000/api/v1/outreach/call/initiate",
    json={
        "campaign_id": "sample_campaign_id",  # From your test data
        "influencer_id": "sample_creator_id",  # From your test data
        "phone_number": "+11234567890"  # Test phone number
    }
)

print(response.json())
```

## Troubleshooting

If you encounter issues:

1. Verify your ElevenLabs API key, agent ID, and phone number ID are correct
2. Check that the database migration completed successfully
3. Ensure your Supabase instance is accessible
4. Review the application logs for detailed error messages 