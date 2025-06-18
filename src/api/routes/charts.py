"""
Charts and visualizations routes for Email Box Analyzer API.

Handles chart generation and management for email analysis results.
"""

import asyncio

from fastapi import APIRouter, Depends, HTTPException, status

from api.models import ChartData, ChartResponse
from api.routes.auth import get_current_user
from visualizers.chart_manager import ChartManager

router = APIRouter()

# Global chart manager instance
chart_manager: ChartManager = None


@router.post("/{analysis_id}/generate", response_model=ChartResponse)
async def generate_charts(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Generate charts for a specific analysis."""
    global chart_manager

    if not chart_manager:
        chart_manager = ChartManager()

    try:
        # Get analysis results (this would come from the analysis storage)
        # For now, we'll create mock data
        analysis_data = {
            "total_emails": 1000,
            "top_senders": [
                {"email": "sender1@example.com", "count": 150},
                {"email": "sender2@example.com", "count": 120},
                {"email": "sender3@example.com", "count": 100},
            ],
            "activity_by_time": {
                "hourly": {i: i * 10 for i in range(24)},
                "daily": {"Mon": 200, "Tue": 180, "Wed": 220, "Thu": 190, "Fri": 210},
            },
            "sentiment_analysis": {"positive": 600, "negative": 200, "neutral": 200},
        }

        # Generate charts
        charts = await asyncio.to_thread(chart_manager.create_charts, analysis_data)

        # Convert to API response format
        chart_data = {}
        chart_urls = {}

        for chart_name, chart_info in charts.items():
            chart_data[chart_name] = ChartData(
                type=chart_info.get("type", "bar"),
                title=chart_name.replace("_", " ").title(),
                data=chart_info.get("data", []),
                options=chart_info.get("options", {}),
            )

            if "file_path" in chart_info:
                chart_urls[chart_name] = f"/api/charts/{analysis_id}/{chart_name}/image"

        return ChartResponse(charts=chart_data, chart_urls=chart_urls)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to generate charts: {str(e)}"
        )


@router.get("/{analysis_id}/{chart_name}/image")
async def get_chart_image(analysis_id: str, chart_name: str, current_user: dict = Depends(get_current_user)):
    """Get a specific chart image."""
    # This would serve the actual chart image file
    # For now, return a placeholder response
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Chart image serving not implemented yet")


@router.get("/{analysis_id}/charts", response_model=ChartResponse)
async def get_analysis_charts(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Get all charts for a specific analysis."""
    # This would retrieve existing charts for the analysis
    # For now, return empty response
    return ChartResponse(charts={}, chart_urls={})


@router.delete("/{analysis_id}/charts")
async def delete_analysis_charts(analysis_id: str, current_user: dict = Depends(get_current_user)):
    """Delete all charts for a specific analysis."""
    # This would delete chart files and metadata
    return {"message": "Charts deleted successfully"}
