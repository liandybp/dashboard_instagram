# Load environment variables with override
from dotenv import load_dotenv
load_dotenv(override=True)

# Set page config as the FIRST command in the script
import streamlit as st

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import re
from zoneinfo import ZoneInfo
import os

# Import our custom modules
import refresh
from idea_filters import is_substantive_comment
import ideas

# Define ID stripping patterns
_ID_PATTERN_LONG = re.compile(r"\b(post|comment|message)[\s_-]?id[:\s]*\d+\b", re.IGNORECASE)

# Rest of the app code would go here...