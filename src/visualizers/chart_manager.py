"""
Chart Manager for Email Box Analyzer

Generates various charts and visualizations from email analysis data.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better-looking charts
plt.style.use("seaborn-v0_8")
sns.set_palette("husl")


class ChartManager:
    """Manages creation and saving of charts and visualizations."""

    def __init__(self, output_dir: Optional[str] = None):
        """
        Initialize the chart manager.

        Args:
            output_dir: Directory to save chart files. If None, uses default.
        """
        self.logger = logging.getLogger(__name__)
        self.output_dir = Path(output_dir) if output_dir else Path.home() / ".email_analyzer" / "charts"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def create_charts(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create all charts from analysis results.

        Args:
            analysis_results: Results from email analysis

        Returns:
            Dictionary containing chart information
        """
        charts = {}

        try:
            # Create various charts
            charts["activity_by_time"] = self._create_time_activity_chart(analysis_results)
            charts["daily_activity"] = self._create_daily_activity_chart(analysis_results)
            charts["hourly_activity"] = self._create_hourly_activity_chart(analysis_results)
            charts["top_senders"] = self._create_top_senders_chart(analysis_results)
            charts["email_size_distribution"] = self._create_size_distribution_chart(analysis_results)
            charts["attachment_analysis"] = self._create_attachment_chart(analysis_results)
            charts["sentiment_analysis"] = self._create_sentiment_chart(analysis_results)
            charts["domain_analysis"] = self._create_domain_chart(analysis_results)
            charts["keyword_cloud"] = self._create_keyword_chart(analysis_results)

            self.logger.info(f"Created {len(charts)} charts")

        except Exception as e:
            self.logger.error(f"Error creating charts: {e}")

        return charts

    def _create_time_activity_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing email activity by time of day."""
        activity_data = results.get("activity_by_time", {})

        if not activity_data:
            return {"type": "time_activity", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(10, 6))

        periods = list(activity_data.keys())
        counts = list(activity_data.values())

        bars = ax.bar(periods, counts, color=sns.color_palette("husl", len(periods)))

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{count}", ha="center", va="bottom")

        ax.set_title("Email Activity by Time of Day", fontsize=16, fontweight="bold")
        ax.set_xlabel("Time Period", fontsize=12)
        ax.set_ylabel("Number of Emails", fontsize=12)
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"time_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "time_activity", "data": activity_data, "file_path": str(file_path)}

    def _create_daily_activity_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing email activity by day of week."""
        daily_data = results.get("activity_by_day", {})

        if not daily_data:
            return {"type": "daily_activity", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(12, 6))

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        counts = [daily_data.get(day, 0) for day in days]

        bars = ax.bar(days, counts, color=sns.color_palette("husl", len(days)))

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{count}", ha="center", va="bottom")

        ax.set_title("Email Activity by Day of Week", fontsize=16, fontweight="bold")
        ax.set_xlabel("Day of Week", fontsize=12)
        ax.set_ylabel("Number of Emails", fontsize=12)
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"daily_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "daily_activity", "data": daily_data, "file_path": str(file_path)}

    def _create_hourly_activity_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing email activity by hour."""
        hourly_data = results.get("activity_by_hour", {})

        if not hourly_data:
            return {"type": "hourly_activity", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(14, 6))

        hours = list(range(24))
        counts = [hourly_data.get(hour, 0) for hour in hours]

        ax.plot(hours, counts, marker="o", linewidth=2, markersize=6)
        ax.fill_between(hours, counts, alpha=0.3)

        ax.set_title("Email Activity by Hour of Day", fontsize=16, fontweight="bold")
        ax.set_xlabel("Hour of Day", fontsize=12)
        ax.set_ylabel("Number of Emails", fontsize=12)
        ax.set_xticks(hours)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"hourly_activity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "hourly_activity", "data": hourly_data, "file_path": str(file_path)}

    def _create_top_senders_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing top email senders."""
        top_senders = results.get("top_senders", [])

        if not top_senders:
            return {"type": "top_senders", "data": [], "file_path": None}

        # Take top 10 senders
        top_10 = top_senders[:10]

        fig, ax = plt.subplots(figsize=(12, 8))

        senders = [sender for sender, count in top_10]
        counts = [count for sender, count in top_10]

        bars = ax.barh(senders, counts, color=sns.color_palette("husl", len(senders)))

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height() / 2.0, f"{count}", ha="left", va="center")

        ax.set_title("Top Email Senders", fontsize=16, fontweight="bold")
        ax.set_xlabel("Number of Emails", fontsize=12)
        ax.set_ylabel("Sender", fontsize=12)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"top_senders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "top_senders", "data": top_senders, "file_path": str(file_path)}

    def _create_size_distribution_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing email size distribution."""
        size_data = results.get("email_size_distribution", {})

        if not size_data or "size_ranges" not in size_data:
            return {"type": "size_distribution", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(10, 6))

        ranges = list(size_data["size_ranges"].keys())
        counts = list(size_data["size_ranges"].values())

        colors = sns.color_palette("husl", len(ranges))
        wedges, texts, autotexts = ax.pie(counts, labels=ranges, autopct="%1.1f%%", colors=colors, startangle=90)

        ax.set_title("Email Size Distribution", fontsize=16, fontweight="bold")

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"size_distribution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "size_distribution", "data": size_data, "file_path": str(file_path)}

    def _create_attachment_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing attachment analysis."""
        attachment_data = results.get("attachment_analysis", {})

        if not attachment_data:
            return {"type": "attachment_analysis", "data": [], "file_path": None}

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Pie chart for attachment rate
        labels = ["With Attachments", "Without Attachments"]
        sizes = [
            attachment_data.get("emails_with_attachments", 0),
            results.get("total_emails", 0) - attachment_data.get("emails_with_attachments", 0),
        ]

        ax1.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax1.set_title("Email Attachment Rate", fontsize=14, fontweight="bold")

        # Bar chart for attachment types
        types_data = attachment_data.get("attachment_types", {})
        if types_data:
            types = list(types_data.keys())[:10]  # Top 10 types
            counts = [types_data[type_name] for type_name in types]

            bars = ax2.bar(types, counts, color=sns.color_palette("husl", len(types)))
            ax2.set_title("Top Attachment Types", fontsize=14, fontweight="bold")
            ax2.set_xlabel("File Type", fontsize=12)
            ax2.set_ylabel("Count", fontsize=12)
            ax2.tick_params(axis="x", rotation=45)

            # Add value labels on bars
            for bar, count in zip(bars, counts):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{count}", ha="center", va="bottom")

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"attachment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "attachment_analysis", "data": attachment_data, "file_path": str(file_path)}

    def _create_sentiment_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing sentiment analysis."""
        sentiment_data = results.get("sentiment_analysis", {})

        if not sentiment_data:
            return {"type": "sentiment_analysis", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(10, 6))

        categories = ["Positive", "Negative", "Neutral"]
        counts = [
            sentiment_data.get("positive", 0),
            sentiment_data.get("negative", 0),
            sentiment_data.get("neutral", 0),
        ]

        colors = ["#2ecc71", "#e74c3c", "#95a5a6"]  # Green, Red, Gray
        bars = ax.bar(categories, counts, color=colors)

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.01, f"{count}", ha="center", va="bottom")

        ax.set_title("Email Sentiment Analysis", fontsize=16, fontweight="bold")
        ax.set_ylabel("Number of Emails", fontsize=12)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "sentiment_analysis", "data": sentiment_data, "file_path": str(file_path)}

    def _create_domain_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing domain analysis."""
        domain_data = results.get("domain_analysis", {})

        if not domain_data or "top_domains" not in domain_data:
            return {"type": "domain_analysis", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(12, 8))

        domains = [domain for domain, count in domain_data["top_domains"][:15]]
        counts = [count for domain, count in domain_data["top_domains"][:15]]

        bars = ax.barh(domains, counts, color=sns.color_palette("husl", len(domains)))

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height() / 2.0, f"{count}", ha="left", va="center")

        ax.set_title("Top Email Domains", fontsize=16, fontweight="bold")
        ax.set_xlabel("Number of Emails", fontsize=12)
        ax.set_ylabel("Domain", fontsize=12)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"domain_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "domain_analysis", "data": domain_data, "file_path": str(file_path)}

    def _create_keyword_chart(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Create chart showing keyword analysis."""
        keyword_data = results.get("keyword_analysis", {})

        if not keyword_data or "top_keywords" not in keyword_data:
            return {"type": "keyword_analysis", "data": [], "file_path": None}

        fig, ax = plt.subplots(figsize=(12, 8))

        keywords = [keyword for keyword, count in keyword_data["top_keywords"][:20]]
        counts = [count for keyword, count in keyword_data["top_keywords"][:20]]

        bars = ax.barh(keywords, counts, color=sns.color_palette("husl", len(keywords)))

        # Add value labels on bars
        for bar, count in zip(bars, counts):
            width = bar.get_width()
            ax.text(width + 0.01, bar.get_y() + bar.get_height() / 2.0, f"{count}", ha="left", va="center")

        ax.set_title("Most Common Keywords", fontsize=16, fontweight="bold")
        ax.set_xlabel("Frequency", fontsize=12)
        ax.set_ylabel("Keyword", fontsize=12)

        plt.tight_layout()

        # Save chart
        file_path = self.output_dir / f"keyword_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(file_path, dpi=300, bbox_inches="tight")
        plt.close()

        return {"type": "keyword_analysis", "data": keyword_data, "file_path": str(file_path)}

    def create_summary_report(self, analysis_results: Dict[str, Any], charts: Dict[str, Any]) -> str:
        """
        Create a summary report with charts and analysis.

        Args:
            analysis_results: Results from email analysis
            charts: Generated charts information

        Returns:
            HTML report content
        """
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Email Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .section { margin-bottom: 30px; }
                .chart { text-align: center; margin: 20px 0; }
                .chart img { max-width: 100%; height: auto; }
                .stats { display: flex; justify-content: space-around; flex-wrap: wrap; }
                .stat-box { background: #f5f5f5; padding: 15px; margin: 10px; border-radius: 5px; text-align: center; }
                .stat-value { font-size: 24px; font-weight: bold; color: #2c3e50; }
                .stat-label { font-size: 14px; color: #7f8c8d; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Email Analysis Report</h1>
                <p>Generated on {date}</p>
            </div>
        """

        # Add summary statistics
        html_content += """
            <div class="section">
                <h2>Summary Statistics</h2>
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-value">{total_emails}</div>
                        <div class="stat-label">Total Emails</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{total_size:.1f} MB</div>
                        <div class="stat-label">Total Size</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{date_range}</div>
                        <div class="stat-label">Date Range</div>
                    </div>
                </div>
            </div>
        """

        # Add charts
        for chart_name, chart_info in charts.items():
            if chart_info.get("file_path"):
                html_content += f"""
                    <div class="section">
                        <h2>{chart_name.replace('_', ' ').title()}</h2>
                        <div class="chart">
                            <img src="{chart_info['file_path']}" alt="{chart_name}">
                        </div>
                    </div>
                """

        html_content += """
        </body>
        </html>
        """

        # Save report
        report_path = self.output_dir / f"email_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return str(report_path)
