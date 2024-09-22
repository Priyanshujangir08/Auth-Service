from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.security import create_access_token, verify_password, get_password_hash
from schemas.user import User
from schemas.organization import Organization
from schemas.role import Role
from schemas.member import Member
from services.email import send_invite_email, send_password_update_email
from models.user_models import SignIn, SignUp, ResetPassword, InviteMail
from core.database import get_db
import logging
from sqlalchemy.exc import SQLAlchemyError

user_router = APIRouter()

@user_router.post("/signin")
def sign_in(sign_in: SignIn, db: Session = Depends(get_db)):
    """
    Sign in the user by verifying credentials and issuing access and refresh tokens.
    
    Args:
        sign_in (SignIn): The user's sign-in credentials (email and password).
        db (Session): The database session dependency.
    
    Returns:
        dict: A dictionary containing the access and refresh tokens.
    """

    try:
        user = db.query(User).filter(User.email == sign_in.email).first()
        if not user or not verify_password(sign_in.password, user.password):
            logging.warning(f"Invalid sign-in attempt for email: {sign_in.email}")
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_access_token(data={"sub": user.email}, expires_in=7*24*60*60)
        
        return {"access_token": access_token, "refresh_token": refresh_token}
    
    except Exception as error:
        logging.error(f"Error during sign-in: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.post("/signup")
def sign_up(sign_up: SignUp, db: Session = Depends(get_db)):
    """
    Sign up a new user and create an organization entry.

    Args:
        sign_up (SignUp): The user's sign-up credentials and organization details.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful signup and the user and organization IDs.

    Raises:
        HTTPException: If the user already exists or if there's a database error.
    """
    try:
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == sign_up.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        # Create the organization entry
        new_organization = Organization(
            name=sign_up.organization_name,
            status=0,  # default status
            personal=sign_up.personal,
            settings=sign_up.organization_settings or {},  # handle if settings are passed or not
            created_at=int(datetime.utcnow().timestamp()),
            updated_at=int(datetime.utcnow().timestamp())
        )
        db.add(new_organization)
        db.commit()  # Commit here for organization
        db.refresh(new_organization)

        # Create the user entry
        hashed_password = get_password_hash(sign_up.password)
        new_user = User(
            email=sign_up.email,
            password=hashed_password,
            profile=sign_up.profile or {},  # handle if profile data is passed
            status=0,  # default status
            settings=sign_up.user_settings or {},
            created_at=int(datetime.utcnow().timestamp()),
            updated_at=int(datetime.utcnow().timestamp())
        )
        db.add(new_user)
        db.commit()  # Commit here for user
        db.refresh(new_user)

        # Fetch the owner role for the member
        role = Role(name="Owner", org_id=new_organization.id)
        db.add(role)
        db.commit()  # Commit here for role

        # Create a member entry with the owner role
        new_member = Member(
            org_id=new_organization.id,
            user_id=new_user.id,
            role_id=role.id,
            status=0,  # default status
            settings={},
            created_at=int(datetime.utcnow().timestamp()),
            updated_at=int(datetime.utcnow().timestamp())
        )
        db.add(new_member)
        db.commit()  # Commit here for member

        send_invite_email(sign_up.email)

        return {"message": "User signed up successfully", "user_id": new_user.id, "org_id": new_organization.id}

    except SQLAlchemyError as error:
        db.rollback()  # Rollback in case of error
        logging.error(f"Database error during sign up: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during sign up: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.post("/reset-password")
def reset_password(reset: ResetPassword, db: Session = Depends(get_db)):
    """
    Reset the user's password.

    Args:
        reset (ResetPassword): The user's email and new password.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful password update.

    Raises:
        HTTPException: If the user is not found or if there's a database error.
    """
    try:
        user = db.query(User).filter(User.email == reset.email).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")
        
        # Update the user's password
        user.password = get_password_hash(reset.new_password)
        db.commit()

        # Send password update email
        send_password_update_email(user.email)

        return {"message": "Password updated successfully"}

    except SQLAlchemyError as error:
        db.rollback()  # Rollback in case of error
        logging.error(f"Database error during password reset: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during password reset: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.post("/invite")
def invite_member(payload: InviteMail, db: Session = Depends(get_db)):
    """
    Invite a new member to the organization.

    Args:
        payload (InviteMail): The email of the user to invite, organization ID, and role ID.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful invitation.

    Raises:
        HTTPException: If the user is not found or if there's a database error.
    """
    try:
        user = db.query(User).filter(User.email == payload.user_email).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        # Create the member entry
        member = Member(org_id=payload.org_id, user_id=user.id, role_id=payload.role_id, status=1)
        db.add(member)
        db.commit()

        # Send invitation email
        send_invite_email(payload.user_email)

        return {"message": "Member invited successfully"}

    except SQLAlchemyError as error:
        db.rollback()  # Rollback in case of error
        logging.error(f"Database error during inviting member: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during inviting member: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.delete("/delete/{member_id}")
def delete_member(member_id: int, db: Session = Depends(get_db)):
    """
    Delete a member by their ID.

    Args:
        member_id (int): The ID of the member to delete.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the member is not found or if there's a database error.
    """
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        db.delete(member)
        db.commit()
        
        return {"message": "Member deleted successfully"}

    except SQLAlchemyError as error:
        db.rollback()  # Rollback in case of error
        logging.error(f"Database error during member deletion: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during member deletion: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@user_router.put("/update-role/{member_id}")
def update_member_role(member_id: int, new_role_id: int, db: Session = Depends(get_db)):
    """
    Update the role of a member by their ID.

    Args:
        member_id (int): The ID of the member whose role is to be updated.
        new_role_id (int): The new role ID to assign to the member.
        db (Session): The database session dependency.

    Returns:
        dict: A message indicating successful role update.

    Raises:
        HTTPException: If the member is not found or if there's a database error.
    """
    try:
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        
        # Update the member's role
        member.role_id = new_role_id
        db.commit()
        
        return {"message": "Member role updated successfully"}

    except SQLAlchemyError as error:
        db.rollback()  # Rollback in case of error
        logging.error(f"Database error during role update for member {member_id}: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")
    except Exception as error:
        logging.error(f"Unexpected error during role update for member {member_id}: {str(error)}")
        raise HTTPException(status_code=500, detail="Internal server error")