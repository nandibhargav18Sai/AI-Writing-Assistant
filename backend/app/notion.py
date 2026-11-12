from notion_client import Client

from app.config import (
    NOTION_TOKEN,
    NOTION_PAGE_ID
)


def save(text):

    if not NOTION_TOKEN or not NOTION_PAGE_ID:

        raise Exception(
            "Notion configuration missing"
        )


    if not text.strip():

        raise Exception(
            "No content available to save"
        )


    notion = Client(
        auth=NOTION_TOKEN
    )


    notion.blocks.children.append(

        block_id=NOTION_PAGE_ID,

        children=[

            {

                "object": "block",

                "type": "paragraph",

                "paragraph": {

                    "rich_text": [

                        {

                            "type": "text",

                            "text": {

                                "content": text[:2000]

                            }

                        }

                    ]

                }

            }

        ]

    )