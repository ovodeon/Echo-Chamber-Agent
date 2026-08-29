import os
import json
from google import genai
from parallel_mcp import ParallelMCPClient

class EchoChamberAgent:
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise ValueError("GEMINI_API_KEY is required.")
        self.client = genai.Client(api_key=gemini_key)
        self.mcp_client = ParallelMCPClient()

    def run_pipeline(self, scene_draft: str, target_location: str, subculture: str) -> str:
        # STEP 1: Tropes & Idiom Extraction
        step1_prompt = f"""
        Analyze this script scene set in '{target_location}' involving '{subculture}'.
        Identify:
        1. Outdated tropes or unnatural dialogue lines.
        2. Specific subcultural idioms or slang that need live web verification.
        
        SCENE:
        {scene_draft}
        """
        step1_res = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=step1_prompt
        )
        trope_analysis = step1_res.text

        # STEP 2: Grounding via Parallel MCP
        search_objective = f"Find authentic, current vernacular and cultural terms for {subculture} in {target_location}."
        search_query = f"{subculture} dialect conversation terms {target_location}"
        mcp_data = self.mcp_client.search_subculture(search_objective, search_query)

        # STEP 3: Dialogue Rewriting & Authenticity Ledger Generation
        step3_prompt = f"""
        You are an elite dialogue co-director and subcultural authenticity analyst.
        
        ORIGINAL SCENE:
        {scene_draft}
        
        ANALYSIS OF ORIGINAL DIALOGUE:
        {trope_analysis}
        
        REAL-TIME GROUNDING DATA (Parallel MCP):
        {json.dumps(mcp_data)}
        
        TASKS:
        1. Provide the REWRITTEN SCENE with authentic, natural dialogue flow.
        2. Provide a 'CULTURAL AUTHENTICITY LEDGER' explaining:
           - Specific changes made.
           - Why original lines were replaced (citing tropes vs. grounded vernacular).
        """
        step3_res = self.client.models.generate_content(
            model="gemini-2.5-pro",
            contents=step3_prompt
        )
        return step3_res.text
