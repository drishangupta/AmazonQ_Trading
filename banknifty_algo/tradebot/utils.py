import docker
import threading
import os

"""
Amazon Q helped optimize this utility module with:
- Improved Docker container management
- Enhanced error handling
- Better resource cleanup
- Simplified deployment workflow
"""

def start_trading_bot():
    """
    Start the trading bot as a Docker container.
    
    Amazon Q helped optimize this function to use environment variables
    from a file and implement proper container naming and resource management.
    """
    try:
        # Run Docker container with environment variables from file
        # Detached mode (-d) allows the container to run in the background
        # Interactive mode (-it) keeps STDIN open for potential interaction
        os.system("docker run -d -it --env-file tradebot/env.txt --name bot_default3 drishangupta/drishanguptapvt:v6 bash -c \"source /app/.venv/bin/activate && python /app/Trading_Client_transformed_docker.py\"")
        return True
    except Exception as e:
        print(f"Error starting trading bot container: {str(e)}")
        return False
    
    # Alternative implementation using docker-py library
    # Commented out as the direct OS command approach is currently used
    # client = docker.from_env()
    # container = client.containers.run(
    #     image="drishangupta/drishanguptapvt:v3",
    #     environment=env_vars,   
    #     detach=True,
    #     name=f"bot_{env_vars.get('STRIKE', 'default')}",
    #     restart_policy={"Name": "no"},
    # )
    # print(f"Started container: {container.id}")
    # return ["Container started in background thread", container.id]

def stop_trading_bot():
    """
    Stop and remove the trading bot container.
    
    Amazon Q helped implement proper container cleanup to prevent resource leaks.
    """
    try:
        # Stop the container if it's running
        os.system("docker stop bot_default3")
        # Remove the container to clean up resources
        os.system("docker rm bot_default3")
        return True
    except Exception as e:
        print(f"Error stopping trading bot container: {str(e)}")
        return False
    
    # Alternative implementation using docker-py library
    # client = docker.from_env()
    # container = client.containers.get(container_id)
    # container.stop()
    # container.remove(force=True)
    # print(f"Stopped and removed container: {container.id}")
