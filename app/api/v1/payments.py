from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional

from app.schemas.payment import PaymentCreate, PaymentUpdate, PaymentProcess
from app.services.payment_service import PaymentService

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_payment(
    payment: PaymentCreate
):
    """
    Create a new payment
    """
    return await PaymentService.create_payment(payment)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_payments(
    contract_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List all payments
    """
    return await PaymentService.get_payments(
        skip=offset, 
        limit=limit, 
        contract_id=contract_id, 
        status=status
    )


@router.get("/{payment_id}", response_model=Dict[str, Any])
async def get_payment(
    payment_id: str = Path(..., description="The ID of the payment to get")
):
    """
    Get payment by ID
    """
    return await PaymentService.get_payment(payment_id)


@router.put("/{payment_id}", response_model=Dict[str, Any])
async def update_payment(
    payment: PaymentUpdate,
    payment_id: str = Path(..., description="The ID of the payment to update")
):
    """
    Update an existing payment
    """
    return await PaymentService.update_payment(payment_id, payment)


@router.post("/{payment_id}/process", response_model=Dict[str, Any])
async def process_payment(
    payment_details: PaymentProcess,
    payment_id: str = Path(..., description="The ID of the payment to process")
):
    """
    Process a payment
    """
    return await PaymentService.process_payment(
        payment_id, 
        payment_details.payment_method
    )


@router.get("/contract/{contract_id}", response_model=List[Dict[str, Any]])
async def get_payments_by_contract(
    contract_id: str = Path(..., description="The ID of the contract")
):
    """
    Get all payments for a contract
    """
    return await PaymentService.get_payments_by_contract(contract_id)


@router.get("/summary", response_model=Dict[str, Any])
async def get_payment_summary():
    """
    Get payment summary statistics
    """
    return await PaymentService.get_payment_summary() 