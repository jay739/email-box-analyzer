"""
Email analysis routes for Email Box Analyzer API.

Handles email analysis operations including starting analysis, monitoring progress,
and retrieving results.
"""

# import asyncio
import uuid
from datetime import datetime
from typing import Any, Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from api.models import (AnalysisRequest, AnalysisResponse, AnalysisStatus,
                        EmailAnalysis)
from api.routes.auth import get_current_user

router = APIRouter()

# Global instances (in production, use proper session management)
# email_manager: EmailManager = None
# analyzer: EmailAnalyzer = None

# In-memory storage for analysis jobs (replace with database in production)
analysis_jobs: Dict[str, Dict[str, Any]] = {}


async def run_analysis_task(analysis_id: str, request: AnalysisRequest):
    """Background task to run email analysis."""
    # global email_manager
    # global analyzer

    try:
        # Update status to running
        analysis_jobs[analysis_id]["status"] = "running"
        analysis_jobs[analysis_id]["current_step"] = "Fetching emails..."
        analysis_jobs[analysis_id]["progress"] = 10

        # Fetch emails
        # emails = email_manager.fetch_emails(request.folder, limit=request.limit)
        # analysis_result = analyzer.analyze_emails(emails)

        analysis_jobs[analysis_id]["current_step"] = "Analyzing emails..."
        analysis_jobs[analysis_id]["progress"] = 30

        # Analyze emails
        # results = analyzer.analyze_emails(emails)

        analysis_jobs[analysis_id]["current_step"] = "Generating visualizations..."
        analysis_jobs[analysis_id]["progress"] = 80

        # Store results
        # analysis_jobs[analysis_id]["results"] = results
        analysis_jobs[analysis_id]["status"] = "completed"
        analysis_jobs[analysis_id]["progress"] = 100
        analysis_jobs[analysis_id]["current_step"] = "Analysis completed"
        analysis_jobs[analysis_id]["updated_at"] = datetime.utcnow()

    except Exception as e:
        analysis_jobs[analysis_id]["status"] = "failed"
        analysis_jobs[analysis_id]["error"] = str(e)
        analysis_jobs[analysis_id]["current_step"] = "Analysis failed"
        analysis_jobs[analysis_id]["updated_at"] = datetime.utcnow()


