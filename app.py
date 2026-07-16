import streamlit as st
from pathlib import Path
from crew import resume_crew
from agents import resume_agent, job_agent, skill_gap_agent, linkedin_job_agent
from tasks import (
    resume_task, job_analysis_task, skill_gap_task, 
    improvement_task, linkedin_jobs_task
)


def read_file(path):
    """Read file content"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def save_file(path, content):
    """Save content to file"""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def main():
    st.set_page_config(page_title="AI Resume Builder", layout="wide")
    
    st.title("🤖 AI Resume Builder")
    st.markdown("---")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page", 
        ["Home", "Input Files", "Tasks", "Generate Resume", "View Results"]
    )
    
    base_dir = Path(__file__).resolve().parent
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"
    
    input_dir.mkdir(exist_ok=True)
    output_dir.mkdir(exist_ok=True)
    
    if page == "Home":
        st.header("Welcome to AI Resume Builder")
        st.write("""
        This application uses AI agents to help you:
        - 📝 Create an ATS-optimized resume
        - 📊 Analyze job descriptions
        - 🎯 Identify skill gaps
        - 📈 Generate improvement plans
        - 💼 Find relevant LinkedIn jobs
        """)
        
    elif page == "Input Files":
        st.header("📂 Input Files")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Student Profile")
            profile_path = input_dir / "student_profile.txt"
            profile_content = read_file(profile_path)
            new_profile = st.text_area(
                "Enter your student profile:",
                value=profile_content,
                height=300,
                key="profile"
            )
            if st.button("Save Profile"):
                save_file(profile_path, new_profile)
                st.success("✅ Profile saved!")
        
        with col2:
            st.subheader("Job Description")
            job_path = input_dir / "job_description.txt"
            job_content = read_file(job_path)
            new_job = st.text_area(
                "Enter the job description:",
                value=job_content,
                height=300,
                key="job"
            )
            if st.button("Save Job Description"):
                save_file(job_path, new_job)
                st.success("✅ Job description saved!")
    
    elif page == "Tasks":
        st.header("⚙️ Run Individual Tasks")
        st.markdown("Execute individual AI tasks to process specific aspects of your resume and job matching.")
        
        profile_path = input_dir / "student_profile.txt"
        job_path = input_dir / "job_description.txt"
        
        profile = read_file(profile_path)
        job = read_file(job_path)
        
        if not profile or not job:
            st.error("❌ Please fill in both the student profile and job description in the 'Input Files' page first!")
        else:
            st.markdown("---")
            
            task_options = {
                "📝 Resume Generation": ("resume", resume_task, resume_agent, "Create ATS-optimized resume"),
                "📊 Job Analysis": ("job_analysis", job_analysis_task, job_agent, "Analyze job description for requirements"),
                "🎯 Skill Gap Analysis": ("skill_gap", skill_gap_task, skill_gap_agent, "Compare skills and generate ATS score"),
                "📈 Improvement Plan": ("improvement", improvement_task, skill_gap_agent, "Generate roadmap for improvement"),
                "💼 LinkedIn Jobs": ("linkedin", linkedin_jobs_task, linkedin_job_agent, "Extract relevant jobs from LinkedIn")
            }
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_task_name = st.selectbox(
                    "Select a task to run:",
                    list(task_options.keys()),
                    help="Choose which task you want to execute"
                )
            
            with col2:
                st.write("") 
                st.write("")
                run_task_btn = st.button("▶️ Run Task", use_container_width=True)
            
            selected_task = task_options[selected_task_name]
            task_key, task_obj, agent_obj, description = selected_task
            
            st.info(f"📌 {description}")
            
            if run_task_btn:
                st.markdown("---")
                st.info("⏳ Running task... This may take a moment.")
                
                # Prepare inputs
                inputs = {
                    "profile": profile,
                    "job_description": job
                }
                
                # Set agent for task
                task_obj.agent = agent_obj
                
                with st.spinner(f"Executing {selected_task_name}..."):
                    try:
                        # Run the single task
                        from crewai import Crew
                        single_task_crew = Crew(
                            agents=[agent_obj],
                            tasks=[task_obj],
                            verbose=True
                        )
                        result = single_task_crew.kickoff(inputs=inputs)
                        
                        st.success("✅ Task completed successfully!")
                        st.markdown("---")
                        st.markdown("### 📋 Result:")
                        st.markdown(result)
                        
                        # Show download option if output file is specified
                        if task_obj.output_file:
                            output_path = Path(task_obj.output_file)
                            if output_path.exists():
                                with open(output_path, "r", encoding="utf-8") as f:
                                    output_content = f.read()
                                st.download_button(
                                    label=f"📥 Download {output_path.name}",
                                    data=output_content,
                                    file_name=output_path.name,
                                    mime="text/markdown"
                                )
                    except Exception as e:
                        st.error(f"❌ Error running task: {str(e)}")
                        st.write(f"Details: {e}")
    
    elif page == "Generate Resume":
        st.header("⚙️ Generate Resume & Analysis")
        
        profile_path = input_dir / "student_profile.txt"
        job_path = input_dir / "job_description.txt"
        
        profile = read_file(profile_path)
        job = read_file(job_path)
        
        if not profile or not job:
            st.error("❌ Please fill in both the student profile and job description first!")
        else:
            if st.button("🚀 Generate All", key="generate_all"):
                st.info("⏳ Processing... This may take a minute.")
                
                inputs = {
                    "profile": profile,
                    "job_description": job
                }
                
                with st.spinner("Running AI agents..."):
                    try:
                        result = resume_crew.kickoff(inputs=inputs)
                        st.success("✅ Generation complete!")
                        st.markdown(result)
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    elif page == "View Results":
        st.header("📋 View Results")
        
        results = {
            "Resume": output_dir / "resume.md",
            "ATS Report": output_dir / "ats_report.md",
            "Improvement Plan": output_dir / "improvement_plan.md",
            "LinkedIn Jobs": output_dir / "linkedin_jobs.md"
        }
        
        selected_result = st.selectbox("Select a result to view:", list(results.keys()))
        
        result_path = results[selected_result]
        content = read_file(result_path)
        
        if content:
            st.markdown(content)
            if st.button("📥 Download"):
                st.download_button(
                    label=f"Download {selected_result}",
                    data=content,
                    file_name=result_path.name,
                    mime="text/markdown"
                )
        else:
            st.info(f"No {selected_result.lower()} generated yet. Please generate it first.")


if __name__ == "__main__":
    main()
