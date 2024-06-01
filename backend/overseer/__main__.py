import uvicorn
from overseer.chronicler.config import get_logging_config


if __name__ == "__main__":
    uvicorn.run(
        'overseer.main:app',
        reload=True,
        log_config=get_logging_config(),
    )