@router.post("/start", response_model=Dict[str, str])
async def start_analysis(
    request: AnalysisRequest, background_tasks: BackgroundTasks, current_user: dict = Depends(get_current_user)
):
    """Start a new email analysis."""
    # global email_manager
    # global analyzer

    # if not email_manager or not email_manager.is_connected():
    #     raise HTTPException(status_code=400, detail="Not connected to email server")

    # Generate analysis ID
    analysis_id = str(uuid.uuid4())

    # Initialize analysis job
    analysis_jobs[analysis_id] = {
        "id": analysis_id,
        "status": "pending",
        "progress": 0,
        "current_step": "Initializing analysis...",
        "error": None,
        "results": None,
        "request": request.dict(),
        "user_id": current_user["id"],
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    # Start background task
    background_tasks.add_task(run_analysis_task, analysis_id, request)

    return {"analysis_id": analysis_id}


@router.get("/{analysis_id}/status", response_model=AnalysisStatus)
async def get_analysis_status(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Get the status of an analysis job."""
    if analysis_id not in analysis_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    job = analysis_jobs[analysis_id]

    # Check if user owns this analysis
    if job["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return AnalysisStatus(
        analysis_id=job["id"],
        status=job["status"],
        progress=job["progress"],
        current_step=job["current_step"],
        error=job["error"],
        created_at=job["created_at"],
        updated_at=job["updated_at"],
    )


@router.get("/{analysis_id}/results", response_model=AnalysisResponse)
async def get_analysis_results(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Get the results of a completed analysis."""
    if analysis_id not in analysis_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    job = analysis_jobs[analysis_id]

    # Check if user owns this analysis
    if job["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if job["status"] != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis is not completed. Current status: {job['status']}",
        )

    results = job["results"]

    # Convert to EmailAnalysis model
    analysis = EmailAnalysis(
        analysis_id=job["id"],
        total_emails=results.get("total_emails", 0),
        date_range=results.get("date_range", {}),
        total_size_mb=results.get("total_size_mb", 0.0),
        top_senders=results.get("top_senders", []),
        activity_by_time=results.get("activity_by_time", {}),
        attachment_stats=results.get("attachment_stats", {}),
        sentiment_analysis=results.get("sentiment_analysis", {}),
        thread_analysis=results.get("thread_analysis", {}),
        domain_analysis=results.get("domain_analysis", {}),
        keyword_analysis=results.get("keyword_analysis", {}),
        response_time_analysis=results.get("response_time_analysis", {}),
        email_size_distribution=results.get("email_size_distribution", {}),
        language_analysis=results.get("language_analysis", {}),
        created_at=job["created_at"],
        processing_time_seconds=(job["updated_at"] - job["created_at"]).total_seconds(),
    )

    return AnalysisResponse(success=True, analysis=analysis, error=None)


@router.get("/last", response_model=AnalysisResponse)
async def get_last_analysis(current_user: dict = Depends(get_current_user)):
    """Get the most recent analysis for the current user."""
    user_analyses = [
        job for job in analysis_jobs.values() if job["user_id"] == current_user["id"] and job["status"] == "completed"
    ]

    if not user_analyses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No completed analyses found")

    # Get the most recent analysis
    latest_job = max(user_analyses, key=lambda x: x["created_at"])

    results = latest_job["results"]

    # Convert to EmailAnalysis model
    analysis = EmailAnalysis(
        analysis_id=latest_job["id"],
        total_emails=results.get("total_emails", 0),
        date_range=results.get("date_range", {}),
        total_size_mb=results.get("total_size_mb", 0.0),
        top_senders=results.get("top_senders", []),
        activity_by_time=results.get("activity_by_time", {}),
        attachment_stats=results.get("attachment_stats", {}),
        sentiment_analysis=results.get("sentiment_analysis", {}),
        thread_analysis=results.get("thread_analysis", {}),
        domain_analysis=results.get("domain_analysis", {}),
        keyword_analysis=results.get("keyword_analysis", {}),
        response_time_analysis=results.get("response_time_analysis", {}),
        email_size_distribution=results.get("email_size_distribution", {}),
        language_analysis=results.get("language_analysis", {}),
        created_at=latest_job["created_at"],
        processing_time_seconds=(latest_job["updated_at"] - latest_job["created_at"]).total_seconds(),
    )

    return AnalysisResponse(success=True, analysis=analysis, error=None)


@router.get("/", response_model=List[AnalysisStatus])
async def list_analyses(limit: int = 10, offset: int = 0, current_user: dict = Depends(get_current_user)):
    """List all analyses for the current user."""
    user_analyses = [job for job in analysis_jobs.values() if job["user_id"] == current_user["id"]]

    # Sort by creation date (newest first)
    user_analyses.sort(key=lambda x: x["created_at"], reverse=True)

    # Apply pagination
    paginated_analyses = user_analyses[offset : offset + limit]

    return [
        AnalysisStatus(
            analysis_id=job["id"],
            status=job["status"],
            progress=job["progress"],
            current_step=job["current_step"],
            error=job["error"],
            created_at=job["created_at"],
            updated_at=job["updated_at"],
        )
        for job in paginated_analyses
    ]


@router.delete("/{analysis_id}")
async def delete_analysis(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Delete an analysis job."""
    if analysis_id not in analysis_jobs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")

    job = analysis_jobs[analysis_id]

    # Check if user owns this analysis
    if job["user_id"] != current_user["id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # Remove the analysis
    del analysis_jobs[analysis_id]

    return {"message": "Analysis deleted successfully"}
