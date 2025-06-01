from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Dict, Any, Optional

from app.schemas.contract import ContractCreate, ContractUpdate, ContractList, Contract
from app.services.contract_service import ContractService

router = APIRouter()


@router.post("/", response_model=Dict[str, Any])
async def create_contract(
    contract: ContractCreate
):
    """
    Create a new contract
    """
    return await ContractService.create_contract(contract)


@router.get("/", response_model=List[Dict[str, Any]])
async def get_contracts(
    campaign_id: Optional[str] = None,
    creator_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    List all contracts
    """
    return await ContractService.get_contracts(
        skip=offset, 
        limit=limit, 
        campaign_id=campaign_id, 
        creator_id=creator_id, 
        status=status
    )


@router.get("/{contract_id}", response_model=Dict[str, Any])
async def get_contract_by_id(
    contract_id: str = Path(..., description="The ID of the contract to get")
):
    """
    Get contract by ID
    """
    return await ContractService.get_contract(contract_id)


@router.put("/{contract_id}", response_model=Dict[str, Any])
async def update_contract(
    contract: ContractUpdate,
    contract_id: str = Path(..., description="The ID of the contract to update")
):
    """
    Update an existing contract
    """
    return await ContractService.update_contract(contract_id, contract)


@router.post("/{contract_id}/sign", response_model=Dict[str, Any])
async def sign_contract(
    contract_id: str = Path(..., description="The ID of the contract to sign")
):
    """
    Sign a contract
    """
    return await ContractService.sign_contract(contract_id)


@router.get("/{contract_id}/pdf", response_model=Dict[str, Any])
async def generate_contract_document(
    contract_id: str = Path(..., description="The ID of the contract to generate PDF for")
):
    """
    Generate contract document
    """
    return await ContractService.generate_contract_document(contract_id)


@router.get("/campaign/{campaign_id}", response_model=List[Dict[str, Any]])
async def get_contracts_by_campaign(
    campaign_id: str = Path(..., description="The ID of the campaign")
):
    """
    Get all contracts for a campaign
    """
    return await ContractService.get_contracts_by_campaign(campaign_id)


@router.get("/creator/{creator_id}", response_model=List[Dict[str, Any]])
async def get_contracts_by_creator(
    creator_id: str = Path(..., description="The ID of the creator")
):
    """
    Get all contracts for a creator
    """
    return await ContractService.get_contracts_by_creator(creator_id) 