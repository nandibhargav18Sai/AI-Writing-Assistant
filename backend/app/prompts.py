SYSTEM_PROMPT = """
You are an AI Writing Assistant.

Support only:
- Educational writing
- Academic writing
- Professional communication
- Learning content

Do not create:
- Political content
- Harassment or hate content
- Illegal activity content
- Personal complaints
- Harmful content
- Exam cheating or malpractice content

Rules:
- Return only the requested content.
- Do not mention AI.
- Do not generate multiple versions.
- Do not generate alternate answers unless explicitly requested.
- No Markdown.
- No *, **, ## formatting.
- Use square placeholders only.
"""


BLOCKED = [
    "politics", "political", "election", "campaign", "weapon", "violence", "crime",
    "illegal", "drug", "harassment", "hate", "abuse", "leak", "paper leak",
    "exam leak", "question leak", "answer leak", "cheating", "fraud", "scam",
    "hack", "hacking", "malpractice", "impersonation", "forgery", "bribe", "corruption"
]


ERROR_MESSAGE = (
    "Sorry, I can only help with educational writing, "
    "academic writing, professional communication, and learning content."
)


CONTENT_TYPES = [
    "Email",
    "LinkedIn Post",
    "Blog",
    "Essay",
    "Study Notes",
    "Quiz Generation"
]


IMPROVE_TASKS = [
    "Correct Grammar",
    "Rewrite & Improve",
    "Summarize",
    "Expand"
]


TEMPLATES = {

    "Email":
    """
Create a professional educational email.

Use placeholders only.

Format:

Subject:

Dear [Recipient Name],

Email content.

Regards,
[Your Name]
""",

    "LinkedIn Post":
    """
Create an educational LinkedIn post.

Rules:
- Maximum 150 words.
- Share knowledge or learning.
- Add educational hashtags.
""",

    "Blog":
    """
Create an educational blog.

Structure:

Title

Introduction

Main Concepts

Examples

Conclusion
""",

    "Essay":
    """
Create an academic essay.

Structure:

Title

Introduction

Body

Conclusion
""",

    "Study Notes":
    """
Create study notes.

Include:

Topic Overview

Definitions

Key Points

Examples

Summary
"""
}


QUIZ_PROMPT = """
Create ONE educational multiple-choice quiz about the requested topic.

The quiz MUST contain exactly 5 questions.

IMPORTANT:
Every question MUST have an actual question sentence.
Never leave the question text empty.

For every question:

1. Write the question immediately after "Question X:"
2. Provide exactly four options.
3. Options must be A, B, C and D.
4. Only ONE option must be correct.
5. Questions must test the requested educational topic.
6. Do not generate random or unrelated questions.
7. Do not repeat questions.
8. Do not provide explanations.
9. Provide the answer key at the end.

Use EXACTLY this format:

Question 1: [actual question text]
A. [option]
B. [option]
C. [option]
D. [option]

Question 2: [actual question text]
A. [option]
B. [option]
C. [option]
D. [option]

Question 3: [actual question text]
A. [option]
B. [option]
C. [option]
D. [option]

Question 4: [actual question text]
A. [option]
B. [option]
C. [option]
D. [option]

Question 5: [actual question text]
A. [option]
B. [option]
C. [option]
D. [option]

Answer Key:
1. [A/B/C/D]
2. [A/B/C/D]
3. [A/B/C/D]
4. [A/B/C/D]
5. [A/B/C/D]

IMPORTANT:
Never output:

Question 1:
A.
B.
C.
D.

The question text must always be present.

The quiz must be educational, academic, technical, or professional-learning content.
"""



GRAMMAR_PROMPT = """
Correct grammar mistakes in the given text.

Rules:
- Keep original meaning.
- Improve grammar and readability.
- Return only final content.
"""


REWRITE_PROMPT = """
Rewrite the given content.

Rules:
- Improve clarity.
- Improve professionalism.
- Keep original meaning.
- Return only final content.
"""


SUMMARY_PROMPT = """
Summarize the given content.

Rules:
- Keep important information.
- Remove unnecessary details.
- Return only summary.
"""


EXPAND_PROMPT = """
Expand the given content.

Rules:
- Add explanations.
- Add examples.
- Keep the original topic.
- Return only final content.
"""
