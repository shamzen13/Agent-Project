"""
tagger.py
Sends articles to the Claude API and extracts structured metadata.
Returns a clean dictionary of tags for each article.
"""

import json
import logging
import anthropic
from config import ANTHROPIC_API_KEY


logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key = ANTHROPIC_API_KEY)

#PROMPT

SYSTEM_PROMT = """you are an analytical assistant specializing in theology, political philosophy and ideological analysis.
your job is to read articles and extract structured metadata from them.

you always respond with valid JSON only - no preamble, no explanation, no markdown code blocks. just the raw JSON object.
"""

def build_user_prompt(title: str, content: str, category: str) -> str:
    return f"""Analyse this {category} article and return a JSON object with exactly these fields:
{{
    "summary": "2-3 sentence summary of the core argument or news",
  "themes": ["theme1", "theme2", "theme3"],
  "ideological_lean": "one of: progressive / conservative / centrist / libertarian / authoritarian / unclear",
  "theological_tradition": "e.g. Catholic, Protestant, Islamic, Jewish, Secular, Liberation Theology, None, etc.",
  "emotional_tone": "one of: urgent / hopeful / critical / neutral / fearful / celebratory / mournful"
}}

Article title : {title}
Article content:
{content[:3000]}

Return only the JSON object, NO other text"""


def tag_article(article_id: int, title: str, content: str, category: str) -> dict | None:
    """
    Sends a single article to Claude for tagging.
    Returns a dict of tags or None if the request fails.
    """
        
    try:
        message = client.messages.create(
            model = "claude-opus-4-6",
            max_tokens = 512,
            system = SYSTEM_PROMT,
            messages = [
                  
                  {
                    "role": "user",
                    "content" : build_user_prompt(title,content,category)
                  }

            ]
        )

        raw_response = message.content[0].text.strip()
        logger.debug(f"raw claide response for article {article_id} : {raw_response}")
      
        #parse json response
        tags = json.loads(raw_response)

        #validate expected keys are present
        required_keys = ["summary", "themes" , "ideological_lean" , "theological_tradition", "emotional_tone"]

        for key in required_keys:
               if key not in tags:
                    logger.warning(f"missing key '{key}' in response for article {article_id} ")
                    tags[key] = "unknown"


        #ensure themes is a list
        if not isinstance(tags["themes"], list):
            tags["themes"] = [tags["themes"]]

        logger.info(f"tagged article {article_id}: {tags['ideological_lean']} | {tags['emotional_tone']}")
        return tags

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error for article {article_id}: {e}")
        logger.error(f"Raw response was: {raw_response}")
        return None

    except anthropic.APIError as e:
        logger.error(f"Claude API error for article {article_id}: {e}")
        return None

    except Exception as e:
        logger.error(f"Unexpected error tagging article {article_id}: {e}")
        return None




        
                

      


