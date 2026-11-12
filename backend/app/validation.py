import re

from app.ai import client
from app.prompts import (
    BLOCKED,
    ERROR_MESSAGE
)


FEATURE_CHECK_PROMPT = """
You are an academic content validator.

Your job is to decide whether a requested topic is suitable for
educational, academic, technical, or professional learning content.

Content Type:
{content_type}

Topic:
{topic}

ALLOW the topic if it is clearly related to one or more of:

- School or college education
- Academic subjects
- Engineering
- Computer Science
- Artificial Intelligence
- Machine Learning
- Programming
- Software Engineering
- Cloud Computing
- AWS
- Azure
- Networking
- Cybersecurity
- Databases
- Operating Systems
- Data Structures
- Algorithms
- Mathematics
- Physics
- Chemistry
- Biology
- Electronics
- Electrical Engineering
- Mechanical Engineering
- Civil Engineering
- Information Technology
- Technology concepts
- Scientific concepts
- Research
- Professional skills
- Career-related learning
- Technical explanations
- Educational general knowledge

IMPORTANT:

A real-world object or technology is allowed when the purpose is
to explain how it works, its principles, components, technology,
history, applications, advantages, disadvantages, or educational use.

Examples of allowed topics:

- How a phone charger works
- Phone charger technology
- How AWS CloudWatch works
- Python programming
- Machine learning algorithms
- How an operating system works
- Database normalization
- Computer networking
- Solar cell working principle

REJECT the topic if it is primarily:

- Entertainment
- Movies or celebrities
- Sports news or match discussion
- Food or recipes
- Restaurants
- Travel or tourism
- Shopping or product recommendations
- Personal opinions
- Personal relationships
- General lifestyle
- Fashion
- Gossip
- Random conversation
- Political content
- Hate or harassment
- Violence
- Crime
- Illegal activities
- Fraud or scams
- Exam leaks
- Question paper leaks
- Cheating
- Academic malpractice

IMPORTANT:

Judge the PURPOSE of the topic, not just individual words.

For example:

"How does a phone charger work?"
= YES

"Best phone charger to buy"
= NO

"Technology behind electric vehicles"
= YES

"Best car to buy"
= NO

"How does GPS technology work?"
= YES

"Best places to visit"
= NO

Reply with exactly:

YES

or

NO
"""


def contains_blocked(text):
    """
    Check for explicitly restricted content.
    """

    text = text.lower()

    for word in BLOCKED:

        pattern = r"\b" + re.escape(word.lower()) + r"\b"

        if re.search(pattern, text):
            return True

    return False


def validate_feature(content_type, topic):
    """
    Validate whether the topic is educational/academic
    before generating content.
    """

    topic = topic.strip()

    # --------------------------------
    # 1. Empty topic check
    # --------------------------------

    if not topic:

        return False, "Topic required."


    # --------------------------------
    # 2. Content type check
    # --------------------------------

    allowed_content_types = [

        "Email",
        "LinkedIn Post",
        "Blog",
        "Essay",
        "Study Notes",
        "Quiz Generation"

    ]

    if content_type not in allowed_content_types:

        return False, "Invalid content type."


    # --------------------------------
    # 3. Explicit blocked-content check
    # --------------------------------

    if contains_blocked(topic):

        return False, ERROR_MESSAGE


    # --------------------------------
    # 4. AI academic-topic validation
    # --------------------------------

    prompt = FEATURE_CHECK_PROMPT.format(

        content_type=content_type,
        topic=topic

    )


    try:

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=[

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            temperature=0,

            max_completion_tokens=100,

            reasoning_effort="low",

            reasoning_format="hidden"

        )


        result = (

            response
            .choices[0]
            .message
            .content
            .strip()
            .upper()

        )


        print(

            "Validation:",

            content_type,

            "|",

            topic,

            "|",

            repr(result)

        )


        # --------------------------------
        # 5. Allow only YES
        # --------------------------------

        if result.startswith("YES"):

            return True, ""


        # --------------------------------
        # 6. Reject non-academic topic
        # --------------------------------

        return False, (

            "This topic is not related to "
            "education, academics, technology, "
            "or professional learning. "
            "Please enter an educational or "
            "study-related topic."

        )


    except Exception as e:

        print(

            "Validation error:",

            str(e)

        )


        return False, (

            "Unable to validate the topic. "
            "Please try again."

        )