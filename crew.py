from crewai import Crew

from agents import  resume_agent, job_agent, skill_gap_agent, linkedin_job_agent
from tasks import resume_task, job_analysis_task, skill_gap_task, improvement_task, linkedin_jobs_task

resume_task.agent = resume_agent
job_analysis_task.agent = job_agent
skill_gap_task.agent = skill_gap_agent
improvement_task.agent = skill_gap_agent
linkedin_jobs_task.agent = linkedin_job_agent

resume_crew = Crew(
    agents=[resume_agent, job_agent, skill_gap_agent, linkedin_job_agent],
    tasks=[resume_task, job_analysis_task, skill_gap_task, improvement_task, linkedin_jobs_task],
    verbose=True
)