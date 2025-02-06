from scrapegraphai.graphs import SmartScraperGraph
import streamlit as st
graph_config = {
   "llm": {
       "api_key": st.secrets["OPENAI_API_KEY"],
       "model": "openai/gpt-4o-mini",
   },
   "verbose": True,
   "headless": False,
}
smart_scraper_graph = SmartScraperGraph(
    prompt="return a summary of this website, include all the resource that relevant to RAG",
    source="https://buttondown.com/ainews/archive/ainews-how-to-scale-your-model-by-deepmind/",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()

import json
print(json.dumps(result, indent=4))