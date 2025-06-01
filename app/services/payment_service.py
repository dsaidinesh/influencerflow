import logging
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
import uuid

from app.models.payment import Payment
from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentProcess
from app.services.supabase_service import SupabaseService

logger = logging.getLogger(__name__)


class PaymentService:
    """
    Service for managing payment-related operations
    """
    
    @staticmethod
    async def get_payments(
        skip: int = 0,
        limit: int = 100,
        contract_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all payments with optional filtering
        """
        try:
            return await SupabaseService.get_payments(
                skip=skip, 
                limit=limit,
                contract_id=contract_id,
                status=status
            )
        except Exception as e:
            logger.error(f"Error getting payments: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving payments")
    
    @staticmethod
    async def get_payment(payment_id: str) -> Dict[str, Any]:
        """
        Get a single payment by ID
        """
        try:
            payment = await SupabaseService.get_payment(payment_id)
            if not payment:
                raise HTTPException(status_code=404, detail=f"Payment with ID {payment_id} not found")
            return payment
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting payment {payment_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving payment {payment_id}")
    
    @staticmethod
    async def create_payment(payment_data: PaymentCreate) -> Dict[str, Any]:
        """
        Create a new payment
        """
        try:
            # Set default values
            payment_dict = payment_data.model_dump()
            payment_dict["id"] = str(uuid.uuid4())
            payment_dict["status"] = "pending"
            payment_dict["created_at"] = datetime.utcnow().isoformat()
            payment_dict["updated_at"] = datetime.utcnow().isoformat()
            
            # Create payment in database
            payment = await SupabaseService.create_payment(PaymentCreate(**payment_dict))
            if not payment:
                raise HTTPException(status_code=500, detail="Failed to create payment")
            
            return payment
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise HTTPException(status_code=500, detail="Error creating payment")
    
    @staticmethod
    async def update_payment(payment_id: str, payment_data: PaymentUpdate) -> Dict[str, Any]:
        """
        Update an existing payment
        """
        try:
            # Check if payment exists
            existing_payment = await SupabaseService.get_payment(payment_id)
            if not existing_payment:
                raise HTTPException(status_code=404, detail=f"Payment with ID {payment_id} not found")
            
            # Update payment
            update_data = payment_data.model_dump(exclude_unset=True)
            update_data["updated_at"] = datetime.utcnow().isoformat()
            
            updated_payment = await SupabaseService.update_payment(payment_id, update_data)
            if not updated_payment:
                raise HTTPException(status_code=500, detail=f"Failed to update payment {payment_id}")
            
            return updated_payment
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating payment {payment_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error updating payment {payment_id}")
    
    @staticmethod
    async def process_payment(
        payment_id: str, 
        payment_method: str = "card"
    ) -> Dict[str, Any]:
        """
        Process a payment through payment provider
        This would typically integrate with Stripe or another payment processor
        """
        try:
            # Check if payment exists
            existing_payment = await SupabaseService.get_payment(payment_id)
            if not existing_payment:
                raise HTTPException(status_code=404, detail=f"Payment with ID {payment_id} not found")
            
            # Update payment status
            payment_details = {
                "payment_method": payment_method
            }
            
            processed_payment = await SupabaseService.process_payment(payment_id, payment_details)
            if not processed_payment:
                raise HTTPException(status_code=500, detail=f"Failed to process payment {payment_id}")
            
            # For now, simulate successful payment
            update_data = {
                "status": "completed",
                "payment_date": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            }
            
            final_payment = await SupabaseService.update_payment(payment_id, update_data)
            
            return final_payment
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing payment {payment_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing payment {payment_id}")
    
    @staticmethod
    async def get_payments_by_contract(contract_id: str) -> List[Dict[str, Any]]:
        """
        Get all payments for a specific contract
        """
        try:
            return await SupabaseService.get_payments(contract_id=contract_id, limit=1000)
        except Exception as e:
            logger.error(f"Error getting payments for contract {contract_id}: {e}")
            raise HTTPException(status_code=500, detail=f"Error retrieving payments for contract {contract_id}")
            
    @staticmethod
    async def get_payment_summary() -> Dict[str, Any]:
        """
        Get payment summary statistics
        """
        try:
            # Get all payments
            payments = await SupabaseService.get_payments(limit=1000)
            
            # Calculate summary statistics
            total_payments = len(payments)
            total_amount = sum(payment.get("amount", 0) for payment in payments)
            pending_payments = len([p for p in payments if p.get("status") == "pending"])
            completed_payments = len([p for p in payments if p.get("status") == "completed"])
            
            return {
                "total_payments": total_payments,
                "total_amount": total_amount,
                "pending_payments": pending_payments,
                "completed_payments": completed_payments,
                "average_payment": total_amount / total_payments if total_payments > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting payment summary: {e}")
            raise HTTPException(status_code=500, detail="Error retrieving payment summary")
    
    async def get_payment_dashboard(self, db: Session) -> Dict[str, Any]:
        """
        Get payment dashboard summary
        """
        try:
            # TODO: Replace with Supabase implementation
            # For now, return placeholder data
            
            # Calculate totals
            total_amount = 0
            total_count = 0
            
            # Calculate pending payments
            pending_amount = 0
            pending_count = 0
            
            # Calculate completed payments
            completed_amount = 0
            completed_count = 0
            
            # Get recent payments
            formatted_recent_payments = []
            
            return {
                "total_payments": {
                    "amount": total_amount,
                    "count": total_count
                },
                "pending_payments": {
                    "amount": pending_amount,
                    "count": pending_count
                },
                "completed_payments": {
                    "amount": completed_amount,
                    "count": completed_count
                },
                "recent_payments": formatted_recent_payments
            }
            
        except Exception as e:
            logger.error(f"Error generating payment dashboard: {str(e)}")
            return {
                "total_payments": {"amount": 0, "count": 0},
                "pending_payments": {"amount": 0, "count": 0},
                "completed_payments": {"amount": 0, "count": 0},
                "recent_payments": []
            } 