import streamlit as st
import subprocess
import os
import time

def run_script(user_input):
    """Runs the existing Python script with the user input and captures error messages."""
    script_path = "copy_of_teknitiai_final_adnan.py"
    
    # Use environment variable instead of modifying script
    env = os.environ.copy()
    env["USER_INPUT"] = user_input  # Pass user input as an environment variable

    # Run the script and capture both stdout and stderr for debugging
    process = subprocess.run(
        ["python", script_path],
        env=env,
        capture_output=True,
        text=True
    )

    # Print any error messages from the script
    if process.stderr:
        st.error(f"Error running script:\n{process.stderr}")
    
    return process.stdout

st.title("🏠 TeknitiAI Copilot")
st.markdown("### The AI Real Estate Agent")
st.write("Enter property details to generate a professional real estate report.")

# User input
user_input = st.text_area(
    "(e.g., 'I am interested in a property at 10 Hubert Road post code NN8 6DA. It is a 4 bedroom semi-detached house with 3 bathrooms.')"
)

generate_btn = st.button("Generate Report")

if generate_btn:
    if user_input.strip():
        st.write("Generating report... Please wait.")
        output = run_script(user_input)  # Run the backend script


        # Wait for file to be generated
        report_filename = "Formatted_Final_Real_Estate_Report_Reviewed.docx"
        
        max_wait_time = 15  # Maximum wait time in seconds
        elapsed_time = 0
        while not os.path.exists(report_filename) and elapsed_time < max_wait_time:
            time.sleep(1)
            elapsed_time += 1

        if os.path.exists(report_filename):
            with open(report_filename, "rb") as file:
                st.success("Report generated successfully!")
                st.download_button(
                    label="Download Report",
                    data=file,
                    file_name="Real_Estate_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
        else:
            st.error("Failed to generate the report file. Please check the backend script execution.")
    else:
        st.error("Please enter property details before generating the report.")
