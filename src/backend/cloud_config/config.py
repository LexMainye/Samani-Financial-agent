# Configuration for serverless execution or environment setup
class ModalConfig:
    TIMEOUT_SECONDS = 300
    GPU_ENABLED = False
    MEMORY_MB = 1024
    
    # Supported file types for the parsing tool
    SUPPORTED_EXTENSIONS = {'.csv', '.xlsx', '.pdf'}

    # Default forecasting parameters
    FORECAST_STEPS = 4