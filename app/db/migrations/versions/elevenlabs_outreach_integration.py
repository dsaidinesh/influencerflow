"""elevenlabs_outreach_integration

Revision ID: 20240602001
Revises: 
Create Date: 2024-06-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20240602001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Update outreach_logs table to support ElevenLabs integration
    
    # Add new columns for ElevenLabs integration
    op.add_column('outreach_logs', sa.Column('channel', sa.String(), nullable=True, server_default='call'))
    op.add_column('outreach_logs', sa.Column('message_type', sa.String(), nullable=True, server_default='outreach'))
    op.add_column('outreach_logs', sa.Column('status', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('conversation_id', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('twilio_call_sid', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('call_duration_seconds', sa.Integer(), nullable=True))
    
    # Add columns for ElevenLabs analysis results
    op.add_column('outreach_logs', sa.Column('call_successful', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('transcript_summary', sa.Text(), nullable=True))
    op.add_column('outreach_logs', sa.Column('full_transcript', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Add columns for evaluation criteria results
    op.add_column('outreach_logs', sa.Column('interest_assessment_result', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('interest_assessment_rationale', sa.Text(), nullable=True))
    op.add_column('outreach_logs', sa.Column('communication_quality_result', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('communication_quality_rationale', sa.Text(), nullable=True))
    
    # Add columns for extracted data
    op.add_column('outreach_logs', sa.Column('interest_level', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('collaboration_rate', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('preferred_content_types', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('timeline_availability', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('contact_preferences', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('audience_demographics', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('brand_restrictions', sa.String(), nullable=True))
    op.add_column('outreach_logs', sa.Column('follow_up_actions', sa.Text(), nullable=True))
    
    # Add JSON content column for general outreach content
    op.add_column('outreach_logs', sa.Column('content', postgresql.JSON(astext_type=sa.Text()), nullable=True))
    
    # Create a unique index on conversation_id for lookups
    op.create_index(op.f('ix_outreach_logs_conversation_id'), 'outreach_logs', ['conversation_id'], unique=True)


def downgrade():
    # Drop all added columns
    op.drop_index(op.f('ix_outreach_logs_conversation_id'), table_name='outreach_logs')
    
    op.drop_column('outreach_logs', 'content')
    op.drop_column('outreach_logs', 'follow_up_actions')
    op.drop_column('outreach_logs', 'brand_restrictions')
    op.drop_column('outreach_logs', 'audience_demographics')
    op.drop_column('outreach_logs', 'contact_preferences')
    op.drop_column('outreach_logs', 'timeline_availability')
    op.drop_column('outreach_logs', 'preferred_content_types')
    op.drop_column('outreach_logs', 'collaboration_rate')
    op.drop_column('outreach_logs', 'interest_level')
    op.drop_column('outreach_logs', 'communication_quality_rationale')
    op.drop_column('outreach_logs', 'communication_quality_result')
    op.drop_column('outreach_logs', 'interest_assessment_rationale')
    op.drop_column('outreach_logs', 'interest_assessment_result')
    op.drop_column('outreach_logs', 'full_transcript')
    op.drop_column('outreach_logs', 'transcript_summary')
    op.drop_column('outreach_logs', 'call_successful')
    op.drop_column('outreach_logs', 'call_duration_seconds')
    op.drop_column('outreach_logs', 'twilio_call_sid')
    op.drop_column('outreach_logs', 'conversation_id')
    op.drop_column('outreach_logs', 'status')
    op.drop_column('outreach_logs', 'message_type')
    op.drop_column('outreach_logs', 'channel') 