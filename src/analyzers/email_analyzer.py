"""
Email Analyzer for Email Box Analyzer

Analyzes email data to extract insights, patterns, and statistics.
"""

import logging
import re
from collections import Counter, defaultdict
from typing import Any, Dict, List

from core.email_manager import EmailMessage


class EmailAnalyzer:
    """Analyzes email data to extract insights and patterns."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_emails(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """
        Analyze a list of email messages.

        Args:
            emails: List of email messages to analyze

        Returns:
            Dictionary containing analysis results
        """
        if not emails:
            return self._empty_results()

        self.logger.info(f"Analyzing {len(emails)} emails")

        results = {
            "total_emails": len(emails),
            "date_range": self._get_date_range(emails),
            "total_size_mb": self._calculate_total_size(emails),
            "top_senders": self._analyze_senders(emails),
            "activity_by_time": self._analyze_time_activity(emails),
            "activity_by_day": self._analyze_daily_activity(emails),
            "activity_by_hour": self._analyze_hourly_activity(emails),
            "subject_analysis": self._analyze_subjects(emails),
            "attachment_analysis": self._analyze_attachments(emails),
            "email_size_distribution": self._analyze_size_distribution(emails),
            "thread_analysis": self._analyze_threads(emails),
            "domain_analysis": self._analyze_domains(emails),
            "sentiment_analysis": self._analyze_sentiment(emails),
            "keyword_analysis": self._analyze_keywords(emails),
            "response_time_analysis": self._analyze_response_times(emails),
        }

        self.logger.info("Email analysis completed")
        return results

    def _empty_results(self) -> Dict[str, Any]:
        """Return empty analysis results."""
        return {
            "total_emails": 0,
            "date_range": "No emails",
            "total_size_mb": 0.0,
            "top_senders": [],
            "activity_by_time": {},
            "activity_by_day": {},
            "activity_by_hour": {},
            "subject_analysis": {},
            "attachment_analysis": {},
            "email_size_distribution": {},
            "thread_analysis": {},
            "domain_analysis": {},
            "sentiment_analysis": {},
            "keyword_analysis": {},
            "response_time_analysis": {},
        }

    def _get_date_range(self, emails: List[EmailMessage]) -> str:
        """Get the date range of emails."""
        if not emails:
            return "No emails"

        dates = [email.date for email in emails if email.date]
        if not dates:
            return "No valid dates"

        min_date = min(dates)
        max_date = max(dates)

        return f"{min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')}"

    def _calculate_total_size(self, emails: List[EmailMessage]) -> float:
        """Calculate total size of emails in MB."""
        total_bytes = sum(email.size for email in emails)
        return total_bytes / (1024 * 1024)  # Convert to MB

    def _analyze_senders(self, emails: List[EmailMessage]) -> List[tuple]:
        """Analyze email senders and their frequencies."""
        sender_counter = Counter()

        for email in emails:
            if email.sender:
                # Extract email address from sender string
                email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email.sender)
                if email_match:
                    sender_counter[email_match.group()] += 1
                else:
                    sender_counter[email.sender] += 1

        return sender_counter.most_common(20)

    def _analyze_time_activity(self, emails: List[EmailMessage]) -> Dict[str, int]:
        """Analyze email activity by time periods."""
        activity = defaultdict(int)

        for email in emails:
            if email.date:
                hour = email.date.hour
                if 6 <= hour < 12:
                    activity["Morning (6-12)"] += 1
                elif 12 <= hour < 17:
                    activity["Afternoon (12-17)"] += 1
                elif 17 <= hour < 22:
                    activity["Evening (17-22)"] += 1
                else:
                    activity["Night (22-6)"] += 1

        return dict(activity)

    def _analyze_daily_activity(self, emails: List[EmailMessage]) -> Dict[str, int]:
        """Analyze email activity by day of week."""
        daily_activity = defaultdict(int)
        day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

        for email in emails:
            if email.date:
                day_name = day_names[email.date.weekday()]
                daily_activity[day_name] += 1

        return dict(daily_activity)

    def _analyze_hourly_activity(self, emails: List[EmailMessage]) -> Dict[int, int]:
        """Analyze email activity by hour of day."""
        hourly_activity = defaultdict(int)

        for email in emails:
            if email.date:
                hourly_activity[email.date.hour] += 1

        return dict(hourly_activity)

    def _analyze_subjects(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email subjects."""
        subject_lengths = []
        subject_words = []
        common_words = Counter()

        for email in emails:
            if email.subject:
                # Subject length analysis
                subject_lengths.append(len(email.subject))

                # Word analysis
                words = re.findall(r"\b\w+\b", email.subject.lower())
                subject_words.extend(words)
                common_words.update(words)

        return {
            "avg_length": sum(subject_lengths) / len(subject_lengths) if subject_lengths else 0,
            "max_length": max(subject_lengths) if subject_lengths else 0,
            "min_length": min(subject_lengths) if subject_lengths else 0,
            "common_words": common_words.most_common(20),
            "total_words": len(subject_words),
        }

    def _analyze_attachments(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email attachments."""
        attachment_types = Counter()
        emails_with_attachments = 0
        total_attachments = 0

        for email in emails:
            if email.attachments:
                emails_with_attachments += 1
                total_attachments += len(email.attachments)

                for attachment in email.attachments:
                    # Extract file extension
                    if "." in attachment:
                        ext = attachment.split(".")[-1].lower()
                        attachment_types[ext] += 1
                    else:
                        attachment_types["no_extension"] += 1

        return {
            "emails_with_attachments": emails_with_attachments,
            "total_attachments": total_attachments,
            "attachment_types": dict(attachment_types.most_common(10)),
            "attachment_rate": (emails_with_attachments / len(emails)) * 100 if emails else 0,
        }

    def _analyze_size_distribution(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email size distribution."""
        sizes = [email.size for email in emails]

        if not sizes:
            return {}

        size_ranges = {
            "Small (< 1KB)": 0,
            "Medium (1KB - 10KB)": 0,
            "Large (10KB - 100KB)": 0,
            "Very Large (> 100KB)": 0,
        }

        for size in sizes:
            if size < 1024:
                size_ranges["Small (< 1KB)"] += 1
            elif size < 10 * 1024:
                size_ranges["Medium (1KB - 10KB)"] += 1
            elif size < 100 * 1024:
                size_ranges["Large (10KB - 100KB)"] += 1
            else:
                size_ranges["Very Large (> 100KB)"] += 1

        return {
            "size_ranges": size_ranges,
            "avg_size": sum(sizes) / len(sizes),
            "max_size": max(sizes),
            "min_size": min(sizes),
        }

    def _analyze_threads(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email threads and conversations."""
        # Simple thread analysis based on subject lines
        thread_groups = defaultdict(list)

        for email in emails:
            if email.subject:
                # Remove common prefixes like "Re:", "Fwd:", etc.
                clean_subject = re.sub(r"^(Re|Fwd|FW|RE|FW):\s*", "", email.subject, flags=re.IGNORECASE)
                thread_groups[clean_subject.lower()].append(email)

        thread_stats = []
        for subject, thread_emails in thread_groups.items():
            if len(thread_emails) > 1:
                thread_stats.append(
                    {"subject": subject, "count": len(thread_emails), "date_range": self._get_date_range(thread_emails)}
                )

        # Sort by thread size
        thread_stats.sort(key=lambda x: x["count"], reverse=True)

        return {
            "total_threads": len([t for t in thread_stats if t["count"] > 1]),
            "largest_thread": thread_stats[0] if thread_stats else None,
            "avg_thread_size": sum(t["count"] for t in thread_stats) / len(thread_stats) if thread_stats else 0,
            "top_threads": thread_stats[:10],
        }

    def _analyze_domains(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email domains."""
        domain_counter = Counter()

        for email in emails:
            if email.sender:
                # Extract domain from sender
                domain_match = re.search(r"@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", email.sender)
                if domain_match:
                    domain_counter[domain_match.group(1)] += 1

        return {
            "top_domains": domain_counter.most_common(20),
            "total_domains": len(domain_counter),
            "domain_diversity": len(domain_counter) / len(emails) if emails else 0,
        }

    def _analyze_sentiment(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email sentiment (basic implementation)."""
        # This is a basic sentiment analysis
        # In a real implementation, you might use NLTK, TextBlob, or other libraries

        positive_words = {
            "good",
            "great",
            "excellent",
            "amazing",
            "wonderful",
            "fantastic",
            "awesome",
            "perfect",
            "love",
            "like",
            "happy",
            "pleased",
            "satisfied",
            "thank",
            "thanks",
            "appreciate",
        }
        negative_words = {
            "bad",
            "terrible",
            "awful",
            "horrible",
            "disappointed",
            "angry",
            "frustrated",
            "hate",
            "dislike",
            "upset",
            "sad",
            "sorry",
            "apologize",
            "problem",
            "issue",
            "error",
        }

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for email in emails:
            text = f"{email.subject} {email.body}".lower()
            words = set(re.findall(r"\b\w+\b", text))

            positive_matches = len(words.intersection(positive_words))
            negative_matches = len(words.intersection(negative_words))

            if positive_matches > negative_matches:
                positive_count += 1
            elif negative_matches > positive_matches:
                negative_count += 1
            else:
                neutral_count += 1

        total = len(emails)
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count,
            "positive_percentage": (positive_count / total) * 100 if total > 0 else 0,
            "negative_percentage": (negative_count / total) * 100 if total > 0 else 0,
            "neutral_percentage": (neutral_count / total) * 100 if total > 0 else 0,
        }

    def _analyze_keywords(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze keywords in email content."""
        word_counter = Counter()
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
            "my",
            "your",
            "his",
            "her",
            "its",
            "our",
            "their",
        }

        for email in emails:
            text = f"{email.subject} {email.body}".lower()
            words = re.findall(r"\b[a-zA-Z]{3,}\b", text)  # Words with 3+ characters

            # Filter out stop words
            filtered_words = [word for word in words if word not in stop_words]
            word_counter.update(filtered_words)

        return {
            "top_keywords": word_counter.most_common(50),
            "total_unique_words": len(word_counter),
            "most_common_word": word_counter.most_common(1)[0] if word_counter else None,
        }

    def _analyze_response_times(self, emails: List[EmailMessage]) -> Dict[str, Any]:
        """Analyze email response times (basic implementation)."""
        # This is a simplified response time analysis
        # In a real implementation, you'd need to match emails in conversations

        response_times = []

        # Group emails by thread (simplified)
        thread_groups = defaultdict(list)
        for email in emails:
            if email.subject:
                clean_subject = re.sub(r"^(Re|Fwd|FW|RE|FW):\s*", "", email.subject, flags=re.IGNORECASE)
                thread_groups[clean_subject.lower()].append(email)

        # Calculate response times within threads
        for thread_emails in thread_groups.values():
            if len(thread_emails) > 1:
                # Sort by date
                sorted_emails = sorted(thread_emails, key=lambda x: x.date)

                for i in range(1, len(sorted_emails)):
                    time_diff = sorted_emails[i].date - sorted_emails[i - 1].date
                    response_times.append(time_diff.total_seconds() / 3600)  # Convert to hours

        if response_times:
            return {
                "avg_response_time_hours": sum(response_times) / len(response_times),
                "min_response_time_hours": min(response_times),
                "max_response_time_hours": max(response_times),
                "response_time_samples": len(response_times),
            }
        else:
            return {
                "avg_response_time_hours": 0,
                "min_response_time_hours": 0,
                "max_response_time_hours": 0,
                "response_time_samples": 0,
            }
