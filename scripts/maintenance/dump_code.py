import os

def create_codebase_dump():
    files_to_dump = [
        "aergia_dashboard.py",
        "intelligence_router.py",
        "router/core.py",
        "router/registry.py",
        "router/policy.py",
        "router/executor.py",
        "router/schemas.py",
        "router/base_provider.py",
        "router/providers/openrouter_provider.py",
        "router/providers/google_gemini_provider.py",
        "router/providers/fal_provider.py",
        r"Project Chimera\worker.py", # Updated name
        r"Project Hyperion\hyperion_director.py",
        r"Project Midas\midas_home.py"
    ]
    
    # Check for Chimera path (user calls it source/worker.py or various paths)
    # Based on earlier reads: "Project Chimera/source/worker.py"
    chimera_worker = r"Project Chimera\source\worker.py"
    if os.path.exists(chimera_worker):
        files_to_dump[-3] = chimera_worker

    output_file = "Aergia_Full_Codebase.md"
    
    with open(output_file, "w", encoding="utf-8") as f_out:
        f_out.write("# AERGIA STUDIO PROPRIETARY CODEBASE (V2 Intelligence)\n")
        f_out.write(f"Generated on {os.path.basename(os.getcwd())}\n\n")
        
        for file_path in files_to_dump:
            full_path = os.path.abspath(file_path)
            if os.path.exists(full_path):
                f_out.write(f"## File: {file_path}\n")
                f_out.write("```python\n")
                try:
                    with open(full_path, "r", encoding="utf-8") as f_in:
                        f_out.write(f_in.read())
                except Exception as e:
                    f_out.write(f"# Error reading file: {e}\n")
                f_out.write("\n```\n\n")
                print(f"Added: {file_path}")
            else:
                print(f"Skipped (Not Found): {file_path}")

if __name__ == "__main__":
    create_codebase_dump()
