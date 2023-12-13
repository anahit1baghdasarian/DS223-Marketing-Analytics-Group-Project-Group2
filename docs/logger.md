# **Custom Formatter for Informative Logging**

The `CLV_Analysis/Logger/logger` module defines a custom logging formatter, `CustomFormatter`, to provide informative and colored output in log messages.

## **Classes:**

- **`CustomFormatter`**: Custom formatter for informative logging.

## **Usage:**

- Instantiate **`CustomFormatter`** and apply it to your logger's handler to enable colored and formatted logging output.

## **Example:**

```py
import logging
import os

logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

logger.debug("debug message")
logger.info("Warning: Email has not been sent...")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")
```

## **Note:**

- The formatter uses ANSI escape codes for colored output.

- Ensure that the console supports ANSI escape codes for proper display.