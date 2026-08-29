import os
from dotenv import load_dotenv
from agent_engine import EchoChamberAgent

load_dotenv()

def main():
    print("==================================================")
    print("   ECHO-CHAMBER: Subcultural Intelligence Agent   ")
    print("==================================================\n")
    
    sample_scene = """
    MARCUS: Hey man, this place is totally wild! Let's get some food nearby.
    DEVON: For real, bro. I heard the spot down the street is super cool.
    """
    
    location = "Port of Spain"
    subculture = "Trinidadian youth culture"
    
    print(f"Ingesting Scene [Location: {location} | Subculture: {subculture}]...\n")
    
    agent = EchoChamberAgent()
    output = agent.run_pipeline(sample_scene, location, subculture)
    
    print("--- AGENT OUTPUT & CULTURAL LEDGER ---")
    print(output)

if __name__ == "__main__":
    main()
