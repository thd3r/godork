from src.services.version import CURRENT_VERSION

"""
The print_banner function is a simple yet visually impactful component designed to display a startup banner when the program is launched. 
It provides users with immediate version information and the current status of the tool in an aesthetically styled format using ASCII art.

Purpose:

    * The function is primarily used to enhance user experience by visually indicating:
    * The tool's name or identity (in this case, associated with thd3r & societyprojects)
    * The current version of the tool (CURRENT_VERSION)
    * The status of the tool (e.g., latest, outdated, or other custom labels)

"""

def print_banner(status):
    # This shows a banner when the program starts.
    
    banner = rf"""
                             __         __  
               ___ ____  ___/ /__  ____/ /__
              / _ `/ _ \/ _  / _ \/ __/  '_/  {CURRENT_VERSION}
              \_, /\___/\_,_/\___/_/ /_/\_\    {status}
             /___/                                                                                                            
                        thd3r & societyprojects                       
    """
    print(banner)