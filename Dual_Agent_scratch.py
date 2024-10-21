import google.generativeai as genai
import os
from typing import Dict, Any

class ContentGenerator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def generate_content(self, prompt: str) -> str:
        """Generate initial content using Gemini."""
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {str(e)}"

class ContentStructurer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def structure_content(self, content: str) -> Dict[str, Any]:
        """Structure the content into a organized format."""
        structuring_prompt = f"""
        Please structure the following content into a well-organized format with:
        - Main topics
        - Key points
        - Supporting details
        - Action items (if any)
        
        Content to structure:
        {content}
        
        Return the response in a clear, hierarchical format.
        """
        
        try:
            response = await self.model.generate_content_async(structuring_prompt)
            return self._parse_structured_content(response.text)
        except Exception as e:
            return {"error": f"Error structuring content: {str(e)}"}
    
    def _parse_structured_content(self, structured_text: str) -> Dict[str, Any]:
        """Parse the structured text into a dictionary format."""
        
        sections = {
            "main_topics": [],
            "key_points": [],
            "supporting_details": [],
            "action_items": []
        }
        
        current_section = None
        for line in structured_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if "Main Topics:" in line or "Main topics:" in line:
                current_section = "main_topics"
            elif "Key Points:" in line or "Key points:" in line:
                current_section = "key_points"
            elif "Supporting Details:" in line or "Supporting details:" in line:
                current_section = "supporting_details"
            elif "Action Items:" in line or "Action items:" in line:
                current_section = "action_items"
            elif current_section and line.startswith('-'):
                sections[current_section].append(line[1:].strip())
                
        return sections

class DualAgentSystem:
    def __init__(self, api_key: str):
        self.generator = ContentGenerator(api_key)
        self.structurer = ContentStructurer(api_key)
    
    async def process_prompt(self, prompt: str) -> Dict[str, Any]:
        """Process the prompt through both agents."""
        # First-ag
        raw_content = await self.generator.generate_content(prompt)
        
        # Second ag
        structured_content = await self.structurer.structure_content(raw_content)
        
        return {
            "raw_content": raw_content,
            "structured_content": structured_content
        }


async def main():

    api_key = ""

    system = DualAgentSystem(api_key)
    

    prompt = "Explain the concept of machine learning and its applications"
    
  
    result = await system.process_prompt(prompt)
    

    print("Raw Content:")
    print("-" * 50)
    print(result["raw_content"])
    print("\nStructured Content:")
    print("-" * 50)
    print(result["structured_content"])


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())