#!/usr/bin/env python3
"""Scheduled Jobs Example - LangChain Tools"""

import time

from scrapegraph_py.logger import sgai_logger

from langchain_scrapegraph.tools import (
    CreateScheduledJobTool,
    DeleteScheduledJobTool,
    GetJobExecutionsTool,
    GetScheduledJobsTool,
    GetScheduledJobTool,
    PauseScheduledJobTool,
    ResumeScheduledJobTool,
    TriggerScheduledJobTool,
    UpdateScheduledJobTool,
)

sgai_logger.set_logging(level="INFO")


def main():
    print("🚀 ScrapeGraph AI Scheduled Jobs Example - LangChain Tools")
    print("=" * 60)

    # Initialize tools
    create_job_tool = CreateScheduledJobTool()
    get_jobs_tool = GetScheduledJobsTool()
    get_job_tool = GetScheduledJobTool()
    update_job_tool = UpdateScheduledJobTool()
    pause_job_tool = PauseScheduledJobTool()
    resume_job_tool = ResumeScheduledJobTool()
    trigger_job_tool = TriggerScheduledJobTool()
    get_executions_tool = GetJobExecutionsTool()
    delete_job_tool = DeleteScheduledJobTool()

    try:
        print("\n📅 Creating a scheduled SmartScraper job...")

        smartscraper_config = {
            "website_url": "https://example.com",
            "user_prompt": "Extract the main heading and description from the page",
        }

        job = create_job_tool.invoke(
            {
                "job_name": "Daily Example Scraping",
                "service_type": "smartscraper",
                "cron_expression": "0 9 * * *",
                "job_config": smartscraper_config,
                "is_active": True,
            }
        )

        job_id = job["id"]
        print(f"✅ Created job: {job['job_name']} (ID: {job_id})")
        print(f"   Next run: {job.get('next_run_at', 'Not scheduled')}")

        print("\n📅 Creating a scheduled SearchScraper job...")

        searchscraper_config = {
            "user_prompt": "Find the latest news about artificial intelligence",
            "num_results": 5,
        }

        search_job = create_job_tool.invoke(
            {
                "job_name": "Weekly AI News Search",
                "service_type": "searchscraper",
                "cron_expression": "0 10 * * 1",
                "job_config": searchscraper_config,
                "is_active": True,
            }
        )

        search_job_id = search_job["id"]
        print(f"✅ Created job: {search_job['job_name']} (ID: {search_job_id})")

        print("\n📋 Listing all scheduled jobs...")

        jobs_response = get_jobs_tool.invoke({"page": 1, "page_size": 10})
        jobs = jobs_response["jobs"]

        print(f"Found {jobs_response['total']} total jobs:")
        for job_item in jobs:
            status = "🟢 Active" if job_item["is_active"] else "🔴 Inactive"
            print(f"  - {job_item['job_name']} ({job_item['service_type']}) - {status}")
            print(f"    Schedule: {job_item['cron_expression']}")
            if job_item.get("next_run_at"):
                print(f"    Next run: {job_item['next_run_at']}")

        print(f"\n🔍 Getting details for job {job_id}...")

        job_details = get_job_tool.invoke({"job_id": job_id})
        print(f"Job Name: {job_details['job_name']}")
        print(f"Service Type: {job_details['service_type']}")
        print(f"Created: {job_details['created_at']}")
        print(f"Active: {job_details['is_active']}")

        print("\n📝 Updating job schedule...")

        updated_job = update_job_tool.invoke(
            {
                "job_id": job_id,
                "cron_expression": "0 8 * * *",
                "job_name": "Daily Example Scraping (Updated)",
            }
        )

        print(f"✅ Updated job: {updated_job['job_name']}")
        print(f"   New schedule: {updated_job['cron_expression']}")

        print(f"\n⏸️ Pausing job {job_id}...")

        pause_result = pause_job_tool.invoke({"job_id": job_id})
        print(f"✅ {pause_result['message']}")
        print(f"   Job is now: {'Active' if pause_result['is_active'] else 'Paused'}")

        print(f"\n▶️ Resuming job {job_id}...")

        resume_result = resume_job_tool.invoke({"job_id": job_id})
        print(f"✅ {resume_result['message']}")
        print(f"   Job is now: {'Active' if resume_result['is_active'] else 'Paused'}")
        if resume_result.get("next_run_at"):
            print(f"   Next run: {resume_result['next_run_at']}")

        print(f"\n🚀 Manually triggering job {job_id}...")

        trigger_result = trigger_job_tool.invoke({"job_id": job_id})
        print(f"✅ {trigger_result['message']}")
        print(f"   Execution ID: {trigger_result['execution_id']}")
        print(f"   Triggered at: {trigger_result['triggered_at']}")

        # Wait a moment for the execution to potentially start
        time.sleep(2)

        print(f"\n📊 Getting execution history for job {job_id}...")

        executions_response = get_executions_tool.invoke(
            {"job_id": job_id, "page": 1, "page_size": 5}
        )

        executions = executions_response["executions"]
        print(f"Found {executions_response['total']} total executions:")

        for execution in executions:
            status_emoji = {
                "completed": "✅",
                "failed": "❌",
                "running": "🔄",
                "pending": "⏳",
            }.get(execution["status"], "❓")

            print(f"  {status_emoji} {execution['status'].upper()}")
            print(f"     Started: {execution['started_at']}")
            if execution.get("completed_at"):
                print(f"     Completed: {execution['completed_at']}")
            if execution.get("credits_used"):
                print(f"     Credits used: {execution['credits_used']}")

        print("\n🔧 Filtering jobs by service type (smartscraper)...")

        filtered_jobs = get_jobs_tool.invoke(
            {"service_type": "smartscraper", "is_active": True}
        )

        print(f"Found {filtered_jobs['total']} active SmartScraper jobs:")
        for job_item in filtered_jobs["jobs"]:
            print(
                f"  - {job_item['job_name']} (Schedule: {job_item['cron_expression']})"
            )

        print("\n🗑️ Cleaning up - deleting created jobs...")

        delete_result1 = delete_job_tool.invoke({"job_id": job_id})
        print(f"✅ {delete_result1['message']} (Job 1)")

        delete_result2 = delete_job_tool.invoke({"job_id": search_job_id})
        print(f"✅ {delete_result2['message']} (Job 2)")

        print("\n🎉 Scheduled jobs example completed successfully!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
