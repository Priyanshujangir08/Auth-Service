from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.organization import Organization
from schemas.role import Role
from schemas.member import Member
from core.database import get_db
import logging
from sqlalchemy.exc import SQLAlchemyError

stats_router = APIRouter()

@stats_router.get("/role-wise-users")
def role_wise_users(db: Session = Depends(get_db)):
    """
    Retrieve the count of users grouped by their roles.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of dictionaries containing role names and user counts.

    Raises:
        HTTPException: If there's a database error.
    """
    try:
        # Perform the query
        results = db.query(Role.name, func.count(Member.user_id)).join(Member).group_by(Role.name).all()
        
        # Convert the results to a list of dictionaries
        response = [{"role": role_name, "user_count": user_count} for role_name, user_count in results]
        
        return response

    except SQLAlchemyError as error:
        logging.error(f"Database error during role-wise user count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during role-wise user count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@stats_router.get("/org-wise-members")
def org_wise_members(db: Session = Depends(get_db)):
    """
    Retrieve the count of members grouped by their organizations.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of dictionaries containing organization names and member counts.

    Raises:
        HTTPException: If there's a database error.
    """
    try:
        # Perform the query
        result = db.query(Organization.name, func.count(Member.user_id)).join(Member).group_by(Organization.name).all()
        
        # Convert the results to a list of dictionaries
        response = [{"organization": organization, "member_count": member_count} for organization, member_count in result]
        
        return response

    except SQLAlchemyError as error:
        logging.error(f"Database error during organization-wise member count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during organization-wise member count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@stats_router.get("/org-role-wise-users")
def org_role_wise_users(db: Session = Depends(get_db)):
    """
    Retrieve the count of users grouped by their organizations and roles.

    Args:
        db (Session): The database session dependency.

    Returns:
        list: A list of dictionaries containing organization names, role names, and user counts.

    Raises:
        HTTPException: If there's a database error.
    """
    try:
        # Perform the query
        result = db.query(Organization.name, Role.name, func.count(Member.user_id))\
                   .select_from(Organization)\
                   .join(Member, Member.org_id == Organization.id)\
                   .join(Role, Role.id == Member.role_id)\
                   .group_by(Organization.name, Role.name)\
                   .all()

        # Convert the results to a list of dictionaries
        response = [
            {
                "organization": org_name,
                "role": role_name,
                "user_count": user_count
            } 
            for org_name, role_name, user_count in result
        ]
        
        return response

    except SQLAlchemyError as error:
        logging.error(f"Database error during organization-role-wise user count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during organization-role-wise user count retrieval: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")