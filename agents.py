from crewai import Agent, LLM

llm = LLM(
    model="ollama/qwen",
    base_url="http://localhost:11434",
    temperature=0.2,
)

resume_agent = Agent(
    role="Professional Resume Writer",
    goal="Create ATS optimized resume",
    backstory="""
    You are an expert HR professional with years of
    experience creating ATS friendly resumes.
    """,
    llm=llm,
    verbose=True,
)

job_agent = Agent(
    role="Job Description Analyst",
    goal="Understand job requirements",
    backstory="""
    You are an expert recruiter.
    Extract required skills, technologies,
    responsibilities and qualifications.
    """,
    llm=llm,
    verbose=True
)

skill_gap_agent = Agent(
    role="Skill Gap Expert",
    goal="Compare resume against job description",
    backstory="""
    Compare candidate skills with job requirements
    and suggest improvements.
    """,
    llm=llm,
    verbose=True
)

linkedin_job_agent = Agent(
    role="LinkedIn Job Hunter",
    goal="Extract relevant jobs from LinkedIn based on CV",
    backstory="""
    You are an expert job search specialist with deep knowledge of LinkedIn.
    You find highly relevant job opportunities that match the candidate's
    skills, experience, and career goals. You focus on 1-week job listings
    with strong alignment to the candidate's profile.
    """,
    llm=llm,
    verbose=True
)